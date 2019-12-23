# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.

"""
Requires own set set of configuration options. See fd_integrator.cfg.yml for the required section.
"""

import logging
from threading import Lock
from itertools import chain
from collections import namedtuple

from IoticAgent.IOT.Client import Client
from IoticAgent.IOT.Exceptions import IOTUnknown, IOTSyncTimeout, LinkShutdownException

from ioticlabs.dt.common.meta import ThingMeta
from ioticlabs.dt.common.item_cache import get_cache        ### what is 'item_cache' ..?

from ioticlabs.dt.api.util import NestedConfig

from ioticlabs.dt.api.integrator import (  # noqa (unused import)
    Integrator as IntegratorBase, IntegratorCallbacks as IntegratorCallbacksBase, IntegratorException, AssetUnknown,
    EventPublishFailure
)

from ..defaults import Asset
from ..values import Sample, Values

log = logging.getLogger(__name__)
DEBUG_ENABLED = log.isEnabledFor(logging.DEBUG)


class FdPublishFailure(EventPublishFailure):
    pass
### where EventPublishFailure came from?

class FdIntegratorCallbacks(IntegratorCallbacksBase):  # pylint: disable=abstract-method
    """Callbacks to implement when using this integrator. Noteable changes (over base integrator):
### Callbacks needs to implement???
    on_asset_created
        - Called only once field data twin has also been create. If this fails, no callback for the asset will be made.
    """
    pass


class _ThingDetails(namedtuple('_ThingDetails', 'lid_prefix tag_prefix recent_samples meta')):

    __slots__ = ()

    @classmethod
    def from_config(cls, config):
        return cls(
            # Local id (lid) prefix for Iotic Thing
            lid_prefix=NestedConfig.get(
                config, 'asset.thing.prefix.lid', required=False, default=Asset.Thing.LID_PREFIX,
                check=NestedConfig.Check.non_empty_str
            ),
            # Unique tag prefix
            tag_prefix=NestedConfig.get(
                config, 'asset.thing.prefix.tag', required=False, default=Asset.Thing.TAG_PREFIX,
                check=NestedConfig.Check.non_empty_str
            ),
            # Number of recent data samples to save
            recent_samples=NestedConfig.get(
                config, 'asset.thing.recent.samples', required=False, default=Asset.Point.Fielddata.RECENT_DATA,
                check=lambda x: isinstance(x, int) and x >= -1
            ),
            # Metadata for field data things
            meta=ThingMeta.from_config(config, 'asset.thing.meta', tag_default=Asset.Thing.TAGS)
        )


class FdIntegrator(IntegratorBase):

    class _Callbacks(IntegratorCallbacksBase):
        """Hide integrator callback implementation from users of FdIntegrator class"""

        def __init__(self, parent):         ### What is 'parent' and where does it came from...???
            if not isinstance(parent, FdIntegrator):
                raise TypeError('parent')
            self.__parent = parent

        def on_asset_created(self, asset_id):
            self.__parent._on_asset_created(asset_id)

        def on_asset_deleted(self, asset_id):
            self.__parent._on_asset_deleted(asset_id)

        def on_t2_request(self, request):
            self.__parent._on_t2_request(request)

    def __init__(self, config, fd_config, client, callbacks, fd_client=None):
        """
        config - base integrator config
        fd_config - field data integrator specific configuration
        client - agent instance, as with base Integrator
        callbacks - instance of FdIntegratorCallbacks
        fd_client - additional agent to use for handling field data things, e.g under different owner. Defaults to
            `client` if not specified.
        """
        super().__init__(config, client, self._Callbacks(self))
        if not isinstance(callbacks, FdIntegratorCallbacks):
            raise TypeError('callbacks')
        self.__callbacks = callbacks
        if fd_client:
            if not isinstance(fd_client, Client):
                raise TypeError('client')
            self.__client = fd_client
        else:
            # already checked by parent __init__
            self.__client = client

        self.__lock = Lock()

        self.__thing_details = _ThingDetails.from_config(fd_config)

        self.__cache = get_cache(fd_config, config_path='asset.cache.method')
        # Mapping of asset id to feed. Values can be None if feed is being initialised
        self.__feeds = {}

    def start(self):
        self.__cache.start()
        super().start()

    def stop(self, timeout=10):
        super().stop(timeout=timeout)
        self.__cache.stop()

    # TODO async version (concurrent futures? handle in same way as base integrator)
    # TODO - other IOT exceptions?
    def publish_fielddata(self, sample):
        """Publish (share) field data synchronously.

        sample - instance of values.Sample

        raises
            TypeError - If sample is invalid
            ValueError - If sample has invalid (or missing) values
            AssetUnknown - If the integrator is currently not handling this asset
            FdPublishFailure - If the sample could not be published. Note: Timeouts are governed by agent and integrator
                configuration.
        """
        if not isinstance(sample, Sample):
            raise TypeError('sample')

        # TODO - perform additional per-value validation here?
        if sample.template.missing:
            raise ValueError('Not all values set')

        try:
            feed = self.__feeds[sample.asset]
        except KeyError as ex:
            raise AssetUnknown(sample.asset) from ex

        try:
            feed.share(sample.template, time=sample.time)
        except IOTUnknown as ex:
            raise AssetUnknown(sample.asset) from ex
        except LinkShutdownException:
            raise FdPublishFailure(sample.asset, EventPublishFailure.Reason.SHUTDOWN)
        except IOTSyncTimeout as ex:
            raise FdPublishFailure(sample.asset, EventPublishFailure.Reason.LOCAL_TIMEOUT)

    # TODO - queue these up somewhere so can retry if creation fails?
    # indirectly for IntegratorCallbacksBase (see _Callbacks)
    def _on_asset_created(self, asset_id):
        with self.__lock:
            if asset_id in self.__feeds:
                # Not expecting multiple notifications for same asset in quick succession
                log.warning('Asset %s already pending, ignoring')
                return
            # Populate with temporary value so do not have to lock for whole creation
            self.__feeds[asset_id] = None

        try:
            shallow = self.__cache.is_known(asset_id)
            feed = self.__create_feed_for(asset_id, shallow)
            if not (shallow or self.__cache.mark_as_known(asset_id)):
                log.warning('Cache marking for %s failed', asset_id)
        except LinkShutdownException:
            # Shutdown requested whilst request pending
            return
        except:
            log.error('Asset creation failed', exc_info=True)
            with self.__lock:
                self.__delete_thing_for(asset_id)
            return

        with self.__lock:
            if asset_id in self.__feeds:
                self.__feeds[asset_id] = feed
            # on_asset_deleted has been triggered in mean time
            else:
                log.warning('Asset %s no longer applies, removing again', asset_id)
                self.__delete_thing_for(asset_id)

        log.debug('Provisioned asset %s (shallow=%s)', asset_id, shallow)

        self.__callbacks.on_asset_created(asset_id)

    def __create_feed_for(self, asset_id, shallow):
        """If shallow is set, only minimal creation will occur, e.g. metadata will not be set for the thing and points.
        """
        details = self.__thing_details
        thing = self.__client.create_thing(details.lid_prefix + asset_id)

        if thing.agent_id != self.__client.agent_id:
            log.warning('Reassigning %s from %s', thing.lid, thing.agent_id)
            thing.reassign(self.__client.agent_id)

        feed = thing.create_feed(Asset.Point.Fielddata.LID)

        if not shallow:
            thing_meta = details.meta

            feed.set_recent_config(max_samples=details.recent_samples)

            thing.create_tag(list(chain((details.tag_prefix + asset_id,), thing_meta.tags)))

            if thing_meta.label or thing_meta.description:
                with thing.get_meta() as meta:
                    if thing_meta.label:
                        meta.set_label(thing_meta.label)
                    if thing_meta.description:
                        meta.set_description(thing_meta.description)

            with feed.get_meta() as meta:
                meta.set_label(Asset.Point.Fielddata.LABEL)
                meta.set_description(Asset.Point.Fielddata.DESCRIPTION)

            for value in Values.all_values():
                feed.create_value(value.label, vtype=value.type_, unit=value.unit, description=value.description)

        return feed

    def __delete_thing_for(self, asset_id):
        """Clear up field data thing and remove feed reference. MUST be called within lock."""
        try:
            self.__client.delete_thing(self.__thing_details.lid_prefix + asset_id)
        except IOTUnknown:
            pass
        except LinkShutdownException:
            # Shutdown requested whilst request pending
            return
        except:
            log.warning('Asset deletion failed', exc_info=DEBUG_ENABLED)

        self.__feeds.pop(asset_id, None)
        if not self.__cache.unmark(asset_id):
            log.warning('Failed to unmark asset %s in cache', asset_id)

    # indirectly for IntegratorCallbacksBase (see _Callbacks)
    def _on_asset_deleted(self, asset_id):
        log.debug('Deleting asset %s', asset_id)
        with self.__lock:
            self.__delete_thing_for(asset_id)

        self.__callbacks.on_asset_deleted(asset_id)

    # indirectly for IntegratorCallbacksBase (see _Callbacks)
    def _on_t2_request(self, request):
        self.__callbacks.on_t2_request(request)

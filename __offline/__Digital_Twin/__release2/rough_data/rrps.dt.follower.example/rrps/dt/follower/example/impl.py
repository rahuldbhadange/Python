# Copyright (c) 2018 Iotic Labs Ltd. All rights reserved.

from hashlib import sha1
from pprint import pformat
import logging

from IoticAgent import ThingRunner
from IoticAgent.IOT.Config import Config

from ioticlabs.dt.api.follower import (
    Follower, FollowerCallbacks, NamedEventMixin, T2ResponseException, AssetUnknown, T2ReqFailureReason, T2Unavailable,
    T2Timeout
)

log = logging.getLogger(__name__)


# Set to True to enable to test T2 request functionality
ENABLE_T2_PROMPT = False


class FollowerExample(NamedEventMixin, FollowerCallbacks, ThingRunner):

    def __init__(self, config, agent_config_str):
        super().__init__(config=Config(string=agent_config_str))

        if not (isinstance(config, dict) and 'follower' in config):
            raise ValueError('Configuration invalid / missing "follower" section')

        # Whilst the follower core requires particular configuration, top-level sections could be defined to provide
        # parameters specific to this follower.
        self.__follower = Follower(config['follower'], self.client, self)
        self.__assets = set()

    def on_startup(self):
        log.debug('Startup')
        self.__follower.start()

    def main(self):
        log.debug('Running')
        while not self.wait_for_shutdown(2):
            if ENABLE_T2_PROMPT:
                for asset in list(self.__assets):
                    input('Press ENTER for T2 example request for %s' % asset)
                    self.example_t2_call(asset)

    def example_t2_call(self, asset):
        """Send an example request & computes sha1 sum of returned raw data"""
        log.debug('Sending t2 request for %s', asset)
        mime = None
        check = sha1()
        try:
            for mime, chunk in self.__follower.t2_request(
                    asset, 'AcmecorpExampleReq', data='small.pdf'.encode('utf8'), timeout=10
            ):
                # Note: can access mime type as soon as first chunk arrives
                check.update(chunk)
        except AssetUnknown:
            log.warning('T2 - Asset %s no longer known, ignoring', asset)
        except T2ResponseException as ex:
            # ex.reason is T2ReqFailureReason - see code documentation for what they mean
            if ex.reason == T2ReqFailureReason.REQ_UNHANDLED:
                log.error('T2 request not handled by provider')
            # equivalent to HTTP 404
            elif ex.reason == T2ReqFailureReason.RESOURCE_UNKNOWN:
                log.error('Data not available for given request and asset')
            else:
                log.error('T2 failed - reason: %s', ex.reason)
        except T2Unavailable:
            log.critical('T2 functionality not enabled in follower')
        except T2Timeout:
            log.error('T2 request timed out')
        except:
            # TODO - agent related exceptions
            log.exception('Other T2 failure')
        else:
            log.debug('Response mime: %s sha1: %s', mime, check.hexdigest())

    def on_shutdown(self, exc_info):
        log.debug('Shutdown')
        self.__follower.stop()

    # for FollowerCallbacks
    def on_asset_created(self, asset_id):
        log.info('Asset created: %s', asset_id)
        self.__assets.add(asset_id)

    # for FollowerCallbacks
    def on_asset_deleted(self, asset_id):
        log.info('Asset deleted: %s', asset_id)
        self.__assets.remove(asset_id)

    # For NamedEventMixin (specific event)
    def do_bombuiltset(self, event):
        log.info(
            '[%s] #%d BoM-as-built (from %s) @ %s (sys: %s)\n%s', event.asset, event.offset, event.source, event.time,
            event.systime, pformat(event.data)
        )
        self.__follower.ack_event(event)

    # for NamedEventMixin (all events for which there isn't a do_ method)
    def on_event_unmatched(self, event):
        log.info(
            '[%s] #%d %s (from %s) @ %s (sys: %s)\n%s', event.asset, event.offset, event.name(), event.source,
            event.time, event.systime, pformat(event.data)
        )
        # Indicate that event has been processed. If asset has been deleted in the mean time, this will be a no-op.
        self.__follower.ack_event(event)

    def on_event_internal(self, event):
        log.info('Internal: %s', event)

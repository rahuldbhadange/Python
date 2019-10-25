# Copyright (c) 2018 Iotic Labs Ltd. All rights reserved.
import logging
from enum import IntEnum, unique
from abc import ABCMeta, abstractmethod
from collections import namedtuple, OrderedDict
from collections.abc import Mapping
from contextlib import contextmanager
from ..util import import_class_item, NestedConfig
log = logging.getLogger(__name__)

@unique
class BatchOpType(IntEnum):
    """Possible operations which can be batched. For internal use (by implementations) only."""
    PUT_ATTR = 1
    """put_attr()"""
    UNMARK = 2
    """unmark()"""

_BatchOp = namedtuple('_BatchOp', 'type_ args kwargs')
"""Represents a single operation to be performed in a batch. For internal use (by implementations) only.
type_ - one of BatchOpType. Identifies which function it represents
args - positional arguments for particular function
kwargs - keyword arguments for particular function
"""

class CacheBase(metaclass=ABCMeta):
    """Simple key-value abstraction used to e.g. track known assets locally. By default no other information is stored
    with the item other than its id, but it is possible to save additional attributes. Note: Attribute names nor types
    are validated, but implementations should aim support primitive types only, including bytes.
    NOTE: Only methods which explicitly state so are thread safe.
    """
    @abstractmethod
    def __init__(self, config):
        """Instantiate cache instance. Should only perform minimal tasks. Use start() to e.g. connect to backing store.
        config - mapping of config applicable to particular cache implementation
        """
        pass
    @staticmethod
    def _validate_item(item):
        """Convenience method for ensuring the item id. Should be used in any methods shich accept an item (id). Note
        that this only performs primited validation, i.e. requirements might be more strict and in such a case this
        method could be overloaded.
        Raises ValueError if invalid, returns True otherwise.
        """
        if not (isinstance(item, str) and item):
            raise ValueError('Invalid item id: %r' % item)
        return True
    def start(self):
        """Override if require setup steps. Will be called before any other methods."""
        pass
    def stop(self, timeout=10):
        """Override if require shutdown steps. Will be called as final method."""
        pass
    def __enter__(self):
        self.start()
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
    @property
    @abstractmethod
    def count(self):
        """Number of items in cache currently"""
        raise NotImplementedError
    @abstractmethod
    def is_known(self, item):
        """Returns True if the item is known locally. Must be thread safe."""
        raise NotImplementedError
    @abstractmethod
    def mark_as_known(self, item, **attrs):
        """Marks an item as known. Should be idempotent (i.e. if already marked this is a no-op apart from attributes
        being potentially updated). Must be thread safe.
        attrs - Additional attributes to set for item. Existing values will be updated if item already known.
        Returns True if managed to persist to backing store (or will do so in background)
        """
        raise NotImplementedError
    @abstractmethod
    def put_attr(self, item, **attrs):
        """Like mark_as_known except the item is replaced completely (even if is unknown).
        attrs - Attributes to set for item. Any existing attributes will be discarded.
        Returns True if managed to persist to backing store (or will do so in background)
        """
        raise NotImplementedError
    @abstractmethod
    def set_attr(self, item, **attrs):
        """Sets the given attributes for an item.
        attrs - one or more attributes to set
        Raises
            - ValueError if no attributes are supplied
            - KeyError if item is unknown
        Returns True if managed to persist to backing store (or will do so in background)
        """
    @abstractmethod
    def del_attr(self, item, *attr_names):
        """Deletes the given attributes for an item. Non-existing attributes are ignored.
        attrs - one or more attributes to delete
        Raises
            - ValueError if no attributes are supplied
            - KeyError if item is unknown
        Returns mapping of attributes for the item. This can be empty if none of the attributes are set.
        """
    @abstractmethod
    def get_attr(self, item, *attr_names):
        """Gets the given attributes for an item.
        attr_names - one or more attributes to fetch. If none are specified, all will be retrieved.
        Raises
            - KeyError if item is unknown
        Returns mapping of attributes for the item. This can be empty if none of the attributes are set.
        """
    @abstractmethod
    def unmark(self, item):
        """Opposite of mark_as_known. All additional attributes are also lost. Should be idempotent (i.e. if already
        cleared this is a no-op). Must be thread safe.
        Returns True if managed to persist to backing store (or will do so in background)
        """
        raise NotImplementedError
    @abstractmethod
    def clear(self):
        """Unmark all known items. Should be idempotent (i.e. if already cleared this is a no-op). Must be thread safe.
        Returns True if managed to persist to backing store (or will do so in background)
        """
        raise NotImplementedError
    class Batch:
        """Operations which can be performed in a batch. Arguments are the same as for non-batched methods."""
        def __init__(self, ops):
            self.__ops = ops
        def unmark(self, item):
            self.__ops[item] = _BatchOp(BatchOpType.UNMARK, (item,), {})
        def put_attr(self, item, **attrs):
            self.__ops[item] = _BatchOp(BatchOpType.PUT_ATTR, (item,), attrs)
    @contextmanager
    def batched(self):
        """Allows for methods defined in the Batch subclass to be combined into fewer requests for potentially better
        performance. Since the supported operations either completely replace or delete an item, operations are
        de-duplicated, i.e. only the last one specified for each item will be performed. If no calls have been made
        within the context, this will be a no-op.
        """
        ops = OrderedDict()
        batch = self.Batch(ops)
        yield batch
        # Won't process batch if an exception occurred
        if ops:
            self._handle_batch(ops.values())
        else:
            log.warning('No operations within batch')
    @abstractmethod
    def _handle_batch(self, batch_ops):
        """Internal method. Receives an iterable of _BatchOp instances to be processed.
        - The given operations should be batched where appropriate and performed in order.
        - Arguments can be expected to be the same as for their non-batched counterparts, but validation must be
            performed anyway.
        - This is not intended to be transactional in any way, i.e.:
            - Validation of individual operations can happen beforehand or whilst processing each one.
            - Retries should not be performed (beyond what non-batched methods already do).
            - Any failures before a batch has finished should halt processing.
        """
        raise NotImplementedError

def get_cache(config, config_path='item.cache.method'):
    """Instantiated known item cache from runner configuration"""
    method = NestedConfig.get(
        config, config_path, required=False, check=lambda x: isinstance(x, Mapping) and len(x) == 1
    )
    if method:
        name, config = next(iter(method.items()))
        if not isinstance(config, Mapping):
            raise ValueError('Expecting mapping for cache method %s config' % name)
    else:
        log.warning('No cache method specified, using memory')
        name, config = 'memory', {}
    cls = import_class_item('.item_cache.' + name, name.capitalize(), relative_module=__name__)
    if not issubclass(cls, CacheBase):
        raise TypeError('Unexpected cache type: %s' % cls)
    return cls(config)

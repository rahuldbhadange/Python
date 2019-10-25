import time
from IoticAgent.Core.Const import SearchScope, SearchType, DescribeScope
from IoticAgent.IOT import Client
from IoticAgent.IOT.utils import uuid_to_hex, logger
from markupsafe import string_types

class test (self, Client):
    def search(reduced=True, unit=None, limit=50, offset=0, scope=SearchScope.PUBLIC, **kwargs):
        # logger.info("search(text=\"%s\", lang=\"%s\", location=\"%s\", unit=\"%s\", limit=%s, offset=%s, reduced=%s)",
        #             text, lang, location, unit, limit, offset, reduced)
        location = {'lat': 52.427809, 'long': -0.327829, 'radius': 6.789}

        evt = self._request_search(location, SearchType.REDUCED if reduced else SearchType.FULL, scope, unit=None,
                                   limit=50, offset=0)
        self._wait_and_except_if_failed(evt)
        return evt.payload['result']  # pylint: disable=unsubscriptable-object
        # self.remote_feed_gpid = evt.payload['result']
        # return
        # ['points']
t=test()
t.search()

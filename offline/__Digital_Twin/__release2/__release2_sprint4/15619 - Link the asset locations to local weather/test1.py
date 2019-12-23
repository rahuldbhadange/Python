import time
from IoticAgent.Core.Const import SearchScope, SearchType, DescribeScope
from IoticAgent.IOT import Client
from IoticAgent.IOT.utils import uuid_to_hex, logger
from markupsafe import string_types


class SysthesiserWeather(Client):

    def main(self):
        with Client('test.ini') as client:
            my_thing = self.create_thing(client)
            guid_or_resource = self.search(reduced=False, scope=SearchScope.PUBLIC)
            self.describe(guid_or_resource)
            self.follow_remote_feed(my_thing)

            while True:
                try:
                    print("Main running, press ctrl+c to quit.")
                    time.sleep(10)
                except KeyboardInterrupt:
                    break

    def create_thing(self, client):
        print("Creating my Thing")

        # Create your Thing in this script
        # Note:
        #  Calling 'create_thing' will create a new Thing, unless the Thing local ID (lid) is already in use.
        #  If it is, it will connect your script to that Thing.
        my_thing = client.create_thing('My_Follower_Thing')  # GIVE IT A NAME

        # Let's have a look at it
        # print some information about your Thing
        print("About my Thing")
        print("My Thing object:", my_thing)
        print("My Thing local ID (lid):", my_thing.lid)
        print("My Thing globally unique ID (guid):", my_thing.guid)
        return my_thing

    def search(self, reduced=False, unit=None, limit=50, offset=0, scope=SearchScope.PUBLIC):
        # logger.info("search(text=\"%s\", lang=\"%s\", location=\"%s\", unit=\"%s\", limit=%s, offset=%s, reduced=%s)",
        #             text, lang, location, unit, limit, offset, reduced)
        location = dict(lat=52.427809, long=-0.327829, radius=6.789)

        evt = self._request_search(location, SearchType.REDUCED if reduced else SearchType.FULL, scope, unit=None,
                                   limit=50, offset=0)
        self._wait_and_except_if_failed(evt)
        return evt.payload['result']  # pylint: disable=unsubscriptable-object
        # self.remote_feed_gpid = evt.payload['result']
        # return
        # ['points']

    def describe(self, guid_or_resource, lang=None, local=None, scope=DescribeScope.AUTO):
        if isinstance(guid_or_resource, self.__guid_resources):
            guid = guid_or_resource.guid
        elif isinstance(guid_or_resource, string_types):
            guid = uuid_to_hex(guid_or_resource)
        else:
            raise ValueError("describe requires guid string or Thing, Point, RemoteFeed or RemoteControl instance")
        logger.info('describe() [guid="%s"]', guid)
        evt = self._request_describe(guid, lang, local, scope)
        self._wait_and_except_if_failed(evt)
        return evt.payload['result']  # pylint: disable=unsubscriptable-object


data = SysthesiserWeather()
data.main()

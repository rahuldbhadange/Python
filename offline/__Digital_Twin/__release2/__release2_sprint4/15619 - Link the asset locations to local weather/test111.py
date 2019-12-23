import time
from IoticAgent import ThingRunner
from IoticAgent.Core.Const import SearchScope, SearchType, DescribeScope
from IoticAgent.IOT import Client
from IoticAgent.IOT.utils import uuid_to_hex, logger
from markupsafe import string_types
from .Point import Point


class SysthesiserWeather(ThingRunner):
    LOOP_TIMER = 10  # minimum number of seconds duration of the main loop

    def __init__(self, config=None):
        """Instantiation code in here, after the call to super().__init__()
        """
        super(SysthesiserWeather, self).__init__(config=config)
        self.__client = Client(config=config)
        self.__thing = None
        self.__remote_control = None

    def on_startup(self):
        """Called once at the beginning, before main().
        Use this method to create your things, rebind connections, setup hardware, etc.
        """
        print("Started. Press CTRL+C to end")
        self.__thing = self.client.create_thing('weather follower thing')
        # self.__remote_control = self.__thing.attach(('offer_basic', 'offer_basic_control'))
        print("About my Thing")
        print("My Thing object:", self.__thing)
        print("My Thing local ID (lid):", self.__thing.lid)
        print("My Thing globally unique ID (guid):", self.__thing.guid)
        publish = self.find_nearest_weather()
        print(publish)

    def find_nearest_weather(self):
        print("finding nearest weather")
        # guid = self.search_reduced()
        # print("print search data")
        gpid_data = self.describe(guid_or_resource="fc5845c95d6b632d889ffe81b2d84924")
        print("printing describe data")
        print(gpid_data)

    def search_reduced(self, lang=None, unit=None, limit=100, offset=0, local=None,
                       scope=SearchScope.PUBLIC):
        # def search_reduced(self, text=None, lang=None, location=None, unit=None, limit=100, offset=0, reduced=True,
        #                    local=None,
        #                    scope=SearchScope.PUBLIC):
        """Shorthand for [search()](#IoticAgent.IOT.Client.Client.search) with `reduced=True`"""

        lang = "English"
        text = "Weather"
        location = {'lat': 52.427809, 'long': -0.327829, 'radius': 1.789}
        guid = self.__client.search(text, lang, location, unit, limit, offset, reduced=True, local=local, scope=scope)
        print(guid)
        return guid

    # def get_recent(self, count):
    #     """Get the last instance(s) of feeddata from the feed. Useful if the remote Thing doesn't publish very often.
    #     Returns an iterable of dicts (in chronologically ascending order) containing:
    #         #!python
    #         'data' # (decoded or raw bytes)
    #         'mime' # (None, unless payload was not decoded and has a mime type)
    #         'time' # (datetime representing UTC timestamp of share)
    #     `count` (mandatory) (integer) How many recent instances to retrieve. High values might be floored to a maximum
    #     as defined by the container.
    #     Note: Feed data is iterable as soon as it arrives, rather than when the request completes.
    #     """
    #     queue = Queue()
    #     evt = self.get_recent_async(count, queue.put)
    #     timeout_time = monotonic() + self._client.sync_timeout
    #     while True:
    #         try:
    #             yield queue.get(True, .1)
    #         except Empty:
    #             if evt.is_set() or monotonic() >= timeout_time:
    #                 break
    #     self._client._except_if_failed(evt)

    def search_located(self, text=None, lang=None, location=None, unit=None, limit=100, offset=0, local=None,
                       scope=SearchScope.PUBLIC):
        """See [search()](#IoticAgent.IOT.Client.Client.search) for general documentation. Provides a thing-only
        result set comprised only of things which have a location set, e.g.:

            #!python
            {
                # Keyed by thing id
                '2b2d8b068e404861b19f9e060877e002':
                    # location (g, lat & long), label (l, optional)
                    {'g': (52.4539, -1.74803), 'l': 'Weather Station #2'},
                '76a3b24b02d34f20b675257624b0e001':
                    {'g': (52.244384, 0.716356), 'l': None},
                '76a3b24b02d34f20b675257624b0e004':
                    {'g': (52.245384, 0.717356), 'l': 'Gasometer'},
                '76a3b24b02d34f20b675257624b0e005':
                    {'g': (52.245384, 0.717356), 'l': 'Zepellin'}
            }


        """
        logger.info("search_located(text=\"%s\", lang=\"%s\", location=\"%s\", unit=\"%s\", limit=%s, offset=%s)",
                    text, lang, location, unit, limit, offset)
        evt = self._request_search(text, lang, location, unit, limit, offset, SearchType.LOCATED, local, scope)

        self._wait_and_except_if_failed(evt)
        return evt.payload['result']  # pylint: disable=unsubscriptable-object

    __guid_resources = (Thing, Point, RemoteFeed, RemoteControl)

    def describe(self, guid_or_resource, lang=None, local=None, scope=DescribeScope.AUTO):
        if isinstance(guid_or_resource, self.__client.__guid_resources):
            guid = guid_or_resource.guid
        elif isinstance(guid_or_resource, string_types):
            guid = uuid_to_hex(guid_or_resource)
        else:
            raise ValueError("describe requires guid string or Thing, Point, RemoteFeed or RemoteControl instance")
        logger.info('describe() [guid="%s"]', guid)
        evt = self._request_describe(guid, lang, local, scope)
        self._wait_and_except_if_failed(evt)
        gpid = evt.payload['result']  # pylint: disable=unsubscriptable-object
        print(gpid)
        return gpid

    def follow_remote_feed(self, my_thing, remote_feed_gpid):
        print("Following remote Feed")

        # Follow remote Feed using global Point ID of the feed you want to follow
        # Note:
        #  Calling 'follow' will return the subscription object regardless of whether it already existed
        # remote_feed_gpid = 'eb6972c7281c750b4282f7aef076965b'  # ADD THE GLOBAL POINT ID OF ANY FEED YOU WANT TO FOLLOW
        print(remote_feed_gpid)
        remote_feed = my_thing.follow(remote_feed_gpid, self.follow_feed_callback)
        print(remote_feed)

        # Let's have a look at it
        # print("Remote Feed subscription object:", remote_feed)
        # # List and print subscriptions (Feeds following or Controls attached to)
        # # Note:
        # # In sub_list, 'id' is the Feed/Control global point ID (gpid)
        # sub_list = my_thing.list_connections()
        # print("Subscription list: ", sub_list)

    # def get_recent(self):
    #
    #
    # def unfollow(self):
    #
    #
    #
    def follow_feed_callback(self, args):
        print("Printing Weather data received from followed Feed")

        # Tells your Thing what to do with data received from the Feed you are following
        # Print data recieved from followed feed
        print("This is the Feed Callback with Weather data:", args['data'])


def main():
    SysthesiserWeather(config="test.ini").run()


if __name__ == '__main__':
    main()

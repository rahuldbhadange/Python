from IoticAgent.Core.compat import monotonic
from IoticAgent.ThingRunner import RetryingThingRunner
from IoticAgent import Datatypes, Units, ThingRunner
from IoticAgent.Core.Const import SearchScope, SearchType, DescribeScope
from IoticAgent.IOT import Client
from IoticAgent.IOT.utils import uuid_to_hex, logger
from markupsafe import string_types


class SysthesiserWeather(ThingRunner):

    LOOP_TIMER = 10  # minimum number of seconds duration of the main loop

    def __init__(self, config=None):
        """Instantiation code in here, after the call to super().__init__()
        """
        super(SysthesiserWeather, self).__init__(config=config)
        # self.__thing = None
        # self.__remote_control = None
        # self.Point = None
        # self.__guid_resources = (self.__thing, self.Point, self.follow_remote_feed, self.__remote_control)

    def on_startup(self):
        """Called once at the beginning, before main().
        Use this method to create your things, rebind connections, setup hardware, etc.
        """
        print("Started. Press CTRL+C to end")





        self.__thing = self.client.create_thing('weather_follower_thing')
        # self.__remote_control = self.__thing.follow(('follower_basic', 'follow_basic_control'))
        self.__remote_control = None
        self.Point = None
        self.__guid_resources = (self.__thing, self.Point, self.follow_remote_feed, self.__remote_control)
        # self.follow_feed_callback()remote_feed = self.__thing.follow(remote_feed_gpid, self.follow_feed_callback)
        print("About my Thing")
        print("My Thing object:", self.__thing)
        print("My Thing local ID (lid):", self.__thing.lid)
        print("My Thing globally unique ID (guid):", self.__thing.guid)

        remote_feed = self.__thing.follow(('share_weather', 'share_weather_feed'),
                                          callback_parsed=self.__callback_parsed)
        self.__fetch_recent(remote_feed)

        publish = self.find_nearest_weather()
        print(publish)

    @staticmethod
    def __callback_parsed(args):
        logger.debug("Feed data received. Shared at %s", args['time'])

        values = args['parsed'].filter_by(types=(Datatypes.INTEGER,), units=(Units.COUNTS_PER_MIN,), text=("random",))
        if values:
            logger.debug('Found parsed data for key %s: value: %s', values[0].label, values[0].value)
        else:
            logger.debug('Parsed data not found')

    @staticmethod
    def __callback_recent(args):
        logger.debug("Recent data received. Shared at %s", args['time'])

        # at the moment, recent data isn't parsed to extract metadata for values so we have to use fixed keys
        try:
            logger.debug('Found recent data for key %s: value: %s', 'count', args['data']['count'])
        except KeyError as exc:
            logger.warning('Failed to find key %s in recent data %s', exc, args)
            raise

    def __fetch_recent(self, remote_point):
        # retrieve all samples, max 99 will likely be floored to container max
        samples = remote_point.get_recent(99)

        for sample in samples:
            self.__callback_recent(sample)

    def find_nearest_weather(self):
        print("finding nearest weather")
        guid = self.search_reduced()
        print("printing search data", guid)
        gpid_data = self.describe(guid_or_resource=guid)
        print("printing describe data", gpid_data)
        print(gpid_data)

    def search_reduced(self, text="Weather", lang="en", unit=None, limit=100, offset=0, local=None,
                       scope=SearchScope.PUBLIC):
        """Shorthand for [search()](#IoticAgent.IOT.Client.Client.search) with `reduced=True`"""
        location = {'lat': 52.427809, 'long': -0.327829, 'radius': 1.789}
        return self.client.search(text, lang, location, unit, limit, offset, reduced=True, local=local, scope=scope)

    #  __guid_resources = (Thing, Point, RemoteFeed, RemoteControl)

    def describe(self, guid_or_resource, lang="en", local=None, scope=DescribeScope.AUTO):
        if isinstance(guid_or_resource, self.__guid_resources):
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
        print("Remote Feed subscription object:", remote_feed)
        # List and print subscriptions (Feeds following or Controls attached to)
        # Note:
        # In sub_list, 'id' is the Feed/Control global point ID (gpid)
        sub_list = my_thing.list_connections()
        print("Subscription list: ", sub_list)
        return sub_list

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
    #

    def follow_feed_callback(self, args):
        print("Printing Weather data received from followed Feed")

        # Tells your Thing what to do with data received from the Feed you are following
        # Print data recieved from followed feed
        print("This is the Feed Callback with Weather data:", args['data'])

    # def unfollow(self):
    #
    #
    #
    def main(self):
        """Called after on_startup.
        Use this method for your main loop (we don't need one here).
        Set self.LOOP_TIMER for your regular tick
        """
        while True:
            start = monotonic()
            # loop code in here
            stop = monotonic()
            if self.wait_for_shutdown(max(0, self.LOOP_TIMER - (stop - start))):
                break


def main():
    SysthesiserWeather(config="test.ini").run()


if __name__ == '__main__':
    main()

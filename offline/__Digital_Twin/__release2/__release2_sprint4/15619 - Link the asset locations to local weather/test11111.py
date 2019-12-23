from IoticAgent.Core.compat import monotonic
from IoticAgent.ThingRunner import RetryingThingRunner
from IoticAgent import Datatypes, Units
from IoticAgent.Core.Const import SearchScope, DescribeScope
from IoticAgent.IOT.utils import uuid_to_hex, logger
from markupsafe import string_types


class SysthesiserWeather(RetryingThingRunner):

    LOOP_TIMER = 10  # minimum number of seconds duration of the main loop

    def __init__(self, config=None):
        """Instantiation code in here, after the call to super().__init__()
        """
        super(SysthesiserWeather, self).__init__(config=config)
        self.__thing = None

    def on_startup(self):
        """Called once at the beginning, before main().
        Use this method to create your things, rebind connections, setup hardware, etc.
        """
        print("Started. Press CTRL+C to end")

        self.__thing = self.client.create_thing('weather_follower_thing')
        print("About my Thing")
        print("My Thing object:", self.__thing)
        print("My Thing local ID (lid):", self.__thing.lid)
        print("My Thing globally unique ID (guid):", self.__thing.guid)
        # remote_feed = self.__thing.follow(('share_weather', 'share_weather_feed'), callback_parsed=self.__callback_parsed)
        # # Let's have a look at it
        # print("Remote Feed subscription object:", remote_feed)
        # # List and print subscriptions (Feeds following or Controls attached to)
        # # Note:
        # # In sub_list, 'id' is the Feed/Control global point ID (gpid)
        # sub_list = self.__thing.list_connections()
        # print("Subscription list: ", sub_list)
        #
        # self.__fetch_recent(remote_feed)
        self.find_nearest_weather()

    @staticmethod
    def __callback_parsed(args):
        logger.debug("Feed data received. Shared at %s", args['time'])

        values = args['parsed'].filter_by(types=(Datatypes.INTEGER,), units=(Units.COUNTS_PER_MIN,), text=("random",))
        if values:
            logger.debug('Found parsed data for key %s: value: %s', values[0].label, values[0].value)
        else:
            logger.debug('Parsed data not found')

    def find_nearest_weather(self):
        print("finding nearest weather")
        search_data = self.search_reduced()
        print("printing search_data: ", search_data)
        gpid = search_data[self.__thing.guid]["points"]
        print("printing gpid: ", gpid)


        # remote_feed = self.__thing.follow(('share_weather', 'share_weather_feed'),
        #                                   callback_parsed=self.__callback_parsed)
        # self.__fetch_recent(remote_feed)

    def search_reduced(self, text="Weather", lang="en", unit=None, limit=100, offset=0, local=None,
                       scope=SearchScope.PUBLIC):
        """Shorthand for [search()](#IoticAgent.IOT.Client.Client.search) with `reduced=True`"""
        location = {'lat': 52.427809, 'long': -0.327829, 'radius': 2.789}
        return self.client.search(text, lang, location, unit, limit, offset, reduced=True, local=local, scope=scope)

    def __fetch_recent(self, remote_point):
        # retrieve all samples, max 99 will likely be floored to container max
        samples = remote_point.get_recent(10)

        for sample in samples:
            self.__callback_recent(sample)

    # __guid_resources = (Thing, Point, RemoteFeed, RemoteControl)

    def describe(self, guid_or_resource, lang=None, local=None, scope=DescribeScope.AUTO):
        """Describe returns the public (or local) description of a Thing or Point

        Returns the description dict (see below for Thing example) if available, otherwise `None`

            #!python
            {
                "type": "Entity",
                "meta": {
                    "long": 0.716356,
                    "lat": 52.244384,
                    "label": "Weather Station #1",
                    "parent": "3bbf307b43b1460289fe707619dece3d",
                    "points": [
                        {
                            "type": "Control",
                            "label": "Control 101",
                            "guid": "fb1a4a4dbb2642ab9f836892da93c101",
                            "storesRecent": false
                        },
                        {
                            "type": "Feed",
                            "label": "My weather feed",
                            "guid": "fb1a4a4dbb2642ab9f836892da93f101",
                            "storesRecent": true
                        }
                    ],
                    "comment": "A lovely weather station...",
                    "tags": [
                        "blue",
                        "garden"
                    ]
                }
            }

        Raises [IOTException](./Exceptions.m.html#IoticAgent.IOT.Exceptions.IOTException)
        containing the error if the infrastructure detects a problem

        Raises [LinkException](../Core/AmqpLink.m.html#IoticAgent.Core.AmqpLink.LinkException)
        if there is a communications problem between you and the infrastructure

        `guid_or_resource` (mandatory) (string or object).
        If a `string`, it should contain the globally unique id of the resource you want to describe in 8-4-4-4-12
        (or undashed) format.
        If an `object`, it should be an instance of Thing, Point, RemoteFeed or RemoteControl.  The system will return
        you the description of that object.

        `lang` (optional) (string) The two-character ISO 639-1 language code for which labels and comments will be
        returned. This does not affect Values (i.e. when describing a Point, apart from value comments) and tags as
        these are language neutral).

        `local` (optional) (boolean) **Deprecated**, use `scope` instead. If `true`, lookup metadata at container level.
        Check the local_meta flag to determine whether local metadata functionality is available. (Takes precedence over
        `scope`.)

        `scope` (optional) ([DescribeScope](../Core/Const.m.html#IoticAgent.Core.Const.DescribeScope)) Whether to
        perform PUBLIC, LOCAL (container level) or LOCAL_OWN (container level restricted to own things) metadata lookup.
        Check the [local_meta](#IoticAgent.IOT.Client.Client.local_meta) flag to determine whether local metadata
        functionality is available. (Note that AUTO, PUBLIC and LOCAL_OWN scopes are always available.). AUTO mode
        first attempts to look up private metadata, then public.
        """
        if isinstance(guid_or_resource, self.__guid_resources):
            guid = guid_or_resource.guid
        elif isinstance(guid_or_resource, string_types):
            guid = uuid_to_hex(guid_or_resource)
        else:
            raise ValueError("describe requires guid string or Thing, Point, RemoteFeed or RemoteControl instance")
        logger.info('describe() [guid="%s"]', guid)

        evt = self._request_describe(guid, lang, local, scope)

        self._wait_and_except_if_failed(evt)
        return evt.payload['result']

    @staticmethod
    def __callback_recent(args):
        logger.debug("Recent data received. Shared at %s", args['time'])

        # at the moment, recent data isn't parsed to extract metadata for values so we have to use fixed keys
        try:
            logger.debug('Found recent data for key %s: value: %s', 'count', args['data']['count'])
        except KeyError as exc:
            logger.warning('Failed to find key %s in recent data %s', exc, args)
            raise

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

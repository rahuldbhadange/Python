from time import sleep
from IoticAgent.Core.compat import monotonic
from IoticAgent.ThingRunner import RetryingThingRunner
from IoticAgent.IOT.utils import logger
from json import dumps


def pretty_print(msg, data):
    print(msg, dumps(data, indent=4))


class RetryingSysthesiserWeather(RetryingThingRunner):

    LOOP_TIMER = 10  # minimum number of seconds duration of the main loop

    def __init__(self, config=None):
        """Instantiation code in here, after the call to super().__init__()
        """
        super(RetryingSysthesiserWeather, self).__init__(config=config)


class SysthesiserWeatherData(RetryingSysthesiserWeather):

    def __validate_weather_type(self, thing_data_label, point_data_label):

        if thing_data_label.startswith("Weather Forecast for: ") and point_data_label == "Current weather info":
            print(" Welcome to Metoffice Forecast")
            return "metoffice forecast"
        elif thing_data_label.startswith("Weather Observation for: ") and point_data_label == "Observation info":
            print("Welcome to Metoffice Observation")
            return "metoffice observation"
        return None

    def on_startup(self, results=None):
        """Called once at the beginning, before main().
        Use this method to create your things, rebind connections, setup hardware, etc.
        """
        __thing = self.client.create_thing('My_SysthesiserWeather_Thing')
        location = {'lat': 52.427809, 'long': -0.327829, 'radius': 1.0}

        while not results:
            results = self.client.search(text="weather", location=location, limit=1)
            pretty_print("results", results)

            for thing_guid, thing_data in results.items():
                pretty_print("thing_guid", thing_guid)
                pretty_print("thing_data", thing_data)
                pretty_print("thing_data_label", thing_data['label'])
                thing_data_label = thing_data['label']

                for point_guid, point_data in thing_data['points'].items():
                    pretty_print("point_guid", point_guid)
                    pretty_print("point_data", point_data)
                    pretty_print("point_data_label", point_data['label'])
                    point_data_label = point_data['label']

                    descr = self.client.describe(point_guid)
                    pretty_print("descr", descr)

                    if descr and self.__validate_weather_type(thing_data_label, point_data_label):
                        remotefeed = __thing.follow(point_guid)
                        samples = remotefeed.get_recent(99)

                        for sample in samples:
                            recent_weather_to_publish = self.__callback_recent(sample)
                            pretty_print("Today's Forecast is : ", recent_weather_to_publish)

            location["radius"] += 0.5

    @staticmethod
    def __callback_recent(args):
        logger.debug("Recent data received. Shared at %s", args['time'])
        # at the moment, recent data isn't parsed to extract metadata for values so we have to use fixed keys

        try:
            logger.debug('Found recent data for key %s: value: %s', args['data'])
            recent_weather_to_publish = args['data']
        except KeyError as exc:
            logger.warning('Failed to find key %s in recent data %s', exc, args)
        return recent_weather_to_publish

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
    SysthesiserWeatherData(config="test.ini").run()

    try:
        while True:
            print("Press ctrl+C to end")
            # Runner-unrelated action goes here
            sleep(10)
    except KeyboardInterrupt:
        pass
    finally:
        SysthesiserWeatherData.stop()
    logger.info('Ended')


if __name__ == '__main__':
    main()

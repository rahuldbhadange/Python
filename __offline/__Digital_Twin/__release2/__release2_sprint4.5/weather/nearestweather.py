from json import dumps
import logging
from IoticAgent.Units import CELSIUS
from datetime import datetime

log = logging.getLogger(__name__)


def pretty_print(msg, data):
    print(msg, dumps(data, indent=4))


class NearestWeather:
    """ NearestWeather initializing """
    def __init__(self, client):
        self.client = client

    def find_nearest_weather(self, location={'lat': 52.427809, 'long': -0.327829}):   # location={'lat': 52.427809, 'long': -0.327829}
        """finding nearest weather"""
        thing = self.client.create_thing('My_SysthesiserWeather_Thing')

        radius_increment = 0.5
        location['radius'] = radius_increment

        results = None
        try:
            while not results:
                results = self.client.search(text="weather", location=location, unit=CELSIUS, limit=1)

                if results:
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

                            __descr = self.client.describe(point_guid)
                            pretty_print("descr", __descr)
                            __validate = self.__validate_weather_type(thing_data_label, point_data_label)
                            if __descr and __validate:
                                remotefeed = thing.follow(point_guid)
                                samples = remotefeed.get_recent(1)
                                # pretty_print("samples", samples)

                                try:
                                    for sample in samples:
                                        __recent_weather_to_publish = self.__process_data(sample)

                                    thing.unfollow(remotefeed.subid)
                                    __label = thing_data_label.strip('Weather Forecast for:')
                                    __recent_weather_to_publish['WeatherStation'] = __label
                                    __recent_weather_to_publish["WeatherType"] = __validate
                                    __recent_weather_to_publish["WeatherProvider"] = __label
                                    __recent_weather_to_publish["Location"] = str(location)

                                    # pretty_print("would send WeatherInfoSet event", __recent_weather_to_publish)
                                    return __recent_weather_to_publish
                                except UnboundLocalError as ex:
                                    print("UnboundLocalError : %s", ex)
                                    pass

                location["radius"] += radius_increment
        except ValueError as ex:
            log.error("Failed to find nearest weather: %s", ex)

    @staticmethod
    def __validate_weather_type(thing_data_label, point_data_label):
        """ validating weather type """
        if thing_data_label.startswith("Weather Forecast for: ") and point_data_label == "Current weather info":
            return "metoffice forecast"
        elif thing_data_label.startswith("Weather Observation for: ") and point_data_label == "Observation info":
            return "metoffice observation"
        return None

    @staticmethod
    def __process_data(args):
        """ Processing data"""
        log.debug("Recent data received. Shared at %s", args['time'])
        # at the moment, recent data isn't parsed to extract metadata for values so we have to use fixed keys
        try:
            log.debug('Found recent data for value: %s', args['data'])
            __recent_weather_to_publish = args['data']

            name_map = {"time": "WeatherTime", "feels": "FeelsLikeTemperature", "gust": "WindGust", "humid": "Humidity",
                        "temp": "Temperature", "visib": "Visibility", "winddir": "WindDirection",
                        "windspd": "WindSpeed", "uv": "MaxUVIndex", "type": "WeatherType",
                        "prob": "PrecipitationProbability"}
            __recent_weather_to_publish = dict((name_map[name], val) for name, val in __recent_weather_to_publish.items())

            WeaTme = {"WeatherTime": str(datetime.utcnow())}

            __recent_weather_to_publish.update(WeaTme)

        except KeyError as exc:
            log.error('Failed to find key %s in recent data %s', exc, args)
        except:
            log.error("Some exception in __process_data", exc_info=False)  # TODO: set True to debug
        return __recent_weather_to_publish

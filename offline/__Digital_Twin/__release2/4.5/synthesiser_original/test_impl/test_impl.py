from pprint import pformat
from time import sleep
from IoticAgent.Core.compat import monotonic
from IoticAgent import ThingRunner
from IoticAgent.IOT.utils import logger
from json import dumps
import logging
from ioticlabs.dt.api.integrator import Integrator, IntegratorCallbacks
from ioticlabs.dt.api.follower import (
     Follower, FollowerCallbacks, NamedEventMixin, T2ResponseException, AssetUnknown, T2ReqFailureReason, T2Unavailable,
     T2Timeout)

log = logging.getLogger(__name__)

def pretty_print(msg, data):
    print(msg, dumps(data, indent=4))


class NearestWeather:

    def __init__(self, client):
        self.client = client

    def __validate_weather_type(self, thing_data_label, point_data_label):
        if thing_data_label.startswith("Weather Forecast for: ") and point_data_label == "Current weather info":
            return "metoffice forecast"
        elif thing_data_label.startswith("Weather Observation for: ") and point_data_label == "Observation info":
            return "metoffice observation"
        return None

    def find_nearest_weather(self, location={'lat': 52.427809, 'long': -0.327829}):
        thing = self.client.create_thing('My_SysthesiserWeather_Thing')
        radius_increment = 0.5
        location['radius'] = radius_increment

        results = None
        while not results:
            results = self.client.search(text="weather", location=location, limit=1)
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

                    descr = self.client.describe(point_guid)
                    pretty_print("descr", descr)

                    if descr and self.__validate_weather_type(thing_data_label, point_data_label):
                        remotefeed = thing.follow(point_guid)
                        samples = remotefeed.get_recent(99)

                        for sample in samples:
                            recent_weather_to_publish = self.__callback_recent(sample)
                            pretty_print("Today's Forecast is : ", recent_weather_to_publish)

                        thing.unfollow(remotefeed.subid)
                        recent_weather_to_publish['label'] = thing_data['label']
                        return recent_weather_to_publish

            location["radius"] += radius_increment

    @staticmethod
    def __callback_recent(args):
        log.debug("Recent data received. Shared at %s", args['time'])
        # at the moment, recent data isn't parsed to extract metadata for values so we have to use fixed keys

        try:
            log.debug('Found recent data for key %s: value: %s', args['data'])
            recent_weather_to_publish = args['data']
        except KeyError as exc:
            log.warning('Failed to find key %s in recent data %s', exc, args)
        except:
            log.error("Some exception in __callback_recent", exc_info=False)  # TODO: set True to debug
        return recent_weather_to_publish


class IntegratorHelper(IntegratorCallbacks):

    def __init__(self, config, client):
        self.__integrator = Integrator(config, client, self)

    def start(self):
        self.__integrator.start()

    def stop(self):
        self.__integrator.stop()

    def publish_event(self, event):
        self.__integrator.publish_event(event)

    # IntegratorCallbacks
    def on_asset_created(self, asset_id):
        log.debug('IntegratorCallbacks Asset created: %s', asset_id)

    # IntegratorCallbacks
    def on_asset_deleted(self, asset_id):
        log.debug('IntegratorCallbacks Asset deleted: %s', asset_id)

    # IntegratorCallbacks
    def on_t2_request(self, request):
        pass


class SynthesiserWeather(NamedEventMixin, FollowerCallbacks, ThingRunner):
    def __init__(self, config, agent_config_str):
        self.__follower = Follower(config['follower'], self.client, self)
        self.__assets = set()
        self.__integrator = IntegratorHelper(config['integrator'], self.client)

    def on_startup(self):
        log.debug('Startup')
        self.__follower.start()
        self.__integrator.start()

    def main(self):
        log.debug('Running')

    def on_shutdown(self, exc_info):
        log.debug('Shutdown')
        self.__follower.stop()
        self.__integrator.stop()

    # for FollowerCallbacks
    def on_asset_created(self, asset_id):
        self.__assets.remove(asset_id)

    # For NamedEventMixin (specific event)
    def do_bombuiltset(self, event):
        log.info('[%s] #%d BoM-as-built (from %s) @ %s (sys: %s)\n%s', event.asset, event.offset, event.source,
        event.time, event.systime, pformat(event.data))

    def do_fielddatasuccessset(self, event):
        self.__handle_fielddatasuccessset(event)
        print("*" * 80)
        print(event.name().lower())
        print(event.version)
        print(event.data)
        self.__follower.ack_event(event)

    def on_FieldDataSuccessSet(self, event):

        if event.version >= 1:
        # Note: Events > 1 will have Location in the event.data
            try:
                nw = NearestWeather(self.client)
                print("weather data", nw.find_nearest_weather())
            except:
                log.error("Exception.", exc_info=True)

        self.__follower.ack_event(event)
            # Note: self.__integrator.publish_event(WeatherSetInfo(
        print("*" * 80)

# for NamedEventMixin (all events for which there isn't a do_ method)
#











#
#
#
#
#
#
#
#
# class SynthesiserWeather(NamedEventMixin, FollowerCallbacks, ThingRunner):
#     self.__assets.remove(asset_id)
#
#
#
#
#     def main(self):
#         """Called after on_startup.
#         Use this method for your main loop (we don't need one here).
#         Set self.LOOP_TIMER for your regular tick
#         """
#
#         while True:
#             start = monotonic()
#             # loop code in here
#             stop = monotonic()
#             if self.wait_for_shutdown(max(0, self.LOOP_TIMER - (stop - start))):
#                 break
#

def main():
    SynthesiserWeather(config="test.ini").run()

    try:
        while True:
            print("Press ctrl+C to end")
            # Runner-unrelated action goes here
            sleep(10)
    except KeyboardInterrupt:
        pass
    finally:
        SynthesiserWeather.stop()
    logger.info('Ended')


if __name__ == '__main__':
    main()

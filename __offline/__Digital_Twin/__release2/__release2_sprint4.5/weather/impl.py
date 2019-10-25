from datetime import datetime
from json import dumps
from pprint import pformat
from IoticAgent import ThingRunner
import logging
from ioticlabs.dt.api.follower import Follower, FollowerCallbacks, NamedEventMixin
from ioticlabs.dt.api.integrator import Integrator, IntegratorCallbacks, EventPublishFailure, AssetUnknown
from .nearestweather import NearestWeather
from rrps.dt.events import WeatherInfoSet

log = logging.getLogger(__name__)


def pretty_print(msg, data):
    print(msg, dumps(data, indent=4))


class IntegratorCB(IntegratorCallbacks):

    def __init__(self, config, client):
        self.__integrator = Integrator(config, client, self)
        self.__assets = set()

    def start(self):
        self.__integrator.start()

    def stop(self):
        self.__integrator.stop()

    def publish_event(self, event):
        self.__integrator.publish_event(event)

    # for IntegratorCallbacks
    def on_asset_created(self, asset_id):
        log.critical('IntegratorCallbacks Asset created: %s', asset_id)

    # for IntegratorCallbacks
    def on_asset_deleted(self, asset_id):
        log.critical('IntegratorCallbacks Asset deleted: %s', asset_id)

    # for IntegratorCallbacks
    def on_t2_request(self, request):
        pass


class SynthesiserWeather(NamedEventMixin, FollowerCallbacks, ThingRunner):

    def __init__(self, config, agent_config):
        super().__init__(config=agent_config)

        self.__follower = Follower(config['follower'], self.client, self)
        self.__assets = set()

        # self.__int_cb = IntegratorCB()
        # self.__integrator = Integrator(config['integrator'], self.client, self.__int_cb)
        self.__integrator = IntegratorCB(config['integrator'], self.client)

    def on_startup(self):
        log.debug('Startup')
        self.__follower.start()
        self.__integrator.start()

    def main(self):
        # Wait for an asset to exist from time import sleep
        while True:
            try:
                self.__assets.pop()
            except KeyError as ex:
                print(ex)
                pass
            else:
                break

        try:
            # __near_wea = NearestWeather(self.client)
            # __weather_data = __near_wea.find_nearest_weather()
            # pretty_print("would send WeatherInfoSet event", __weather_data)
            #
            # Time = datetime.now()
            # asset = self.__assets.pop()
            #
            #
            # # self.__integrator.publish_event(asset, time=Time, data=__event_object)
            # print("hi " * 10)
            # self.__integrator.publish_event(WeatherInfoSet(asset, time=Time, data=__weather_data))
            # # self.__integrator.publish_event(event)
            # print("bye " * 10)
            while not self.wait_for_shutdown(100):
                log.debug('Running')
        except KeyboardInterrupt:
            print("not passed")

    def on_shutdown(self, exc_info):
        log.debug('Shutdown')
        self.__integrator.stop()
        self.__follower.stop()

    # for FollowerCallbacks
    def on_asset_created(self, asset_id):
        log.info('Follower Callbacks Asset created: %s', asset_id)
        self.__assets.add(asset_id)

    # for FollowerCallbacks
    def on_asset_deleted(self, asset_id):
        log.info('Follower Callbacks Asset deleted: %s', asset_id)
        self.__assets.remove(asset_id)

    def do_fielddatasuccessset(self, event):

        log.info('[%s] #%d FieldData-Success-Set (from %s) @ %s (sys: %s)\n%s', event.asset, event.offset, event.source,
                 event.time, event.systime, pformat(event.data))

        # Indicate that event has been processed. If asset has been deleted in the mean time, this will be a no-op.
        self.__follower.ack_event(event)

        print("_#-" * 30)
        print(event.name().lower())
        print(event.version)
        print(event.data)
        __location = event.data["Location"]
        name_map = {"Latitude": "lat", "Longitude": "long"}
        __location = dict((name_map[name], val) for name, val in __location.items())
        try:
            __near_wea = NearestWeather(self.client)
            __weather_data = __near_wea.find_nearest_weather(__location)
            pretty_print("would send WeatherInfoSet event", __weather_data)
            asset = self.__assets.pop()
            Time = datetime.utcnow()
            print(" $ " * 10)
            self.__integrator.publish_event(WeatherInfoSet(asset, time=Time, data=__weather_data))
            print(" % " * 10)
        except ValueError:
            log.error("Exception.", exc_info=True)
        except KeyboardInterrupt:
            pass

    # def on_event_unmatched(self, event):
    #     log.info('[%s] #%d %s (from %s) @ %s (sys: %s)\n%s', event.asset, event.offset, event.name(), event.source,
    #         event.time, event.systime, pformat(event.data))
    #
    #     # Indicate that event has been processed. If asset has been deleted in the mean time, this will be a no-op.
    #     self.__follower.ack_event(event)

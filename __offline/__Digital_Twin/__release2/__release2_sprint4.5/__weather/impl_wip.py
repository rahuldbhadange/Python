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
    # for IntegratorCallbacks
    def on_asset_created(self, asset_id):
        log.debug('IntegratorCallbacks Asset created: %s', asset_id)

    # for IntegratorCallbacks
    def on_asset_deleted(self, asset_id):
        log.debug('IntegratorCallbacks Asset deleted: %s', asset_id)

    # for IntegratorCallbacks
    def on_t2_request(self, request):
        pass


class SynthesiserWeather(NamedEventMixin, FollowerCallbacks, ThingRunner):

    def __init__(self, config, agent_config):
        super().__init__(config=agent_config)

        self.__follower = Follower(config['follower'], self.client, self)
        self.__assets = set()

        self.__int_cb = IntegratorCB()
        self.__integrator = Integrator(config['integrator'], self.client, self.__int_cb)

    def on_startup(self):
        log.debug('Startup')
        self.__follower.start()
        self.__integrator.start()

    def main(self):
        try:
            # __near_wea = NearestWeather(self.client)
            # __weather_event = __near_wea.find_nearest_weather()
            # pretty_print("would send WeatherInfoSet event", __weather_event)

            # Time = datetime.now()
            # asset = "1000021    "
            # event = WeatherInfoSet(asset)
            # WeatherInfoSet = nw.find_nearest_weather()

            # self.__integrator.publish_event(asset, time=Time, data=__event_object)
            # self.__integrator.publish_event(WeatherInfoSet(asset, time=Time, data=__weather_event))
            # self.__integrator.publish_event(event)

            while not self.wait_for_shutdown(50):
                log.debug('Running')
        except KeyboardInterrupt:
            print("g")

    # def __publish_success(self, asset):
    #     event = WeatherInfoSet(asset)
    #
    #     while True:
    #         # Try to publish the event until it succeed
    #         try:
    #             self.__integrator.publish_event(event)
    #         except EventPublishFailure as ex:
    #             log.error('Event Publish Failure: %s', ex)
    #         except AssetUnknown:
    #             break
    #         else:
    #             log.debug('Published success event: %s Asset: %s', event, asset)
    #             # Save in cache
    #             # self.__remember_fname(self.__get_fname_from_blobname(blobname))
    #             break

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

    # For NamedEventMixin (specific event)
    def do_bombuiltset(self, event):
        log.info('[%s] #%d BoM-as-built (from %s) @ %s (sys: %s)\n%s', event.asset, event.offset, event.source,
        event.time, event.systime, pformat(event.data))

        # Indicate that event has been processed. If asset has been deleted in the mean time, this will be a no-op.
        self.__follower.ack_event(event)

    def do_fielddatasuccessset(self, event):

        log.info('[%s] #%d FieldData-Success-Set (from %s) @ %s (sys: %s)\n%s', event.asset, event.offset, event.source,
                 event.time, event.systime, pformat(event.data))

        # Indicate that event has been processed. If asset has been deleted in the mean time, this will be a no-op.
        # self.__follower.ack_event(event)

        print("_#-" * 30)
        print(event.name().lower())
        print(event.version)
        print(event.data)
        __location = event.data["Location"]
        name_map = {"Latitude": "lat", "Longitude": "long"}
        __location = dict((name_map[name], val) for name, val in __location.items())
        try:
            __near_wea = NearestWeather(self.client)
            # __near_wea.find_nearest_weather(__location)
            __weather_data = __near_wea.find_nearest_weather(__location)
            pretty_print("would send WeatherInfoSet event", __weather_data)
            asset = self.__assets.pop()
            Time = datetime.utcnow()
            self.__integrator.publish_event(WeatherInfoSet(asset, time=Time, data=__weather_data))
        except ValueError:
            log.error("Exception.", exc_info=True)
        except KeyboardInterrupt:
            pass

    # def on_fielddatasuccessset(self, event):
    #
    #     log.debug('[%s] #%d %s (from %s) @ %s (sys: %s)\n%s', event.asset, event.offset, event.name(), event.source,
    #              event.time, event.systime, pformat(event.data))
    #
    #     # Indicate that event has been processed. If asset has been deleted in the mean time, this will be a no-op.
    #     self.__follower.ack_event(event)
    #
    #     print("-%*" * 30)
    #     try:
    #         __near_wea = NearestWeather(self.client)
    #         __weather_event = __near_wea.find_nearest_weather()
    #         pretty_print("would send WeatherInfoSet event", __weather_event)
    #     except ValueError:
    #         log.error("Exception.", exc_info=True)
    #     except KeyboardInterrupt:
    #         pass
    #
    #     try:
    #         self.__integrator.publish_event(event)
    #     except EventPublishFailure as ex:
    #         log.error('Event Publish Failure: %s', ex)

    # def on_event_unmatched(self, event):
    #     log.info('[%s] #%d %s (from %s) @ %s (sys: %s)\n%s', event.asset, event.offset, event.name(), event.source,
    #         event.time, event.systime, pformat(event.data))
    #
    #     # Indicate that event has been processed. If asset has been deleted in the mean time, this will be a no-op.
    #     self.__follower.ack_event(event)

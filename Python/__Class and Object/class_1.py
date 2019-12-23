print("\n", "*_*-" * 15)


class IntegratorCB:
    # for IntegratorCallbacks
    # @staticmethod
    def on_asset_created(self):
        print('IntegratorCallbacks Asset created')

    # for IntegratorCallbacks
    # @staticmethod
    def on_asset_deleted(self):
        print('IntegratorCallbacks Asset deleted')


class SynthesiserWeather(IntegratorCB):
    def __init__(self):
        self.IntegratorCB = IntegratorCB
        print('self.IntegratorCB: ', hex(id(self.IntegratorCB)))
        

SynthesiserWeather = SynthesiserWeather()
print('SynthesiserWeather: ', SynthesiserWeather)
SynthesiserWeather.on_asset_created()
SynthesiserWeather.on_asset_deleted()



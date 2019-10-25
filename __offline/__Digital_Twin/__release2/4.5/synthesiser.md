# DT Synthesiser Development

This is a quick guide to the development of digital twin synthesisers.  A synthesiser is both a follower and integrator.  A typical use case could be following the twin, following data from Iotic Space and publishing new events.

## How to

Starting from a follower (eg. acmecorp.dt.follower.example).

1. Create package
- Copy/Rename to acmecorp.dt.synthesiser.example.
- Rename directory acmecorp/dt/follower to synthesiser
- Edit setup.py to change package name and entry_points
- Rename cfg/follower.cfg.yml to cfg/synthesiser.cfg.yml

2. Add integrator config
- Copy the reference integrator section from acmecorp.dt.integrator.example/cfg/integrator.cfg.yml into synthesiser.cfg.yml

3. Add IntegratorHelper to impl.py
The IntegratorCallbacks and FollowerCallbacks share the same names so cannot exist in the same class.  To work around this we'll use the FollowerCallbacks to keep track of digital twin assets and we'll just deubg log the IntegratorCallbacks.

- Add import

```python
from ioticlabs.dt.api.integrator import Integrator, IntegratorCallbacks
```

- Minimal implementation of IntegratorCallbacks exposes start,stop and publish_event. 

```python
class IntegratorHelper(IntegratorCallbacks):

    def __init__(self, config, client):
        self.__integrator = Integrator(config, client, self)

    def start(self):
        self.__integrator.start()

    def stop(self):
        self.__integrator.stop()

    def publish_event(self, event):
        self.__integrator.publish_event(event)

    def on_asset_created(self, asset_id):
        log.debug('IntegratorCallbacks Asset created: %s', asset_id)

    def on_asset_deleted(self, asset_id):
        log.debug('IntegratorCallbacks Asset deleted: %s', asset_id)

    def on_t2_request(self, request):
        pass
```

- Add to follower __init__ function

```python
self.__integrator = IntegratorHelper(config['integrator'], self.client)
```

- Add integrator start/stop to the on_startup and on_shutdown functions

```python
def on_startup(self):
    log.debug('Startup')
    self.__follower.start()
    self.__integrator.start()

def on_shutdown(self, exc_info):
    log.debug('Shutdown')
    self.__follower.stop()
    self.__integrator.stop()
```

- Now events can be published from the Follower using the exposed publish_event function.

```python
self.__integrator.publish_event(AnotherEvent(asset, time=time))
```


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
    # self.__guid_resources = (self.__thing, self.Point, self.follow_remote_feed, self.__remote_control)
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

    __guid_resources = (Thing, Point, self.remote_feed, RemoteControl)

    def find_nearest_weather(self):
        print("finding nearest weather")
        guid = self.search_reduced()
        print("printing search data", guid)
        gpid_data = self.describe(guid_or_resource=guid)
        print("printing describe data", gpid_data)
        print(gpid_data)
        remote_feed = self.__thing.follow(('share_weather', 'share_weather_feed'),
                                          callback_parsed=self.__callback_parsed)
        self.__fetch_recent(remote_feed)

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


def follow_feed_callback(self, args):
    print("Printing Weather data received from followed Feed")

    # Tells your Thing what to do with data received from the Feed you are following
    # Print data recieved from followed feed
    print("This is the Feed Callback with Weather data:", args['data'])

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
    return evt.payload['result']  # pylint: disable=unsubscriptable-object
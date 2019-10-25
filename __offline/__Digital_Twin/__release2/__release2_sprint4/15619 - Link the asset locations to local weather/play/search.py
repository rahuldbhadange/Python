def search(self, text=None, lang=None, location=None, unit=None, limit=50, offset=0, reduced=False, local=None,
           scope=SearchScope.PUBLIC):
    """Search the Iotic Space for public Things with metadata matching the search parameters:
    text, lang(uage), location, unit, limit, offset. Note that only things which have at least one point defined can
    be found.
    Returns dict of results as below (first with reduced=False, second with reduced=True)- OR -
        #!python
        # reduced=False returns dict similar to below
        {
            "2b2d8b068e404861b19f9e060877e002": {
                "long": -1.74803,
                "matches": 3.500,
                "lat": 52.4539,
                "label": "Weather Station #2",
                "owner": "3bbf307b43b1460289fe707619dece3d",
                "points": {
                    "a300cc90147f4e2990195639de0af201": {
                        "matches": 3.000,
                        "label": "Feed 201",
                        "type": "Feed",
                        "storesRecent": true
                    },
                    "a300cc90147f4e2990195639de0af202": {
                        "matches": 1.500,
                        "label": "Feed 202",
                        "type": "Feed",
                        "storesRecent": false
                    }
                }
            },
            "76a3b24b02d34f20b675257624b0e001": {
                "long": 0.716356,
                "matches": 2.000,
                "lat": 52.244384,
                "label": "Weather Station #1",
                "owner": "3bbf307b43b1460289fe707619dece3d",
                "points": {
                    "fb1a4a4dbb2642ab9f836892da93f101": {
                        "matches": 1.000,
                        "label": "My weather feed",
                        "type": "Feed",
                        "storesRecent": false
                    },
                    "fb1a4a4dbb2642ab9f836892da93c102": {
                        "matches": 1.000,
                        "label": None,
                        "type": "Control",
                        "storesRecent": false
                    }
                }
            }
        }
        # reduced=True returns dict similar to below
        {
            "2b2d8b068e404861b19f9e060877e002": {
                "a300cc90147f4e2990195639de0af201": "Feed",
                "a300cc90147f4e2990195639de0af202": "Feed"
            },
            "76a3b24b02d34f20b675257624b0e001": {
                "fb1a4a4dbb2642ab9f836892da93f101": "Feed",
                "fb1a4a4dbb2642ab9f836892da93f102": "Control"
            }
        }
    Raises [IOTException](./Exceptions.m.html#IoticAgent.IOT.Exceptions.IOTException)
    containing the error if the infrastructure detects a problem
    Raises [LinkException](../Core/AmqpLink.m.html#IoticAgent.Core.AmqpLink.LinkException)
    if there is a communications problem between you and the infrastructure
    `text` (optional) (string) The text to search for. Label and description will be searched
    for both Thing and Point and each word will be used as a tag search too. Text search is case-insensitive. Tag
    search is language neutral.
    `lang` (optional) (string) The two-character ISO 639-1 language code to search in, e.g. "en" "fr"
    Language is used to limit search to only labels and descriptions in that language. You will only get labels `in
    that language` back from search and then only if there are any in that language.
    `location` (optional) (dictionary) Latitude, longitude and radius to search within.
    All values are float, Radius is in kilometers (km). E.g. `{"lat"=1.2345, "long"=54.321, "radius"=6.789}`. Note:
    If `text` has not been specified, radius can at most be 25km.
    `unit` (optional) (string) Valid URL of a unit in an ontology.  Or use a constant from the
    [units](../Units.m.html#IoticAgent.Units) class - such as [METRE](../Units.m.html#IoticAgent.Units.METRE).
    `limit` (optional) (integer) Return this many search results.
    `offset` (optional) (integer) Return results starting at this offset - good for paging.
    `reduced` (optional) (boolean) If `true`, return the reduced results just containing points and
    their type.
    `local` (optional) (boolean) **Deprecated**, use `scope` instead. If `true`, perform search at container level.
    Check the local_meta flag to determine whether local metadata functionality is available. (Takes precedence over
    `scope`.)
    `scope` (optional) ([SearchScope](../Core/Const.m.html#IoticAgent.Core.Const.SearchScope)) Whether to perform
    PUBLIC, LOCAL (container level) or LOCAL_OWN (container level restricted to own things) search. Check the
    [local_meta](#IoticAgent.IOT.Client.Client.local_meta) flag to determine whether local metadata functionality is
    available. (Note that PUBLIC and LOCAL_OWN scopes are always available.)
    """
    logger.info("search(text=\"%s\", lang=\"%s\", location=\"%s\", unit=\"%s\", limit=%s, offset=%s, reduced=%s)",
                text, lang, location, unit, limit, offset, reduced)
    evt = self._request_search(text, lang, location, unit, limit, offset,
                               SearchType.REDUCED if reduced else SearchType.FULL, local, scope)
    self._wait_and_except_if_failed(evt)
    return evt.payload['result']  # pylint: disable=unsubscriptable-object

# -*- coding: utf-8 -*-
# Copyright (c) 2017 Iotic Labs Ltd. All rights reserved.

from __future__ import unicode_literals, print_function

from json import dumps

import logging
logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s] {%(threadName)s} %(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from IoticAgent.Core.compat import monotonic
from IoticAgent.ThingRunner import RetryingThingRunner


def pretty_print(msg, data):
    print(msg, dumps(data, indent=4))


class TemplateTR(RetryingThingRunner):
    LOOP_TIMER = 10  # minimum number of seconds duration of the main loop

    def __init__(self, config=None):
        """Instantiation code in here, after the call to super().__init__()
        """
        super(TemplateTR, self).__init__(config=config)

    def on_startup(self):
        """Called once at the beginning, before main().
        Use this method to create your things, rebind connections, setup hardware, etc.
        """
        results = self.client.search(text="weather", location={'lat': 52.427809, 'long': -0.327829, 'radius': 10.789}, limit=1)
        pretty_print("results", results)
        for thing_guid, thing_data in results.items():
            pretty_print("thing_guid", thing_guid)
            pretty_print("thing_data", thing_data)

            for point_guid, point_data in results.items():
                pretty_print("point_guid", point_guid)
                pretty_print("point_data", point_data)

                descr = self.client.describe(point_guid)
                pretty_print("descr", descr)

    def main(self):
        """Called after on_startup.
        Use this method for your main loop (if you need one).
        Set LOOP_TIMER for your regular tick
        """
        while True:
            start = monotonic()
            # loop code in here
            stop = monotonic()
            if self.wait_for_shutdown(max(0, self.LOOP_TIMER - (stop - start))):
                break


def main():
    TemplateTR(config="dev.ini").run()

if __name__ == '__main__':
    main()

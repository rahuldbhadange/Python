#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2016 Iotic Labs Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://github.com/Iotic-Labs/py-application-examples/blob/master/LICENSE
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# INFO-----------------------------------------------------------------------------------------------------------------

# 3.4_connect_thing_following_hardcoded.py 12/02/2016 Iotic Labs.
# Connects an already created virtual Thing, or creates a new one.
# Prints information about that Thing (Thing object, lid, guid).
# Gets and prints metadata (eg metadata added in the UI).
# Lists and prints tags (eg tags added in the UI).
# Follows a feed using a hard-coded global point id (gpid).

# PYTHON2 COMPATIBILITY -----------------------------------------------------------------------------------------------
from __future__ import unicode_literals, print_function  # pylint: disable=unused-import

# LOGGING -------------------------------------------------------------------------------------------------------------
# Logging set to only CRITICAL messages by default.  To see more, use logging.INFO, or to see loads, logging.DEBUG
import logging
logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)s [%(name)s] {%(threadName)s} %(message)s',
                    level=logging.CRITICAL)

# IMPORTS -------------------------------------------------------------------------------------------------------------
import time

# IOTIC AGENT IMPORTS -------------------------------------------------------------------------------------------------
from IoticAgent import IOT

# ---------------------------------------------------------------------------------------------------------------------


def connect_thing(client):
    print("Connecting My First Thing")

    # Create your Thing in this script
    # Note:
    #  Calling 'create_thing' will connect a your script to a virtual Thing if the Local id (lid) is already in use,
    #  if not it creates a new Thing with this lid.
    my_thing = client.create_thing('My_First_Thing')  # GIVE IT A NAME

    # Let's have a look at it
    # print some information about your Thing
    print("About my Thing")
    print("My Thing object:", my_thing)
    print("My Thing local ID (lid):", my_thing.lid)
    print("My Thing globally unique ID (guid):", my_thing.guid)

    return my_thing


def show_metadata(my_thing):
    print("My metadata (simplified)")

    # Get and print the metadata you set in the UI
    with my_thing.get_meta() as my_metadata:
        # get the label
        my_labels = my_metadata.get_labels()
        print("Returned labels:")
        print(my_labels)
        # get the description
        my_descriptions = my_metadata.get_descriptions()
        print("Returned descriptions:")
        print(my_descriptions)
        # get the location
        my_lat, my_lon = my_metadata.get_location()
        print("Returned location lat = %f & lon = %f" % (my_lat, my_lon))

        # List and print tags you set in the UI
        print("Tags")
        print("List of Tags for this Thing:")
        tag_list = my_thing.list_tag()
        print(tag_list)


def follow_remote_feed(my_thing):
    print("Following remote Feed")

    # Follow remote Feed using global Point ID of the feed you want to follow
    # Note:
    #  Calling 'follow' will return the subscription object regardless of whether it already existed
    remote_feed_gpid = '7106712cbf35ef86fc83041d19a9491c'  # ADD THE GLOBAL POINT ID OF ANY FEED YOU WANT TO FOLLOW

    remote_feed = my_thing.follow(remote_feed_gpid, follow_feed_callback)

    # Let's have a look at it
    print("Remote Feed subscription object:", remote_feed)
    # List and print subscriptions (Feeds following or Controls attached to)
    # Note:
    #  In sub_list, 'id' is the Feed/Control global point ID (gpid)
    sub_list = my_thing.list_connections()
    print("Subscription list: ", sub_list)


def follow_feed_callback(args):
    print("Printing data received from followed Feed")

    # Tells your Thing what to do with data received from the Feed you are following
    # Print data recieved from followed feed
    print("This is the Feed Callback with data:", args['data'])


# MAIN -------------------------------------------------------------------------------------------------------------------------------------

def main():
    with IOT.Client(config='My First Agent.ini') as client:  # ADD OWN CONFIG .ini HERE
        my_thing = connect_thing(client)
        follow_remote_feed(my_thing)
        while True:
            try:
                print("Main running, press ctrl+c to quit.")
                time.sleep(10)
            except KeyboardInterrupt:
                break


# RUN --------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()

# END --------------------------------------------------------------------------------------------------

import time
from IoticAgent.IOT import Client
# from IoticAgent.Core import Client


def main():
    with Client('test.ini') as client:
        create_thing(client)
        # guid_or_resource = self.search(reduced=False, scope=SearchScope.PUBLIC)
        # self.describe(guid_or_resource)
        # self.follow_remote_feed(my_thing)

        while True:
            try:
                print("Main running, press ctrl+c to quit.")
                time.sleep(10)
            except KeyboardInterrupt:
                break


def create_thing(client):
    print("Creating my Thing")

    # Create your Thing in this script
    # Note:
    #  Calling 'create_thing' will create a new Thing, unless the Thing local ID (lid) is already in use.
    #  If it is, it will connect your script to that Thing.
    my_thing = client.create_thing('My_Follower_Thing')  # GIVE IT A NAME

    # Let's have a look at it
    # print some information about your Thing
    print("About my Thing")
    print("My Thing object:", my_thing)
    print("My Thing local ID (lid):", my_thing.lid)
    print("My Thing globally unique ID (guid):", my_thing.guid)

    return my_thing


main()

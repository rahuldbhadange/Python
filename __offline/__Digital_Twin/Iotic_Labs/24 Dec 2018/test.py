# IMPORTS ---------------------------

import time

# IOTIC AGENT IMPORTS -------------------------------------

from IoticAgent import IOT
from IoticAgent.Core.Const import R_FEED

# -------------------------

def connect_thing(client):
    print("Connecting First Iotic Thing")

    # CREATE THING ----------------------------
    # Note: Calling 'create_thing' connects your script to a virtual Thing if the Local ID (lid) is already in use. If not it creates a new Thing with this lid.
    my_thing = client.create_thing('First_Iotic_Thing') # ** Make sure the Local ID matches your Thing **

    return my_thing

# MAIN ---------------------

def main():
    with IOT.Client(config='Iotic_Agent.ini') as client:  # ** Make sure this matches your .ini file **
        my_thing = connect_thing(client)

        while True:
            try:
                print("Main running. Press ctrl+c to quit.")
                time.sleep(10)
            except KeyboardInterrupt:
                break

# RUN ------------------

if __name__ == '__main__':
    main()

# END -------------------

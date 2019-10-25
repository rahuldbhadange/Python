# RRPS Development on Windows

This is a quick overview of the development environment setup; full documentation will be made available later.

## Environment setup

### Python
Download and install Python 3.6.7 for Windows.

### Visual Studio compilers

Download and install the Microsoft Visual Studio build tools from https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2017 .

Execute the following from the folder where you downloaded the build tools to install them in `C:\Buildtools`:

```
vs_buildtools.exe --norestart --nocache --installPath C:\BuildTools --add Microsoft.VisualStudio.Workload.VCTools;includeRecommended --add Microsoft.VisualStudio.Component.Windows81SDK --add Microsoft.VisualStudio.ComponentGroup.NativeDesktop.Win81
```

The Visual Studio tools are required to build C extensions; if a `pip` execution fails to compile something, execute the following to ensure that the compilers are in the user path:

```
C:\BuildTools\VC\Auxiliary\Build\vcvarsall.bat x64 8.1
```

### Virtual environment

In order to avoid polluting the system python interpreter, it is necessary to create a virtual environment for development.

Such environment can be created by running the following:

```
mkdir %HOME%\envs
C:\Python36\python -mvenv %HOME%\envs\rrpsdev
```
hbd2kor> python -mvenv envs\rrpsdev
The environment can be activated in the current command prompt by running:

```
%HOME%\envs\rrpsdev\Scripts\activate
```

When the environment is active, you'll see its name in the command prompt, e.g.:

```
(rrpsdev) C:\Users\foo\>
```

### Editing

To edit the sources in Pycharm, create a new project pointing to the GIT clone.

Click on `File` > `Settings...` and then click on `Project: <project name>`.

Click on `Python interpreter`.

Click on the cog next to the interpreter dropdown and then on `Add...`

Select "Existing environment".

Click on `...` next to `Interpreter` and put `~\envs\rrpsdev\Scripts\python.exe` as the interpreter (adjust if your virtual environment is in a different location).

Click OK and make sure that the selected interpreter is the one you just created.

Click OK and wait for indexing to complete (see bottom of the editor for progress).

To verify that Pycharm is working properly, open `rrps\python\rrps.dt.integrator.sapequipmenthistory\rrps\dt\integrator\sapequipmenthistory\impl.py` and expand the imports.

Go over the NestedConfig symbol in the imports and press `CTRL+Q`; you should see the docstring for the module.

Ctrl + Click on the symbol and you should jump to its source code.

### Setup of the rrps.events package

The first package that should be added to the virtual environment is `rrps.events`; the package contains the definition of all the RRPS events that will be produced by integrators and consumed by followers.

To setup the package, activate your virtual environment, go to the `rrps\python\rrps.dt.events` directory and execute:

```
pip install -e . -f ..\..\..\deps
```

## How to

### A simple follower that dumps RRPS events to the console

Copy the directory `example\dt\acmecorp.dt.follower.exmple` to `rrps\python\rrps.dt.follower.example`.

Go inside that directory and:

- Rename the `acmecorp` directory to `rrps`.
- Delete `docker_collect_deps.sh`.
- Delete `README.md`.
- Delete `run_local.sh`.
- Delete `Dockerfile`.
- Delete `static_tests.sh`.

Open the file `setup.py` and perform the following changes:

- Change the name of the package to `rrps.dt.follower.example`.
- Change the dependency `acmecorp.dt.events>=0.1.0,<0.2` to `rrps.dt.events>=0.1.7,<0.2` ; this is particularly important as the package contains the definition of the events that the follower will follow.
- Change the first console script from `acmecorp-dt-follower-example = acmecorp.dt.follower.example.__main__:main` to `rrps-dt-follower-example = rrps.dt.follower.example.__main__:main`;
  this will cause the creation a script named `rrps-dt-follower-example` in the Python virtual environment that you will be able to use to launch the follower from the console.

Replace the file `rrps\dt\follower\example\__main__.py` with the file at the bottom of this document.

Open a command prompt and go the `rrps\python\rrps.dt.follower.example` directory, then activate your virtualenv and link the package to the environment by running:

```
pip install -e . -f ..\..\..\deps
```

#### Configuration

Open the file `cfg\follower.cfg.yml` and change the following parameters:

- `follower.thing.lid`: `follower` . This is the name of the thing that the follower will create in the Iotic Space to communicate with the Digital Twin runner.
- `asset.event.modules`: set the first item to `rrps.dt.events`. This option specifies the names of Python packages that contain event definitions.
- `asset.discovery.text`: set to `env_m_c`. This parameter tells the follower to look for things created by the Digital Twin runner that have the tag `env_m_c`, which is what we use to categorize assets in the Bosch environment.
- `asset.discovery.scope`: set to `local`.
- `asset.discovery.filter.tags.unique_regex`: set to `'^m_(.+)$'` . This is the regular expression that will be used by the follower to extract the unique identifier of the asset from a thing tag.
- `asset.discovery.filter.tags.thing`: set to `['env_m_c']`. This is a list of tags that will have to be assigned to the thing in order to be considered an asset.
- `asset.tracker.method.json.path`: set to `./tmp_assets.json`.

Create the file `cfg\agent.ini` and paste your **follower** agent credentials in it; note that it is not possible to have concurrent agents with the same credentials so each developer will need to ask for follower credentials and keep them personal.

Open the file `cfg\follower.log.yml` and change all instances of `acmecorp` to `rrps`.

#### Execution

You should now be able to start the follower by running:

```
rrps-dt-follower-example -l cfg\follower.log.yml cfg\follower.cfg.yml cfg\agent.ini
```

After a while you should see that assets are discovered, e.g.:

```
2019-01-28 15:22:29,651 INFO [rrps.dt.follower.example.impl] {ioticlabs.dt.api.follower.__do_callback} Asset created: 1000020
2019-01-28 15:22:34,774 INFO [rrps.dt.follower.example.impl] {ioticlabs.dt.api.follower.__do_callback} Asset created: 1000021
2019-01-28 15:22:40,969 INFO [rrps.dt.follower.example.impl] {ioticlabs.dt.api.follower.__do_callback} Asset created: 1000015
```

You can leave this follower running to see the events that will be published by integrators.

### Testing the sapmasterdata integrator

The sapmasterdata integrator is a simple integrator that periodically sends a request for each known asset to a SAP API and generates a `SapMasterDataSet` event containing information about a Powerpack.

The SAP API runs in the RRPS DMZ so it cannot be used for testing; that said, it is possible to run this integrator with mocked data.

Start the follower in a separate command prompt as described in the previous section.

Open a command prompt and go the `rrps\python\rrps.dt.integrator.sapmasterdata` directory, then activate your virtualenv and link the package to the environment by running:

```
pip install -e . -f ..\..\..\deps
```

#### Configuration

Open the file `cfg\integrator.cfg.yml` and change the following parameters:

- `config.use_mock_data`: set to `1` to use mock data instead of making actual http requests.
- `config.loop_time`: set to `10` to process assets every 10 seconds.
- `integrator.source`: `sapmasterdata`. The source will be set in each event produced by the integrator and should be set only once.
- `integrator.thing.lid`: `sapmasterdata` . This is the identifier of the thing that the integrator will create in the Iotic Space to communicate with the Digital Twin runner.
- `asset.event.modules`: set the first item to `rrps.dt.events`. This option specifies the names of Python packages that contain event definitions.
- `asset.discovery.text`: set to `env_m_p`. This parameter tells the follower to look for things created by the Digital Twin runner that have the tag `env_m_p`, which is what we use to categorize assets in the Bosch environment.
- `asset.discovery.scope`: set to `local`.
- `asset.discovery.filter.tags.unique_regex`: set to `'^m_(.+)$'` . This is the regular expression that will be used by the follower to extract the unique identifier of the asset from a thing tag.
- `asset.discovery.filter.tags.thing`: set to `['env_m_p']`. This is a list of tags that will have to be assigned to the thing in order to be considered an asset..

Create the file `cfg\agent.ini` and paste your **integrator** agent credentials in it; note that it is not possible to have concurrent agents with the same credentials so each developer will need to ask for follower credentials and keep them personal.

#### Execution

You should now be able to start the integrator by running:

```
rrps-dt-integrator-sapmasterdata -l cfg\integrator.log.yml cfg\integrator.cfg.yml cfg\agent.ini
```

After a while you should see that assets are discovered and events are fired, e.g.:

```
2019-01-28 15:36:03,173 DEBUG [rrps.dt.integrator.sapmasterdata.impl] {ioticlabs.dt.api.integrator.__do_callback} Asset created: 1000015
2019-01-28 15:36:04,469 DEBUG [rrps.dt.integrator.sapmasterdata.impl] {ioticlabs.dt.api.integrator.__do_callback} Asset created: 1000021
2019-01-28 15:36:08,017 DEBUG [rrps.dt.integrator.sapmasterdata.impl] {ioticlabs.dt.api.integrator.__do_callback} Asset created: 1000020
2019-01-28 15:37:06,141 DEBUG [rrps.dt.integrator.sapmasterdata.impl] {MainThread} Using mock master data
2019-01-28 15:37:06,143 INFO [rrps.dt.integrator.sapmasterdata.impl] {MainThread} Checking asset cache for: 1000020
2019-01-28 15:37:06,146 INFO [rrps.dt.integrator.sapmasterdata.impl] {MainThread} Publish event for 1000020
2019-01-28 15:37:06,146 DEBUG [rrps.dt.integrator.sapmasterdata.impl] {MainThread} Event: <SapMasterDataSet v1 ('1000020'@-1)>
```

If you look at the follower output, you should see events being received or replayed, e.g.:

```
2019-01-28 16:31:36,080 INFO [rrps.dt.follower.example.impl] {ioticlabs.dt.api.follower.__do_callback} [1000020] #0 SapMasterDataSet (from sapmasterdata) @ 2017-09-07 23:00:00 (sys: None)
{'Datab': 1504828800000,
 'Datbi': 253402214400000,
 'EqunrAgg': '000000000200000081',
 'EqunrEng': '000000000200000082',
 'Kunde': '0022111236',
 'MaktxAgg': 'AUFNAHMEKOERPER',
 'MaktxEng': 'R16V4000G83 REMAN ENGINE',
 'MatnrAgg': '12V2000C10',
 'MatnrEng': 'R16V4000G83',
 'Name1': 'Land Badenwürtenberg',
 'SernrAgg': 'SER-00123',
 'SernrEng': '4711-001',
 'Yybau': '030'}
2019-01-28 16:31:36,080 INFO [rrps.dt.follower.example.impl] {ioticlabs.dt.api.follower.__do_callback} Internal: <IntTwinEofReplay v1 ('1000021'@0)>
```

### Testing the sapequipmenthistory integrator

The sapequipmenthistory integrator is a simple integrator that periodically sends requests for each known asset to a SAP API to retrieve the history of equipment used in Powerpacks and related documents.

The SAP API runs in the RRPS DMZ so it cannot be used for testing; that said, it is possible to run this integrator with mocked data.

Start the follower in a separate command prompt as described in the previous section.

Open a command prompt and go the `rrps\python\rrps.dt.integrator.sapequipmenthistory` directory, then activate your virtualenv and link the package to the environment by running:

```
pip install -e . -f ..\..\..\deps
```

#### Configuration

Open the file `cfg\integrator.cfg.yml` and change the following parameters:

- `config.use_mock_data`: set to `1` to use mock data instead of making actual http requests.
- `config.loop_time`: set to `10` to process assets every 10 seconds.
- `config.data-cache`: set to `cache`.
- `integrator.source`: `SapDOC`. The source will be set in each event produced by the integrator and should be set only once.
- `integrator.thing.lid`: `sapequipmenthistory` . This is the identifier of the thing that the integrator will create in the Iotic Space to communicate with the Digital Twin runner.
- `asset.event.modules`: set the first item to `rrps.dt.events`. This option specifies the names of Python packages that contain event definitions.
- `asset.discovery.text`: set to `env_m_p`. This parameter tells the follower to look for things created by the Digital Twin runner that have the tag `env_m_p`, which is what we use to categorize assets in the Bosch environment.
- `asset.discovery.scope`: set to `local`.
- `asset.discovery.filter.tags.unique_regex`: set to `'^m_(.+)$'` . This is the regular expression that will be used by the follower to extract the unique identifier of the asset from a thing tag.
- `asset.discovery.filter.tags.thing`: set to `['env_m_p']`. This is a list of tags that will have to be assigned to the thing in order to be considered an asset..

Create the file `cfg\agent.ini` and paste your **integrator** agent credentials in it; note that it is not possible to have concurrent agents with the same credentials so each developer will need to ask for follower credentials and keep them personal.

#### Execution

You should now be able to start the integrator by running:

```
rrps-dt-integrator-sapequipmenthistory -l cfg\integrator.log.yml cfg\integrator.cfg.yml cfg\agent.ini
```

After a while you should see that assets are discovered and events are fires.

If you look at the follower output, you should see events containing the mock data being received/replayed.


## Attachments

### __main__.py file for the example follower

```
# Copyright (c) 2018 Iotic Labs Ltd. All rights reserved.


from argparse import ArgumentParser
from os import environ as env, getpid, kill
from signal import signal, SIGINT, SIGTERM

from ioticlabs.dt.api.util import load_config, configure_logging


def parse_args():
    """Command line arguments specific to this integrator"""
    parser = ArgumentParser(description='Example follower. Use SIGINT/SIGTERM/CTRL+C to exit gracefully.')
    parser.add_argument('cfg', metavar='CONFIG', help='Configuration file (yaml) for this follower')
    parser.add_argument('agent', metavar='AGENT', help='Agent credentials (ini) for this follower')
    parser.add_argument('-l', '--log-cfg', metavar='LOGGING_CONFIG', help='Configuration for Python logging (yaml)')
    parser.add_argument(
        '--storeutil', action='store_true',
        help="""Treat any supplied file arguments as environment variables defining storeutil blob keys to read
        configuration from.
        """
    )
    return parser.parse_args()


def get_blob_via_env(blobstore, arg):
    """arg -> environment variable -> blob name -> contents (bytes) -> utf8 string (return)"""
    return blobstore.get_blob(env[arg]).read().decode('utf8')


def follower_via_storeutil(args):
    """Configures logging and returns instance of Integrator. Exceptions are not handled since an early failure in the
    startup process is terminal."""
    from ioticlabs.common.storeutil import connect_blobstore

    bstore = connect_blobstore()

    configure_logging(get_blob_via_env(bstore, args.log_cfg) if args.log_cfg else None, as_string=True)

    # Importing only now so logging configuration has been applied already
    from IoticAgent.IOT.Config import Config
    from .impl import FollowerExample

    return FollowerExample(
        load_config(get_blob_via_env(bstore, args.cfg), as_string=True),
        Config(string=get_blob_via_env(bstore, args.agent))
    )


def follower_via_args(args):
    """Configures logging and returns instance of Integrator. Exceptions are not handled since an early failure in the
    startup process is terminal."""
    configure_logging(cfg_file=args.log_cfg)

    # Importing only now so logging configuration has been applied already
    from .impl import FollowerExample

    with open(args.agent, 'r') as agent_config_file:
        agent_config_str = agent_config_file.read()

    return FollowerExample(load_config(args.cfg), agent_config_str)


# Handle SIGTERM the same way as SIGINT (e.g. for running within docker)
def sigterm_handler(*_):
    kill(getpid(), SIGINT)


def main():
    signal(SIGTERM, sigterm_handler)

    args = parse_args()
    follower = follower_via_storeutil(args) if args.storeutil else follower_via_args(args)
    try:
        follower.run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
```
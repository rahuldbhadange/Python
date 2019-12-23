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
    from .impl import SynthesiserWeather

    return SynthesiserWeather(
        load_config(get_blob_via_env(bstore, args.cfg), as_string=True),
        Config(string=get_blob_via_env(bstore, args.agent))
    )


def follower_via_args(args):
    """Configures logging and returns instance of Integrator. Exceptions are not handled since an early failure in the
    startup process is terminal."""
    configure_logging(cfg_file=args.log_cfg)

    # Importing only now so logging configuration has been applied already
    from .impl import SynthesiserWeather

    return SynthesiserWeather(load_config(args.cfg), args.agent)


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

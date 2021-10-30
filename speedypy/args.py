import argparse
import pkgutil
from importlib import import_module
import logging

from speedypy._meta import __version__, __doc__

log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    description=__doc__,
)

parser.add_argument(
    '-v', '--version', action='version',
    version=__version__,
)

parser.add_argument(
    '-c', '--config',
    default='',
    help="path to config file (default: "
    "${XDG_CONFIG_HOME:-$HOME/.config}/speedypy/speedypy.conf or "
    "./speedypy.conf)",
)


parser.add_argument(
    '-l', '--log-level',
    choices=['INFO', 'WARNING', 'ERROR', 'DEBUG'],
    default='INFO',
    help="log level (default: %(default)s)",
)


subparsers = parser.add_subparsers(help='choose a sub-command',
                                   dest='subcommand')
# Keep track of the subparsers we add so we can add subsubparsers
subparsers_map = {}


def argument(*name_or_flags, **kwargs):
    """Convenience function to properly format arguments to pass to the
    subcommand decorator.
    """
    return (list(name_or_flags), kwargs)


def subcommand(args=[], parent=subparsers):
    """Decorator to define a new subcommand in a sanity-preserving way.
    The function will be stored in the ``func`` variable when the parser
    parses arguments so that it can be called directly like so::
        args = cli.parse_args()
        args.func(args)
    Usage example::
        @subcommand([argument("-d", help="Enable debug mode",
                              action="store_true")])
        def subcommand(args):
            print(args)
    Then on the command line::
        $ python cli.py subcommand -d
    """
    def decorator(func):
        parser = parent.add_parser(func.__name__, description=func.__doc__)
        for arg in args:
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=func)
        subparsers_map[func.__name__] = parser
    return decorator


def parse_args(argv=None):
    from speedypy import subcommands
    for importer, modname, _ in pkgutil.iter_modules(subcommands.__path__):
        import_module('..subcommands.' + modname, __name__)
    args = parser.parse_args(argv)
    args.config = parse_config(args.config)
    if not args.subcommand:
        parser.print_help()
        exit(0)
    return args


def parse_config(path):
    import configparser
    import collections
    import os

    import xdg.BaseDirectory

    config_parser = configparser.ConfigParser()
    if not path:
        path = './speedypy.conf'
        if not os.path.exists(path):
            path = os.path.join(
                xdg.BaseDirectory.xdg_config_home,
                'speedypy',
                'speedypy.conf',
            )
    config_parser.read(path)
    attrs = 'exclude_servers'.split()
    Config = collections.namedtuple('Config', attrs)
    config = Config(
        *[config_parser['DEFAULT'].get(a) for a in attrs]
    )

    return config


def get_exclude_servers(args):
    try:
        exclude_servers = args.config.exclude_servers.split(',')
    except AttributeError:
        exclude_servers = None
    return exclude_servers


def get_file(name):
    import os

    import xdg.BaseDirectory

    if name == 'logfile':
        logfile_name = os.path.join(
            xdg.BaseDirectory.save_data_path('speedypy'),
            'speedtests.log',
        )
        return logfile_name

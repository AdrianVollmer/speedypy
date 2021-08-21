import argparse

from speedypy.args import subcommand, argument, get_exclude_servers, \
    subparsers_map, get_file

args = []


args.append(argument(
    '-o', '--outfile',
    default='-',
    type=argparse.FileType(mode='w'),
    help="path to an output file (default: stdout)",
))


@subcommand(args)
def plot(args):
    '''Visualize the data'''


subparsers = subparsers_map['plot'].add_subparsers(help='choose a sub-command',
                                                   dest='subcommand')

time_series_args = []


time_series_args.append(argument(
    '-D', '--no-download',
    default=False,
    action='store_true',
    help="don't show download data (default: %(default)s)",
))


time_series_args.append(argument(
    '-U', '--no-upload',
    default=False,
    action='store_true',
    help="don't show upload data (default: %(default)s)",
))


time_series_args.append(argument(
    '-P', '--no-ping',
    default=False,
    action='store_true',
    help="don't show ping data (default: %(default)s)",
))

time_series_args.append(argument(
    '-a', '--include-all-servers',
    default=False,
    action='store_true',
    help="also show data points from servers that are excluded "
    "in the config file (default: %(default)s)",
))


time_series_args.append(argument(
    '-w', '--smoothing-window',
    default=12,
    type=int,
    help="size of the smoothing window in hours (default: %(default)s)",
))


@subcommand(time_series_args, parent=subparsers)
def time_series(args):
    '''Plot data as a time series'''
    import json
    import dateutil

    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.ndimage.filters import uniform_filter1d

    exclude_servers = get_exclude_servers(args)
    logfile_name = get_file('logfile')

    data = []
    with open(logfile_name, 'r') as f:
        for line in f.readlines():
            j = json.loads(line)
            if int(j['server']['id']) not in exclude_servers:
                data.append(json.loads(line))

    f = dateutil.parser.isoparse
    time = np.array([f(d['timestamp']) for d in data])

    download = np.array([d['download']/1024**2 for d in data])
    upload = np.array([d['upload']/1024**2 for d in data])
    ping = np.array([d['ping'] for d in data])

    size = args.smoothing_window
    download = uniform_filter1d(download, size=size)
    upload = uniform_filter1d(upload, size=size)
    ping = uniform_filter1d(ping, size=size)

    lines = {
        "Download [Mbit/s]": download,
        "Upload [Mbit/s]": upload,
        "Ping [ms]": ping,
    }

    for label, values in lines.items():
        plt.plot(time, values, label=label)
    plt.legend()
    plt.show()

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
    '-D', '--hide-download',
    default=False,
    action='store_true',
    help="don't show download data (default: %(default)s)",
))


time_series_args.append(argument(
    '-U', '--hide-upload',
    default=False,
    action='store_true',
    help="don't show upload data (default: %(default)s)",
))


time_series_args.append(argument(
    '-P', '--hide-ping',
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

    import matplotlib.pyplot as plt
    from scipy.ndimage.filters import uniform_filter1d

    exclude_servers = get_exclude_servers(args)
    time, download, upload, ping = get_data(exclude_servers)

    # TODO use time window, not number of data points
    size = args.smoothing_window
    download = uniform_filter1d(download, size=size)
    upload = uniform_filter1d(upload, size=size)
    ping = uniform_filter1d(ping, size=size)

    lines = {}
    if not args.hide_download:
        lines["Download [Mbit/s]"] = download
    if not args.hide_upload:
        lines["Upload [Mbit/s]"] = upload
    if not args.hide_ping:
        lines["Ping [ms]"] = ping

    for label, values in lines.items():
        plt.plot(time, values, label=label)
    plt.legend()
    plt.show()


scatter_args = []

scatter_args.append(argument(
    '-q', '--quantity',
    default='download',
    choices=['download', 'upload', 'ping'],
    help="which quanitity to plot (default: %(default)s)",
))

scatter_args.append(argument(
    '-b', '--bin-size',
    default=1,
    type=int,
    help="bin size in hours (default: %(default)s)",
))

scatter_args.append(argument(
    '-A', '--hide-average',
    default=False,
    action='store_true',
    help="hide average values (default: %(default)s)",
))

scatter_args.append(argument(
    '-D', '--hide-data',
    default=False,
    action='store_true',
    help="hide data points (default: %(default)s)",
))


@subcommand(scatter_args, parent=subparsers)
def scatter(args):
    '''Visualize the speed results as a scatter plot'''
    import collections

    import matplotlib.pyplot as plt
    import numpy as np

    exclude_servers = get_exclude_servers(args)
    data = get_data(exclude_servers)
    data = dict(zip(['time', 'download', 'upload', 'ping'], data))
    time = data['time']
    time_ = []
    for t in time:
        t = t.time()
        t = t.hour + t.minute/60
        time_.append(t)
    time = time_
    quantity = data[args.quantity]
    if args.quantity == 'ping':
        unit = 'ms'
    else:
        unit = 'Mbit/s'

    if not args.hide_average:
        bins = collections.defaultdict(list)
        for t, x in zip(time, quantity):
            bins[(t * 60) // (60 * args.bin_size)].append(x)

        mean = collections.defaultdict(list)
        stddev = collections.defaultdict(list)
        for k, v in bins.items():
            mean[k + 0.5] = np.mean(v)
            stddev[k + 0.5] = np.std(v)

        plt.errorbar(mean.keys(), mean.values(), yerr=stddev.values(),
                     marker='o', linestyle="", label='Average [%s]' % unit,
                     color='red')

    if not args.hide_data:
        plt.scatter(time, quantity, label='Data [%s]' % unit)
    plt.legend()
    plt.xlabel('Time of day in hours')
    plt.show()


def get_data(exclude_servers):
    import json
    import dateutil

    import numpy as np

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

    return time, download, upload, ping

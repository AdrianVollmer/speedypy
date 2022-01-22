import argparse

from speedypy.common import get_data
from speedypy.args import subcommand, argument, get_exclude_servers, \
    subparsers_map

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
    default=None,
    type=int,
    help="size of the smoothing window in hours (default: %(default)s)",
))


@subcommand(time_series_args, parent=subparsers)
def time_series(args):
    '''Plot data as a time series'''

    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    exclude_servers = get_exclude_servers(args)
    data = get_data(exclude_servers)

    window_size = args.smoothing_window
    if window_size:
        data['download'], data['upload'], data['ping'] = [
            d.rolling('%ih' % window_size).mean()
            for d in (data['download'], data['upload'], data['ping'])
        ]

    lines = {}
    if not args.hide_download:
        lines["Download [Mbit/s]"] = data['download']
    if not args.hide_upload:
        lines["Upload [Mbit/s]"] = data['upload']
    if not args.hide_ping:
        lines["Ping [ms]"] = data['ping']

    for label, values in lines.items():
        plt.plot(data.index, values, label=label)

    gaps = find_gaps(data.index)
    if gaps:
        for g in gaps:
            plt.axvspan(g[0], g[0] + g[1], alpha=0.2, color='red')

        handles, labels = plt.gca().get_legend_handles_labels()
        red_patch = mpatches.Patch(alpha=0.2, color='red',
                                   label='Missing data')
        handles.append(red_patch)

    plt.legend(handles=handles)
    title = "Bandwidth (%s)" % ', '.join(set(data['isp']))
    if window_size:
        title += ', %ih rolling average' % window_size
    plt.title(title)
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
    import statistics

    import matplotlib.pyplot as plt

    exclude_servers = get_exclude_servers(args)
    data = get_data(exclude_servers)[:-1]
    time = data.index
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
            mean[k + 0.5] = statistics.mean(v)
            stddev[k + 0.5] = statistics.stdev(v)

        plt.errorbar(mean.keys(), mean.values(), yerr=stddev.values(),
                     marker='o', linestyle="", label='Average [%s]' % unit,
                     color='red')

    if not args.hide_data:
        plt.scatter(time, quantity, label='Data [%s]' % unit)
    plt.legend()
    plt.xlabel('Time of day in hours')
    plt.show()


def find_gaps(time):
    import statistics
    distances = [(t, time[i+1] - t) for i, t in enumerate(time[:-1])]
    second_list = [x[1].seconds for x in distances]
    mean = statistics.mean(second_list)
    stddev = statistics.stdev(second_list)

    result = [x for x in distances if x[1].seconds > mean + 5*stddev]
    return result

from speedypy.args import subcommand, argument
from speedypy.common import get_data

args = []


args.append(argument(
    '-o', '--outfile',
    default=None,
    help="path to an output file (default: stdout)",
))


@subcommand(args)
def analytics(args):
    '''Output interesting statistics'''
    import statistics

    data = get_data()
    total_mean = statistics.mean(data['download'])
    total_std = statistics.stdev(data['download'])
    print("Download:\t%.2f +- %.2f Mbit/s" % (
        total_mean,
        total_std,
    ))
    print("Upload:\t\t%.2f +- %.2f Mbit/s" % (
        statistics.mean(data['upload']),
        statistics.stdev(data['upload']),
    ))
    print("Ping:\t\t%.2f +- %.2f ms" % (
        statistics.mean(data['ping']),
        statistics.stdev(data['ping']),
    ))

    ids = data['server_id'].unique()
    print("\nIDs of consistently slow servers (download only):")
    for id_ in ids:
        subdata = data[data['server_id'] == id_]
        count = subdata['download'].count()

        if count < 3:  # dismiss servers we've seen less than 3 times
            continue

        result = {}
        for q in ['download', 'upload', 'ping']:
            stddev = subdata[q].std()
            mean = subdata[q].mean()

            if abs(total_mean - mean) > (stddev**2 + total_std**2)**.5:
                result[q] = (mean, stddev)
        if 'download' in result:
            id_text = "%s (%d data points):" % (
                id_,
                count,
            )
            print(id_text)
            for k, v in result.items():
                print("\t%s: %.2f +- %.2f" % (k, *v))

import logging

from speedypy.args import subcommand, argument

args = []
log = logging.getLogger(__name__)


args.append(argument(
    '-n', '--dont-store',
    default=False,
    action='store_true',
    help="output result on stdout instead of storing on disk"
    " (default: %(default)s)",
))


@subcommand(args)
def measure(args):
    '''Measure speed and log result'''
    log.info("Running speedtest...")
    try:
        exclude_servers = args.config.exclude_servers.split(',')
    except AttributeError:
        exclude_servers = None
    result = run_speedtest(exclude_servers=exclude_servers)
    if args.dont_store:
        print(result)
    else:
        store_result(result)


def run_speedtest(exclude_servers=[]):
    # https://github.com/sivel/speedtest-cli/wiki
    import speedtest

    s = speedtest.Speedtest()
    s.get_servers(exclude=exclude_servers)
    s.get_best_server()
    s.download()
    s.upload()

    return s.results.dict()


def store_result(result):
    import json
    import os

    import xdg.BaseDirectory

    logfile_name = os.path.join(
        xdg.BaseDirectory.save_data_path('speedypy'),
        'speedtests.log',
    )
    log.info("Storing result to file: %s" % logfile_name)
    with open(logfile_name, 'a') as fp:
        json.dump(result, fp)

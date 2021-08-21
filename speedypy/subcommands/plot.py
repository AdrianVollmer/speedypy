import argparse

from speedypy.args import subcommand, argument

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

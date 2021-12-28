from speedypy.args import subcommand, argument

args = []


args.append(argument(
    '-o', '--outfile',
    default=None,
    help="path to an output file (default: stdout)",
))


@subcommand(args)
def analytics(args):
    '''Output interesting statistics'''
    print("Not yet implemented")

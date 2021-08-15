def main(argv=None):
    from speedypy.args import parse_args
    from speedypy.log import init_logging
    args = parse_args(argv=argv)
    init_logging(loglevel=args.log_level)
    args.func(args)


if __name__ == "__main__":
    main()

from speedypy.args import get_file


def get_data(exclude_servers=[]):
    import json
    import dateutil

    import pandas

    logfile_name = get_file('logfile')

    data = []
    with open(logfile_name, 'r') as f:
        for line in f.readlines():
            if not line.strip():
                continue
            j = json.loads(line)
            if not j:
                continue
            try:
                if int(j['server']['id']) not in exclude_servers:
                    data.append(j)
            except Exception:
                print("Error while parsing line: %s" % line)

    if not data:
        print("No data available")
        exit(1)

    f = dateutil.parser.isoparse
    time = ([f(d['timestamp']) for d in data])

    download = [d['download']/1024**2 for d in data]
    upload = [d['upload']/1024**2 for d in data]
    ping = [d['ping'] for d in data]
    server_id = [d['server']['id'] for d in data]
    isp = [d['client']['isp'] for d in data]

    return pandas.DataFrame(index=time, data=dict(
        download=download,
        upload=upload,
        ping=ping,
        server_id=server_id,
        isp=isp,
    ))

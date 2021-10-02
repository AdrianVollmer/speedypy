speedypy
========

Measure and visualize your internet speed

Installation
------------

Make sure you have Python3 and pip installed, then run this:

```
$ pip3 install --user git+https://github.com/AdrianVollmer/speedypy
```

Usage
-----

Put this in your crontab with `crontab -e`:

```
17 * * * * /home/username/.local/bin/speedypy --log-level ERROR measure

```

This runs the `measure` subcommand once an hour, at 17 minutes after the
full hour.

To visualize, run `speedypy plot time_series`.

Read the output of `speedypy -h` for more information.


Config
------

In `$HOME/.config/speedypy/speedypy.conf` you can exclude certain servers
that consistenly yield outliers. It could look like this:

```
[DEFAULT]

exclude_servers = 1338,16633,15728
```

You'll find the server IDs in `$HOME/.local/share/speedypy/speedtests.log`.

(A nicer way to identify such servers will be included in future versions.)


Author
------

Adrian Vollmer

License
-------

MIT

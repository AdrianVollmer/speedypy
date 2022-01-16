speedypy
========

Measure and visualize your internet speed systematically

![Speedypy Example](https://github.com/AdrianVollmer/speedypy/blob/master/doc/speedypy_example.png)


Installation
------------

Make sure you have Python3 and pip installed, then run this:

```
$ python3 -m pip install --user git+https://github.com/AdrianVollmer/speedypy
```

Usage
-----

On Linux, put something like this in your crontab with `crontab -e`:

```
17 * * * * /home/<USERNAME>/.local/bin/speedypy --log-level ERROR measure

```

This runs the `measure` subcommand once an hour, at 17 minutes after the
full hour. One measurement per hour is a sensible frequency.

To visualize, run `speedypy plot time_series`.

Read the output of `speedypy -h` for more information.


Config
------

We adhere to the [XDG Base Directory
Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html),
so the configuration file is in `$HOME/.config/speedypy` by default.

In `$HOME/.config/speedypy/speedypy.conf` you can exclude certain servers
that consistently yield outliers. It could look like this:

```
[DEFAULT]

exclude_servers = 1338,16633,15728
```

You'll find the server IDs in `$HOME/.local/share/speedypy/speedtests.log`.

(A nicer way to identify such servers will be included in future versions.)


Limitations
-----------

Because we can exclude bad servers and the plot is done using a rolling
average over many data points per day, the presented data should be quite
robust and suitable for judging whether your actual bandwidth matches what
you are paying for.

However, note that the connection speed may also be influenced by factors
between your computer and your provider, such as a bad cable, faulty
hardware or a poor wifi signal. Best results are achieved when running this
on a computer that is connected via ethernet cable directly to the modem or
router of your internet service provider.

Of course, this tool may detect anomalies that occur in-between
measurements, such as a complete outage of the connection with a duration of
half an hour or less.

Author
------

Adrian Vollmer

License
-------

MIT

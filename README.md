speedypy
========

Measure and visualize you internet speed

Installation
------------

Make sure you have Python3 and pip instlaled, then run this:

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


Author
------

Adrian Vollmer

License
-------

MIT

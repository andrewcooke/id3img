id3img
======

This is a simple web server that works with
[MPDroid](https://github.com/abarisain/dmix) so that you can see the
album art for your music.

By default, [MPDroid](https://github.com/abarisain/dmix) will pull images
from [Last.fm](http://last.fm), which is OK, but doesn't always get exactly
the right image.  So there is an alternative configuration (see
"Download local cover art" in the settings) that allows you to pull images
from a "web server" - `id3img` provides a suitable web server.

`id3img` provides images from four different sources:

  * from `/root/artist/album/folder.jpg` - this assumes that each album
    directory contains an image with a fixed name (by default `folder.jpg`,
    but you can change it in [MPDroid](https://github.com/abarisain/dmix)'s
    settings).

  * from an ID3 `PIC` or `APIC` tag in any `/root/artist/album/*.mp3` -
    so if any mp3 in that directory contains an image in the ID3 data,
    then that image will be used.

  * from `/root/Various/album/folder.jpg` - as above (fixed name file), but
    maybe the album is a collection from various artists.

  * from an ID3 `PIC` or `APIC` tag in any `/root/Various/album/*.mp3` -
    as above (ID3 image), but maybe the album is a collection from various
    artists.

In the examples above, `/root` is the path that you give to the `id3img` server
on the command line when you start the program (see below).  The values of
`artist` and `album` are taken from the music that is being played.
An alternative for `folder.jpg` can be set in the
[MPDroid](https://github.com/abarisain/dmix) settings.

Limitations
-----------

This is Python code, not packaged in anyway, so you need to be able to install
Python software from Github and be comfortable with getting it running.

It has been tested only on Linux, with Python 3.3 (it will not work with
Python 2 - come on, it's 2013 already).

Everything assumes that the music is grouped in directories by artist name
and then album name.

**IMPORTANT** - this program provides access to files on your computer.
A remote user can request any file, by giving the appropriate path.  So you
should only use it on a local network where you trust other users.
(In theory, only files below the directory containing music - the path given
on the command line at startup - are available, but there may be bugs in the
code.)

Installation
------------

  0. Make sure that you have Python 3 (tested with Python 3.3) available.

  1. Clone this git repo.

  2. If you want, you can use the `setup-env.sh` script to create a
     virtualenv environment.

  3. Run the server.  For example,

     `PYTHONPATH=src python3.3 src/id3img/server.py /music/mp3`

     For help on options, see `python3.3 src/id3img/server.py -h`.

  4. Configure [MPDroid](https://github.com/abarisain/dmix).  You will
     likely want to change the "path to music" to be something like
     `http://your.machine:6601/`.

Debugging
---------

You can enable debug logging (to stderr) with:

`python3.3 src/id3img/server.py -l DEBUG /path/to/music`

Don't forget to open port 6601 (or whatever value you configure with `-p`)
in your firewall.

Licence
-------

Code is (c) Andrew Cooke 2013, but released into the public domain with
absolutely no warranty.  So you can do what you like with it.  Just don't
sue me.

Stagger
-------

This software includes a copy of [Stagger](https://code.google.com/p/stagger)
which appears to be no longer maintained, and does not install.  The copyright
remains with the initial author, Karoly Lorentey.  See LICENCE file in the
stagger directory.


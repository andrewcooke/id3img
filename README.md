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

Limitations
-----------

This is Python code, not packaged in anyway, so you need to be able to install
Python software from Github and be comfortable with getting it running.

It has been tested only on Linux, with Python 3.3 (it will not work with
Python 2 - come on, it's 2013 already).

Everything assumes that the music is grouped in directories by artist name
and then album name.

Installation
------------

  0. Make sure that you have Python 3 (tested with Python 3.3) available.

  1. Clone this git repo.

  2. If you want, you can use the `setup-env.sh` script to create a
     virtualenv environment.  Alternatively, make sure that you have the
     [Stagger](https://code.google.com/p/stagger/) library installed
     (perhaps by doing `sudo easy_install stagger`).

  3. Run the server.  For example,

     `python3.3 src/id3img/server.py /music/mp3`

     For help on options, see `python3.3 src/id3img/server.py -h`.

  4. Configure [MPDroid](https://github.com/abarisain/dmix).  You will
     likely want to change the "path to music" to be something like
     `http://your.machine:6601/`.

Debugging
---------

You can enable debug information with:

`python3.3 src/id3img/server.py -l DEBUG /path/to.music`

Don't forget to open port 6601 (or whatever value you configure with `-p`)
in your firewall.

Licence
-------

Code is (c) Andrew Cooke 2013, but released into the public domain with
absolutely no warranty.  So you can do what you like with it.  Just don't
sue me.


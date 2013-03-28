
from argparse import ArgumentParser
from http.server import BaseHTTPRequestHandler, HTTPServer
from logging import basicConfig, getLogger
from mimetypes import guess_type
from os import listdir
from urllib.parse import unquote
from os.path import join

from stagger import read_tag


def find_image(root, path):
    '''
    Find a suitable image and return (mime type, binary data).  We try to make
    everyone happy by including:
    - the exact file requested (folder.jog by default)
    - any ID3 picture from an mp3 file in that directory
    - the same as above, but with the artist name (first path element)
      replaced by "Various"
    '''
    artist, rest = path.split('/')
    album, file = rest.rsplit('/')
    for name in artist, 'Various':
        dir = join(root, name, album)
        for mime, data in exact_file(dir, file): yield mime, data
        for mime, data in id3_picture(dir): yield mime, data


def exact_file(dir, file):
    LOG = getLogger('exact_file')
    path = join(dir, file)
    try:
        LOG.debug('trying %s' % path)
        with open(path, 'rb') as input:
            LOG.info('found %s' % path)
            yield guess_type(file), input.readall()
    except KeyboardInterrupt: raise
    except Exception as e: LOG.debug(e)


def id3_picture(dir):
    LOG = getLogger('id3_picture')
    try:
        for file in listdir(dir):
            if file.endswith('.mp3'):
                LOG.debug('trying %s' % file)
                tag = read_tag(join(dir, file))
                for key in 'PIC', 'APIC':
                    if key in tag:
                        LOG.info('found %s' % file)
                        pic = tag[key][0]
                        yield pic.mime, pic.data
    except KeyboardInterrupt: raise
    except Exception as e: LOG.debug(e)



def handler(root):

    LOG = getLogger('handler')

    class ImageHandler(BaseHTTPRequestHandler):

        def do_GET(self):
            LOG.debug('request: %s' % self.path)
            try:
                for mime, data in find_image(root, unquote(self.path[1:])):
                    self.send_response(200)
                    self.send_header('Content-type', mime)
                    self.end_headers()
                    self.wfile.write(data)
                    return
            except KeyboardInterrupt: raise
            except Exception as e:
                LOG.debug(e)
                self.send_error(404, '%s not found' % self.path)

    return ImageHandler


def options():
    parser = ArgumentParser(description='Serve embedded ID3 images.')
    parser.add_argument('-a', '--address', default='0.0.0.0', help='address for server to listen on')
    parser.add_argument('-p', '--port', type=int, default=6601, help='port for server to listen on')
    parser.add_argument('-l', '--loglevel', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='WARNING', help='log level')
    parser.add_argument('path', help='path to music files')
    args = parser.parse_args()
    basicConfig(level=args.loglevel)
    return args


if __name__ == '__main__':
    args = options()
    getLogger(__name__).info('Serving on %s:%d', args.address, args.port)
    server = HTTPServer((args.address, args.port), handler(args.path))
    server.serve_forever()

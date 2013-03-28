
from argparse import ArgumentParser
from http.server import BaseHTTPRequestHandler, HTTPServer
from logging import basicConfig, getLogger
from urllib.parse import unquote
from os.path import join

from stagger import read_tag


def handler(root):

    LOG = getLogger('handler')

    class ImageHandler(BaseHTTPRequestHandler):

        def do_GET(self):
            LOG.debug('request: %s' % self.path)
            try:
                tag = read_tag(join(root, unquote(self.path[1:])))
                for key in 'PIC', 'APIC':
                    if key in tag: return self.image(tag[key][0])
                raise Exception('No image found')
            except KeyboardInterrupt: raise
            except Exception as e:
                LOG.debug(e)
                self.send_error(404, '%s not found' % self.path)

        def image(self, tag):
            LOG.debug(tag)
            self.send_response(200)
            self.send_header('Content-type', tag.mime)
            self.end_headers()
            self.wfile.write(tag.data)

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

#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
from optparse import OptionParser
from argparse import ArgumentParser

ROUTER = {
    '/': {
        'file': 'index.html',
        'mime': 'text/html'
    },
    '/index.html': {
        'file': 'index.html',
        'mime': 'text/html'
    },
    '/main.js': {
        'file': 'main.js',
        'mime': 'application/javascript'
    },
    '/qrcode.min.js': {
        'file': 'qrcode.min.js',
        'mime': 'application/javascript'
    }
}

class Dictionary(object):

    def __init__(self, filename, interval):
        self.interval = interval
        self.dict = []
        with open(filename) as dict:
            for line in dict:
                self.dict.append(line)

    def getWord(self):
        value = self.dict[0]
        self.dict.pop(0)
        return value.strip()

    def getInterval(self):
        return str(self.interval)


class RequestHandler(BaseHTTPRequestHandler):

    def word(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(self.getWord(), 'utf8'))

    def interval(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(self.getInterval(), 'utf8'))

    def files(self):
        self.send_response(200)
        self.send_header('Content-type', ROUTER[self.path]['mime'])
        self.end_headers()
        with open('files/%s' % ROUTER[self.path]['file']) as fp:
            self.wfile.write(bytes(fp.read(), 'utf8'))

    def error404(self):
        self.send_response(404)
        self.end_headers()

    def do_GET(self):
        if self.path in list(ROUTER):
            self.files()
        elif self.path == '/word':
            self.word()
        elif self.path == '/interval':
            self.interval()
        else:
            self.error404()
        return


def start():
    parser = ArgumentParser()
    parser.add_argument('-d', dest='dict', help='dictionary FILE',
                        metavar='FILE', type=str, required=True)

    parser.add_argument('-p', dest='port', default=8080, help='server port (8080 default)',
                        metavar='PORT', type=int)

    parser.add_argument('-i', dest='interval', default=1000, help='brute force interval (1000 ms default)',
                        metavar='MILLISECONDS', type=int)

    args = parser.parse_args()

    words = Dictionary(args.dict, args.interval)
    handler = RequestHandler
    setattr(handler, 'getWord', words.getWord)
    setattr(handler, 'getInterval', words.getInterval)
    print('Starting Server...')
    httpd = HTTPServer(('0.0.0.0', args.port), handler)
    httpd.serve_forever()


if __name__ == '__main__':
    start()

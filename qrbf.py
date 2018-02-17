#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer

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

    def __init__(self):
        self.dict = []
        with open('test.txt') as dict:
            for line in dict:
                self.dict.append(line)

    def getWord(self):
        value = self.dict[0]
        self.dict.pop(0)
        return value.strip()


class RequestHandler(BaseHTTPRequestHandler):

    def word(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(self.getWord(), 'utf8'))

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
        else:
            self.error404()
        return


def start():
    dict = Dictionary()
    handler = RequestHandler
    setattr(handler, "getWord", dict.getWord)
    print('Starting Server...')
    httpd = HTTPServer(('0.0.0.0', 8081), handler)
    httpd.serve_forever()


if __name__ == '__main__':
    start()

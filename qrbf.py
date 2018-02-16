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

    def jsonp(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/javascript')
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
        elif self.path == '/jsonp':
            self.jsonp()
        else:
            self.error404()
        return


def start():
    print('Starting Server...')
    dict = Dictionary()
    handler = RequestHandler
    setattr(handler, "getWord", dict.getWord)
    httpd = HTTPServer(('127.0.0.1', 8081), handler)
    httpd.serve_forever()


if __name__ == '__main__':
    start()

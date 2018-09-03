#!/usr/bin/python
#encoding=utf-8
import SimpleHTTPServer
import SocketServer
import re
from common.mymako import render_mako_context, render_json
 
def htc(m):
    return chr(int(m.group(1),16))
 
def urldecode(url):
    rex=re.compile('%([0-9a-hA-H][0-9a-hA-H])',re.M)
    return rex.sub(htc,url)

def runser():
    Handler = SETHandler
    PORT = 8080
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print "serving at port", PORT
    httpd.serve_forever()
 
class SETHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def createHTML(self):
        html = file("index.html", "r")
        for line in html:
            self.wfile.write(line)
            
    def do_GET(self):
        print "GET"
        print self.headers;
        print u"操作get"
        
    def do_POST(self):
        print "POST"
        print self.headers;
        length = int(self.headers.getheader('content-length'))
        qs = self.rfile.read(length)
        url=urldecode(qs)
        print "url="
        print url
        #self.createHTML()
    
        


    


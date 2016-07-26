from threading import Thread

import storage
import re
import json

class addPair(Thread) :
    def __init__(self, csock, req):
        Thread.__init__(self)
        self.csock = csock
        self.req = req

    def run(self):
        postData = re.findall(r'^.*\r\n\r\n(.*)', self.req, re.MULTILINE)[0]
        match = re.match("key=(\w+)&value=(\w+)", postData)
        key = match.group(1)
        value = match.group(2)
        if key in storage.objects :
            self.csock.sendall("""HTTP/1.0 200 OK
                        Content-Type: text/json\r\n
                        {status : "failed", cause : "key already exists"}""")
        else :
            storage.objects[key] = value
            self.csock.sendall("""HTTP/1.0 200 OK
                        Content-Type: text/json\r\n
                        {status : "ok"}""")
        self.csock.close()


class updatePair(Thread) :
    def __init__(self, csock, req):
        Thread.__init__(self)
        self.csock = csock
        self.req = req

    def run(self):
        postData = re.findall(r'^.*\r\n\r\n(.*)', self.req, re.MULTILINE)[0]
        match = re.match("key=(\w+)&value=(\w+)", postData)
        key = match.group(1)
        value = match.group(2)
        if key in storage.objects :
            storage.objects[key] = value
            self.csock.sendall("""HTTP/1.0 200 OK
                        Content-Type: text/json\r\n
                        {status : "ok"}""")
        else :
            self.csock.sendall("""HTTP/1.0 200 OK
                        Content-Type: text/json\r\n
                        {status : "failed", cause : "key does not exist"}""")
        self.csock.close()

class deletePair(Thread) :
    def __init__(self, csock, req):
        Thread.__init__(self)
        self.csock = csock
        self.req = req

    def run(self):
        postData = re.findall(r'^.*\r\n\r\n(.*)', self.req, re.MULTILINE)[0]
        match = re.match("key=(\w+)", postData)
        key = match.group(1)
        if key in storage.objects :
            del storage.objects[key]
            self.csock.sendall("""HTTP/1.0 200 OK
                        Content-Type: text/json\r\n
                        {status : "ok"}""")
        else :
            self.csock.sendall("""HTTP/1.0 200 OK
                        Content-Type: text/json\r\n
                        {status : "failed", cause : "key does not exist"}""")
        self.csock.close()


class view(Thread) :
    def __init__(self, csock):
        Thread.__init__(self)
        self.csock = csock

    def run(self):
        pairs = json.dumps(storage.objects)
        self.csock.sendall("""HTTP/1.0 200 OK
                                Content-Type: text/json\r\n
                                """ + pairs)
        self.csock.close()

class retrieve(Thread) :
    def __init__(self, csock, req):
        Thread.__init__(self)
        self.csock = csock
        self.req = req

    def run(self):
        match = re.match('GET /retrieve/(\w+)\sHTTP/1', self.req)
        key = match.group(1)
        if key in storage.objects :
            s = '{status: "ok", value: "' + storage.objects[key] + '"}'
            self.csock.sendall("""HTTP/1.0 200 OK
                                            Content-Type: text/json\r\n
                                            """ + s)
        else :
            self.csock.sendall("""HTTP/1.0 200 OK
                                    Content-Type: text/json\r\n
                                    {status : "failed", cause : "key does not exist"}""")
        self.csock.close()
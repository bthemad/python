from twisted.application import internet, service
from twisted.internet import protocol, reactor, defer
from twisted.protocols import basic
from twisted.web import resource, server, static

import cgi


class FingerProtocol(basic.LineReceiver):
    def lineReceived(self, user):
        d = self.factory.getUser(user)

        def onError(err):
            return 'Internal error in server'
        d.addErrback(onError)

        def writeResponse(message):
            self.transport.write(message + "\r\n")
            self.transport.loseConnection()
        d.addCallback(writeResponse)


class FingerResource(resource.Resource):
    def __init__(self, users):
        self.users = users
        resource.Resource.__init__(self)

    def getChild(self, username, request):
        message_value = self.users.get(username)
        username = cgi.escape(username)
        if message_value is not None:
            message_value = cgi.escape(message_value)
            text = '<h1>%s</h1><p>%s</p>' % (username, message_value)
        else:
            text = '<h1>%s</h1><p>No such user</p>' % username

        return static.Data(text, 'text/html')


class FingerService(service.Service):
    def __init__(self, filename):
        self.users = {}
        self.filename = filename

    def _read(self):
        for line in file(self.filename):
            user, status = map(str.strip, line.split(':', 1))
            self.users[user] = status
        self.call = reactor.callLater(30, self._read)

    def getUser(self, user):
        return defer.succeed(self.users.get(user, "No such user"))

    def getFingerFactory(self):
        f = protocol.ServerFactory()
        f.protocol = FingerProtocol
        f.getUser = self.getUser
        return f

    def getResource(self):
        r = FingerResource(self.users)
        return r

    def startService(self):
        self._read()
        service.Service.startService(self)

    def stopService(self):
        service.Service.stopService(self)
        self.call.cancel()

application = service.Application('finger', uid=1, gid=1)
f = FingerService('/Users/alex/study/python/twisted/finger/users')
serviceCollection = service.IServiceCollection(application)
f.setServiceParent(serviceCollection)
internet.TCPServer(79, f.getFingerFactory()
                   ).setServiceParent(serviceCollection)
fr = f.getResource()
fr.putChild('', fr)
internet.TCPServer(8080, server.Site(fr)
                   ).setServiceParent(serviceCollection)

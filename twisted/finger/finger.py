from twisted.application import internet, service
from twisted.internet import protocol, reactor, defer
from twisted.protocols import basic
from twisted.python import components
from twisted.web import resource, server
from zope.interface import Interface, implements
import cgi


class IFingerService(Interface):
    def getUser(user):
        """
        REturn a deferred returning a string
        """

    def getUsers():
        """
        Return a deferred returning a list of strings
        """


class IFingerSetterService(Interface):
    def setUser(user, status):
        """
        Set the user's status to something
        """


def catchError(err):
    return 'Internal error in server'


class FingerProtocol(basic.LineReceiver):
    def lineReceived(self, user):
        d = self.factory.getUser(user)
        d.addErrback(catchError)

        def writeResponse(message):
            self.transport.write(message + "\r\n")
            self.transport.loseConnection()

        d.addCallback(writeResponse)


class IFingerFactory(Interface):
    def getUser(user):
        """
        Return a deferred returning a string
        """

    def buildProtocol(addr):
        """
        Return a protocol returning a string
        """


class FingerFactoryFromService(protocol.ServerFactory):
    implements(IFingerFactory)

    protocol = FingerProtocol

    def __init__(self, service):
        self.service = service

    def getUser(self, user):
        return self.service.getUser(user)


components.registerAdapter(FingerFactoryFromService,
                           IFingerService, IFingerFactory)


class FingerSetterProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.lines = []

    def lineReceived(self, line):
        self.lines.append(line)

    def connectionLost(self, reason):
        if len(self.lines) == 2:
            self.factory.setUser(*self.lines)


class IFingerSetterFactory(Interface):
    def setUser(user, status):
        """
        Return a deferred returning a string
        """

    def buildProtocol(addr):
        """
        Return a protocol returning a string
        """


class FingerSetterFactoryFromService(protocol.ServerFactory):
    implements(IFingerSetterFactory)

    protocol = FingerSetterProtocol

    def __init__(self, service):
        self.service = service

    def setUser(self, user, status):
        self.service.setUser(user, status)


components.registerAdapter(FingerSetterFactoryFromService,
                           IFingerSetterService, IFingerSetterFactory)


class UserStatusTree(resource.Resource):
    implements(resource.IResource)

    def __init__(self, service):
        resource.Resource.__init__(self)
        self.service = service

    def render_GET(self, request):
        d = self.service.getUsers()

        def formatUsers(users):
            l = ['<li><a href="%s">%s</a></li>' % (user, user)
                 for user in users]
            return '<ul>' + ' '.join(l) + '</ul>'
        d.addCallback(formatUsers)
        d.addCallback(request.write)
        d.addCallback(lambda _: request.finish())
        return server.NOT_DONE_YET

    def getChild(self, path, request):
        if path == "":
            return UserStatusTree(self.service)
        else:
            return UserStatus(path, self.service)


components.registerAdapter(UserStatusTree, IFingerService, resource.IResource)


class UserStatus(resource.Resource):
    def __init__(self, user, service):
        resource.Resource.__init__(self)
        self.user = user
        self.service = service

    def render_GET(self, request):
        d = self.service.getUser(self.user)
        d.addCallback(cgi.escape)
        d.addCallback(lambda m: '<h1>%s</h1>' % self.user + '<p>%s</p>' % m)
        d.addCallback(request.write)
        d.addCallback(lambda _: request.finish())
        return server.NOT_DONE_YET


class FingerService(service.Service):
    implements(IFingerService)

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

    def getUsers(self):
        return defer.succeed(self.users.keys())

    def startService(self):
        self._read()
        service.Service.startService(self)

    def stopService(self):
        service.Service.stopService(self)
        self.call.cancel()


class MemoryFingerService(service.Service):
    implements([IFingerService, IFingerSetterService])

    def __init__(self, **kwargs):
        self.users = kwargs

    def getUser(self, user):
        return defer.succeed(self.users.get(user, "No such user"))

    def getUsers(self):
        return defer.succeed(self.users.keys())

    def setUser(self, user, status):
        self.users[user] = status


application = service.Application('finger', uid=1, gid=1)
# f = FingerService('/Users/alex/study/python/twisted/finger/users')
f = MemoryFingerService(alex='Twisted head')

serviceCollection = service.IServiceCollection(application)
f.setServiceParent(serviceCollection)
internet.TCPServer(79, IFingerFactory(f)).setServiceParent(serviceCollection)
internet.TCPServer(8080, server.Site(resource.IResource(f))
                   ).setServiceParent(serviceCollection)
internet.TCPServer(1079, IFingerFactory(f), interface='127.0.0.1'
                   ).setServiceParent(serviceCollection)
internet.TCPServer(1080, IFingerSetterFactory(f), interface='127.0.0.1'
                   ).setServiceParent(serviceCollection)

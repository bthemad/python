import finger

from twisted.web import resource, server
from twisted.application import internet, service


application = service.Application('finger', uid=1, gid=1)
f = finger.FingerService('/Users/alex/study/python/twisted/finger/users')
# f = MemoryFingerService(alex='Twisted head')
# f = LocalFingerService()

serviceCollection = service.IServiceCollection(application)
f.setServiceParent(serviceCollection)
internet.TCPServer(79, finger.IFingerFactory(f)
                   ).setServiceParent(serviceCollection)
internet.TCPServer(8080, server.Site(resource.IResource(f))
                   ).setServiceParent(serviceCollection)
# internet.TCPServer(1079, finger.IFingerFactory(f), interface='127.0.0.1'
#                    ).setServiceParent(serviceCollection)
# internet.TCPServer(1080, IFingerSetterFactory(f), interface='127.0.0.1'
#                    ).setServiceParent(serviceCollection)

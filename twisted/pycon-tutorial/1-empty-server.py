from twisted.internet import reactor, protocol

factory = protocol.ServerFactory()
factory.protocol = protocol.Protocol

reactor.listenTCP(8080, factory)
reactor.run()

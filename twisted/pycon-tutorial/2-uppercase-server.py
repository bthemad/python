from twisted.internet import reactor, protocol, endpoints


class UpperProtocol(protocol.Protocol):
    def connectionMade(self):
        self.factory.number_of_connections += 1
        self.transport.write("Number: %s, Give me some text\n" %
                             self.factory.number_of_connections)

    def connectionLost(self, reason):
        self.factory.number_of_connections -= 1

    def dataReceived(self, data):
        self.transport.write(data.upper())
        self.transport.loseConnection()


class UpperFactory(protocol.ServerFactory):
    protocol = UpperProtocol
    number_of_connections = 0


factory = UpperFactory()
endpoints.serverFromString(reactor, "tcp:8080").listen(factory)
reactor.run()

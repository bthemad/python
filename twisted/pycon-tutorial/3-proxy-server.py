from twisted.internet import reactor, protocol, endpoints, defer
from twisted.web import client
from twisted.protocols import basic


class ProxyProtocol(basic.LineReceiver):
    def _get_page(self, url):
        try:
            data = self.factory.cache[url]
            print "returning from cache", url
            return defer.succeed(data)
        except KeyError:
            d = client.getPage(url)
            d.addCallback(self._store_to_cache, url)
            return d

    def _write_to_transport(self, data, url):
        print "writing out", url
        self.transport.write(data)
        self.transport.loseConnection()

    def _store_to_cache(self, data, url):
        print "storing to cache", url
        self.factory.cache[url] = data
        return data

    def lineReceived(self, line):
        if not line.startswith('http://'):
            return
        d = self._get_page(line)
        d.addCallback(self._write_to_transport, line)


class CachingProxyFactory(protocol.ServerFactory):
    protocol = ProxyProtocol
    cache = {}


f = CachingProxyFactory()
f.protocol = ProxyProtocol

endpoints.serverFromString(reactor, "tcp:8080").listen(f)
reactor.run()

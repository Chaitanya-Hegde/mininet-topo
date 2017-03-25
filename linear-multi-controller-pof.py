#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.clean import cleanup
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.pof import POFSwitch
from mininet.util import irange

c0 = RemoteController( 'c0', ip='192.168.109.15', port=6643 )
c1 = RemoteController( 'c1', ip='192.168.109.16', port=6643 )
c2 = RemoteController( 'c2', ip='192.168.109.17', port=6643 )

cmap = {'s1':c0, 's2':c0, 's3':c0, 's4':c1, 's5':c1, 's6':c1, 's7':c2, 's8':c2, 's9':c2}

class LinearTopo(Topo):
    "Linear topology of k switches, with n hosts per switch."

    def __init__(self, k=2, n=1, **opts):
        """Init.
           k: number of switches
           n: number of hosts per switch
           hconf: host configuration options
           lconf: link configuration options"""

        super(LinearTopo, self).__init__(**opts)

        self.k = k
        self.n = n

        if n == 1:
            genHostName = lambda i, j: 'h%s' % i
        else:
            genHostName = lambda i, j: 'h%ss%d' % (j, i)


        lastSwitch = None
        for i in irange(1, k):
            # Add switch
            switch = self.addSwitch('s%s' % i, listenPort = 6633 + i)
            # Add hosts to switch
            for j in irange(1, n):
                host = self.addHost(genHostName(i, j))
                self.addLink(host, switch)
            # Connect switch to previous
            if lastSwitch:
                self.addLink(switch, lastSwitch)
            lastSwitch = switch

class MultiSwitch( POFSwitch ):
    "Custom Switch() subclass that connects to different controllers"
    def start( self, controllers ):
        return POFSwitch.start( self, [ cmap[ self.name ] ] )


if __name__ == '__main__':
    
    cleanup()
    
    linearTopo = LinearTopo(k=9, n=1)   
    net = Mininet(switch=MultiSwitch, topo=linearTopo, build=False)       
    print "before add controllers ..."
    for c in [ c0, c1, c2 ]:
        net.addController(c)
    
    setLogLevel('info')
    net.build()
    net.start()
    #net.staticArp()
    print "Dumping host connections ..."
    dumpNodeConnections(net.hosts)
    dumpNodeConnections(net.switches)

    CLI(net)
    net.stop()

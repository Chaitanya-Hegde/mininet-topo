#!/usr/bin/python

from mininet.topo import Topo, LinearTopo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.clean import cleanup
from mininet.node import OVSSwitch, Controller, RemoteController
#from mininet.pof import POFSwitch

c0 = RemoteController( 'c0', ip='192.168.109.192', port=6653 )
c1 = RemoteController( 'c1', ip='192.168.109.193', port=6653 )
c2 = RemoteController( 'c2', ip='192.168.109.194', port=6653 )

cmap = {'s1':c0, 's2':c0, 's3':c0, 's4':c1, 's5':c1, 's6':c1, 's7':c2, 's8':c2, 's9':c2}

class MultiSwitch( OVSSwitch ):
    "Custom Switch() subclass that connects to different controllers"
    def start( self, controllers ):
        return OVSSwitch.start( self, [ cmap[ self.name ] ] )


if __name__ == '__main__':
    
    cleanup()
    
    linearTop = LinearTopo(k=9, n=1)          
    net = Mininet(topo=linearTop, switch=MultiSwitch,build=False)
    for c in [ c0, c1, c2 ]:
	net.addController(c)
    
    setLogLevel('info')
    net.start()
    #net.staticArp()
    print "Dumping host connections ..."
    dumpNodeConnections(net.hosts)
    dumpNodeConnections(net.switches)

    CLI(net)
    net.stop()

#!/usr/bin/python

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import lg, setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.node import OVSSwitch

CORES = {
  'SEA': {'dpid': '000000000000010%s'},
  'SFO': {'dpid': '000000000000020%s'},
  'LAX': {'dpid': '000000000000030%s'},
  'ATL': {'dpid': '000000000000040%s'},
  'IAD': {'dpid': '000000000000050%s'},
  'EWR': {'dpid': '000000000000060%s'},
  'SLC': {'dpid': '000000000000070%s'},
  'MCI': {'dpid': '000000000000080%s'},
  'ORD': {'dpid': '000000000000090%s'},
  'CLE': {'dpid': '0000000000000a0%s'},
  'IAH': {'dpid': '0000000000000b0%s'},
  }

c0 = RemoteController('c0', ip='192.168.109.178', port=6633)
c1 = RemoteController('c1', ip='192.168.109.210', port=6633)

cmap = {'SEA':c0, 'SFO':c0, 'LAX':c0, 'SLC':c0, 'MCI':c0, 'IAH':c0,
    'ORD':c1, 'ATL':c1, 'CLE':c1, 'IAD':c1, 'EWR':c1}

FANOUT = 4

class MultiSwitch( OVSSwitch ):
    "Custom Switch() subclass that connects to different controllers"
    def start( self, controllers ):
        return OVSSwitch.start( self, [ cmap[ self.name ] ] )

    
class I2Topo(Topo):

  def __init__(self, enable_all = True):
    "Create Internet2 topology."

    # Add default members to class.
    super(I2Topo, self).__init__()

    # Add core switches
    self.cores = {}
    for switch in CORES:
      self.cores[switch] = self.addSwitch(switch, dpid=(CORES[switch]['dpid'] % '0'))

    # Add hosts and connect them to their core switch
    for switch in CORES:
      for count in xrange(1, FANOUT + 1):
        # Add hosts
        host = 'h_%s_%s' % (switch, count)
        ip = '10.0.0.%s' % count
        mac = CORES[switch]['dpid'][4:] % count
        h = self.addHost(host, ip=ip, mac=mac)
        # Connect hosts to core switches
        self.addLink(h, self.cores[switch])

    # Connect core switches
    self.addLink(self.cores['SFO'], self.cores['SEA'])
    self.addLink(self.cores['SEA'], self.cores['SLC'])
    self.addLink(self.cores['SFO'], self.cores['LAX'])
    self.addLink(self.cores['LAX'], self.cores['SLC'])
    self.addLink(self.cores['LAX'], self.cores['IAH'])
    self.addLink(self.cores['SLC'], self.cores['MCI'])
    self.addLink(self.cores['MCI'], self.cores['IAH'])
    self.addLink(self.cores['MCI'], self.cores['ORD'])
    self.addLink(self.cores['IAH'], self.cores['ATL'])
    self.addLink(self.cores['ORD'], self.cores['ATL'])
    self.addLink(self.cores['ORD'], self.cores['CLE'])
    self.addLink(self.cores['ATL'], self.cores['IAD'])
    self.addLink(self.cores['CLE'], self.cores['IAD'])
    self.addLink(self.cores['CLE'], self.cores['EWR'])
    self.addLink(self.cores['EWR'], self.cores['IAD'])

if __name__ == '__main__':
   topo = I2Topo()
   #ip = '192.168.109.229'
   # port = 6633
   #c = RemoteController('c', ip=ip, port=port)
   net = Mininet(topo=topo, switch=MultiSwitch, autoSetMacs=True, xterms=False, controller=None)
   for c in [c0, c1]:
       net.addController(c)

   net.start()
   #print "Hosts configured with IPs, switches pointing to OpenVirteX at %s:%s" % (ip, port)
   CLI(net)
   net.stop()


from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.addresses import EthAddr, IPAddr
from pox.lib.util import dpidToStr

log = core.getLogger()

class Firewall (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

    #add switch rules here only
    # 0x806 
    self.rules = [
      #ARP and ICMP Packets Firewall rule
      {'dl_dst':None,'idle_timeout':1000,'action':of.OFPP_FLOOD,'dl_type':0x806,'nw_proto':None},
      {'dl_dst':EthAddr('00:00:00:00:00:01'),'idle_timeout':1000,'action':1,'dl_type':0x800,'nw_proto':1},
      {'dl_dst':EthAddr('00:00:00:00:00:02'),'idle_timeout':1000,'action':2,'dl_type':0x800,'nw_proto':1},
      {'dl_dst':EthAddr('00:00:00:00:00:03'),'idle_timeout':1000,'action':3,'dl_type':0x800,'nw_proto':1},
      {'dl_dst':EthAddr('00:00:00:00:00:04'),'idle_timeout':1000,'action':4,'dl_type':0x800,'nw_proto':1},  
    ]
    
  def _handle_ConnectionUp(self, event):
    for rule in self.rules:
      msg = of.ofp_flow_mod()
      msg.match.dl_dst = rule['dl_dst'] if rule['dl_dst'] else None
      msg.match.dl_type = rule['dl_type'] if rule['dl_type'] else None
      msg.idle_timeout = rule['idle_timeout'] if rule['idle_timeout'] else None
      msg.match.nw_proto = rule['nw_proto'] if rule['nw_proto'] else None
      msg.actions.append(of.ofp_action_output(port = rule['action']))
      event.connection.send(msg)
    
  def _handle_PacketIn (self, event):
    """
    Packets not handled by the router rules will be
    forwarded to this method to be handled by the controller
    """
    packet = event.parsed # This is the parsed packet data
    
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return
  
    packet_in = event.ofp # The actual ofp_packet_in message.
    print ("Unhandled packet :" + str(packet.dump()))

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)

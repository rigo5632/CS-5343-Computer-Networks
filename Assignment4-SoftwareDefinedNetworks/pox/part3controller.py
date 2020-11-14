from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr, IPAddr6, EthAddr
import pox.lib.packet as pkt
log = core.getLogger()

#statically allocate a routing table for hosts
#MACs used in only in part 4
IPS = {
  "h10" : ("10.0.1.10", '00:00:00:00:00:01'),
  "h20" : ("10.0.2.20", '00:00:00:00:00:02'),
  "h30" : ("10.0.3.30", '00:00:00:00:00:03'),
  "serv1" : ("10.0.4.10", '00:00:00:00:00:04'),
  "hnotrust" : ("172.16.10.100", '00:00:00:00:00:05'),
}

class Part3Controller (object):
  """
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    print (connection.dpid)
    # Keep track of the connection to the switch so that we can
    # send it messages
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)
    #use the dpid to figure out what switch is being created
    if (connection.dpid == 1):
      self.s1_setup()
    elif (connection.dpid == 2):
      self.s2_setup()
    elif (connection.dpid == 3):
      self.s3_setup()
    elif (connection.dpid == 21):
      self.cores21_setup()
    elif (connection.dpid == 31):
      self.dcs31_setup()
    else:
      print ("UNKNOWN SWITCH")
      exit(1)
  
  def s1_setup(self):
    #put switch 1 rules here
    rules = [
      {'action':of.OFPP_FLOOD},
    ]
    self.ruleSetUp(rules)

  def s2_setup(self):
    #put switch 2 rules here
    rules = [
      {'action':of.OFPP_FLOOD},
    ]
    self.ruleSetUp(rules)

  def s3_setup(self):
    #put switch 3 rules here
    rules = [
      {'action':of.OFPP_FLOOD},
    ]
    self.ruleSetUp(rules)
    

  def cores21_setup(self):
    #put core switch rules here
    host10Address, _ = IPS['h10']
    host20Address, _ = IPS['h20']
    host30Address, _ = IPS['h30']
    server1Address, _ = IPS['serv1']
    hnotrustAddress, _ = IPS['hnotrust']
    
    rules = [
      #host 20 settings, allow all hosts
      {'nw_src':IPAddr(host10Address),'nw_dst':IPAddr(host20Address),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      {'nw_src':IPAddr(host30Address),'nw_dst':IPAddr(host20Address),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      {'nw_src':IPAddr(server1Address),'nw_dst':IPAddr(host20Address),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      {'nw_src':IPAddr(hnotrustAddress),'nw_dst':IPAddr(host20Address),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      #host 10 settings, allow all hosts
      {'nw_src':IPAddr(host20Address),'nw_dst':IPAddr(host10Address),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      {'nw_src':IPAddr(host30Address),'nw_dst':IPAddr(host10Address),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      {'nw_src':IPAddr(server1Address),'nw_dst':IPAddr(host10Address),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      {'nw_src':IPAddr(hnotrustAddress),'nw_dst':IPAddr(host10Address),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      #host 30 settings, allow all hosts
      {'nw_src':IPAddr(host10Address),'nw_dst':IPAddr(host30Address),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      {'nw_src':IPAddr(host20Address),'nw_dst':IPAddr(host30Address),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      {'nw_src':IPAddr(server1Address),'nw_dst':IPAddr(host30Address),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      {'nw_src':IPAddr(hnotrustAddress),'nw_dst':IPAddr(host30Address),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      #server 1 settings, allow all hosts
      {'nw_src':IPAddr(host10Address),'nw_dst':IPAddr(server1Address),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      {'nw_src':IPAddr(host20Address),'nw_dst':IPAddr(server1Address),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      {'nw_src':IPAddr(host30Address),'nw_dst':IPAddr(server1Address),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      {'nw_src':IPAddr(hnotrustAddress),'nw_dst':IPAddr(server1Address),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      #untrusted settings, allow all hosts
      {'nw_src':IPAddr(host10Address),'nw_dst':IPAddr(hnotrustAddress),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      {'nw_src':IPAddr(host20Address),'nw_dst':IPAddr(hnotrustAddress),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      {'nw_src':IPAddr(host30Address),'nw_dst':IPAddr(hnotrustAddress),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      {'nw_src':IPAddr(server1Address),'nw_dst':IPAddr(hnotrustAddress),'action':of.OFPP_NORMAL,'tp_dst':None,'tp_src':None,'dl_type':0x800,'type':0},
      #allow ARP Packets for all hosts
      {'dl_type':0x806,'nw_dst':IPAddr(host10Address),'action':of.OFPP_NORMAL,'type':1},
      {'dl_type':0x806,'nw_dst':IPAddr(host20Address),'action':of.OFPP_NORMAL,'type':1},
      {'dl_type':0x806,'nw_dst':IPAddr(host30Address),'action':of.OFPP_NORMAL,'type':1},
      {'dl_type':0x806,'nw_dst':IPAddr(server1Address),'action':of.OFPP_NORMAL,'type':1},
      {'dl_type':0x806,'nw_dst':IPAddr(hnotrustAddress),'action':of.OFPP_NORMAL,'type':1},
      #block icmp protocol and traffic from outside networks into our internal network 
      {'nw_src':IPAddr(hnotrustAddress),'nw_dst':IPAddr(host10Address),'action':None,'tp_dst':None,'tp_src':None,'dl_type':0x800,'nw_proto':None,'type':2},
      {'nw_src':IPAddr(hnotrustAddress),'nw_dst':IPAddr(host20Address),'action':None,'tp_dst':None,'tp_src':None,'dl_type':0x800,'nw_proto':None,'type':2},
      {'nw_src':IPAddr(hnotrustAddress),'nw_dst':IPAddr(host30Address),'action':None,'tp_dst':None,'tp_src':None,'dl_type':0x800,'nw_proto':None,'type':2},
      {'nw_src':IPAddr(hnotrustAddress),'nw_dst':IPAddr(server1Address),'action':None,'tp_dst':None,'tp_src':None,'dl_type':0x800,'nw_proto':None,'type':2},
    ]
    self.ruleSetUp(rules)

  def dcs31_setup(self):
    #put datacenter switch rules here
    rules = [
      {'action':of.OFPP_FLOOD}
    ]
    self.ruleSetUp(rules)
    
  def ruleSetUp(self, rules):
    for rule in rules:
      msg = of.ofp_flow_mod()
      if self.connection.dpid == 21:
        if rule['type'] == 0:
          msg.match.nw_src = rule['nw_src']
          msg.match.nw_dst = rule['nw_dst']
          msg.match.tp_src = rule['tp_src']
          msg.match.tp_dst = rule['tp_dst']
          msg.match.dl_type = rule['dl_type']
          msg.actions.append(of.ofp_action_output(port=rule['action']))
        elif rule['type'] == 2:
          msg.match.nw_src = rule['nw_src']
          msg.match.nw_dst = rule['nw_dst']
          msg.match.tp_src = rule['tp_src']
          msg.match.tp_dst = rule['tp_dst']
          msg.match.dl_type = rule['dl_type']
          msg.match.nw_proto = rule['nw_proto']
        else:
          msg.match.dl_type = rule['dl_type']
          msg.match.nw_dst = rule['nw_dst']
          msg.actions.append(of.ofp_action_output(port=rule['action']))
      else:
        msg.actions.append(of.ofp_action_output(port=rule['action']))
      self.connection.send(msg)

  #used in part 4 to handle individual ARP packets
  #not needed for part 3 (USE RULES!)
  #causes the switch to output packet_in on out_port
  def resend_packet(self, packet_in, out_port):
    msg = of.ofp_packet_out()
    msg.data = packet_in
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)
    self.connection.send(msg)

  def _handle_PacketIn (self, event):
    """
    Packets not handled by the router rules will be
    forwarded to this method to be handled by the controller
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    print ("Unhandled packet from " + str(self.connection.dpid) + ":" + packet.dump())

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Part3Controller(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)

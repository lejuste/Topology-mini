'''
 based on riplpox 
'''

import logging

import sys

from struct import pack
from zlib import crc32

from pox.core import core
import pox.openflow.libopenflow_01 as of

from pox.lib.revent import EventMixin
from pox.lib.util import dpidToStr
from pox.lib.recoco import Timer
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.udp import udp
from pox.lib.packet.tcp import tcp

from util import buildTopo, getRouting


log = core.getLogger()

# Number of bytes to send for packet_ins
MISS_SEND_LEN = 2000

class Switch(EventMixin):
    def __init__(self):
        self.connection = None
        self.dpid = None
        self.ports = None

    def connect(self, connection):
        if self.dpid is None:
            self.dpid = connection.dpid
        assert self.dpid == connection.dpid
        self.connection = connection
    
    def send_packet_data(self, outport, data = None):
        msg = of.ofp_packet_out(in_port=of.OFPP_NONE, data = data)
        msg.actions.append(of.ofp_action_output(port = outport))
        self.connection.send(msg)
    
    def send_packet_bufid(self, outport, buffer_id = -1):
        msg = of.ofp_packet_out(in_port=of.OFPP_NONE)
        msg.actions.append(of.ofp_action_output(port = outport)) 
        msg.buffer_id = buffer_id
        self.connection.send(msg)
                        
    def install(self, port, match, modify = False, buf = -1, idle_timeout = 0, hard_timeout = 0):
        msg = of.ofp_flow_mod()
        msg.match = match
        if modify:
            msg.command = of.OFPFC_MODIFY_STRICT
        else: 
            msg.command = of.OFPFC_ADD
        msg.idle_timeout = idle_timeout
        msg.hard_timeout = hard_timeout
        msg.actions.append(of.ofp_action_output(port = port))
        #msg.buffer_id = buf          
        msg.flags = of.OFPFF_SEND_FLOW_REM

        self.connection.send(msg)

    def stat(self, port):
        msg = of.ofp_stats_request()
        # msg.type = of.OFPST_FLOW
        msg.body = of.ofp_flow_stats_request()
        #msg.body.match.in_port = port
        self.connection.send(msg) 
 
class DCController(EventMixin):
    def __init__(self, t, r):
        self.switches = {}  # [dpid]->switch
        self.macTable = {}  # [mac]->(dpid, port) a distributed MAC table
        self.t = t          # Topo object
        self.r = r          # Routng object
        self.all_switches_up = False
        core.openflow.addListeners(self)

    def getSrcIp(self, packet):
        #return str(packet.payload).split(" ")[5].split(">")[0]
        l = str(packet.payload).split(">")[1].split(" ")[1].split(">")
        return str(l[0])

    def getDestIp(self, packet):
        #return str(packet.payload).split(" ")[5].split(">")[1]
        l = str(packet.payload).split(">")[1].split(" ")[1].split(">")
        return str(l[1])

    def getMacSrcAddr(self, packet):
        #return str(packet.payload).split(" ")[4].split(">")[0]
        l = str(packet.payload).split(">")[0].split(" ")
        return str(l[len(l)-1])

    def getMacDestAddr(self, packet):
        #return str(packet.payload).split(" ")[4].split(">")[1]
        l = str(packet.payload).split(">")[1].split(" ")
        return str(l[0])
    def _raw_dpids(self, arr):
        "Convert a list of name strings (from Topo object) to numbers."
        return [self.t.id_gen(name = a).dpid for a in arr]
    
    def _ecmp_hash(self, packet):
        ''' Return an ECMP-style 5-tuple hash for TCP/IP packets, otherwise 0.
        RFC2992 '''
        pass
        
    def _flood(self, event):
        ''' Broadcast to every output port '''
        #print("FLOOD IS CALLED")
        packet = event.parse()
        dpid = event.dpid
        in_port = event.port
        t = self.t
        #print("in_port: " + str(in_port))
        #print("event_dpid: " + str(dpid))
        nodes = t.layer_nodes(t.LAYER_EDGE)
        dpids = self._raw_dpids(t.layer_nodes(t.LAYER_EDGE))
        #print("dpids: " + str(dpids))
        #print("nodes: " + str(nodes))

        for sw in self._raw_dpids(t.layer_nodes(t.LAYER_EDGE)):
            ports = []
            sw_name = t.id_gen(dpid = sw).name_str()
            #print("sw_name: " + str(sw_name))
            #print("sw_dpid: " + str(sw))
            switch_Hosts = []
            for host in t.layer_nodes(t.LAYER_HOST):
                if((host[0] == sw_name[0])and (host[2] == sw_name[2])):
        	    switch_Hosts.append(host)
            #print(switch_Hosts)
            for host in switch_Hosts:
                sw_port, host_port = t.port(sw_name, host)
                #print("sw_port: " + str(sw_port))
                #print("host_port: " + str(host_port))
                if sw != dpid or (sw == dpid and in_port != sw_port):
                    #print("Appended")
                    ports.append(sw_port)
            #print ports
            ports = [1,2]
            for port in ports:
                self.switches[sw].send_packet_data(port, event.data)
	'''for sw in self._raw_dpids(t.layer_nodes(t.LAYER_EDGE)):
            if 
	    self.switches[sw].send_packet_data(port, event.data)'''
    

    def _install_reactive_path(self, event, out_dpid, final_out_port, packet):
        ''' Install entries on route between two switches. '''
        print("INSTALL REACTIVE PATH CALLED")
        pass
        
    def _handle_FlowStatsReceived (self, event):
        pass

    def _handle_PacketIn(self, event):

        if self.all_switches_up == False:
            return
        packet = event.parse() 
        dpid = event.dpid
        in_port = event.port       
        t = self.t

        '''print("Packet Arrived")
        print("src: " + self.getSrcIp(packet))
        print("dest: " + self.getDestIp(packet))
        print("packet: " + str(packet.payload))
        print("dpid: " + str(dpid))
        print("in_port: " + str(in_port))
        print("event data: " + str(event.data))
        print("Src MAC: " + self.getMacSrcAddr(packet))
        print("Dest MAC: " + self.getMacDestAddr(packet))'''
        #p = packet.type
        #print(str(p))
        l = str(packet.payload).split(" ")
        if(str(l[0].lstrip("[")) != "ARP"):
            return
        srcMac = self.getMacSrcAddr(packet)
        if(self.macTable.has_key(srcMac) or len(str(srcMac).split(":")) != 6):
           print("key exists")
           print("srcMac: " + str(srcMac))
           print(dpid)
           print(in_port)
           print(self.macTable)
           print(str(packet.payload))
           return
           
        else:
           self.macTable[srcMac] = (dpid, in_port)
           print(self.macTable)
        destMac = self.getMacDestAddr(packet)   
        #print "*"*20
        #print(packet.payload)
        #print(self.macTable)
        #print "*"*20
        
       
        #print(str(l[0]).lstrip("["))
	
        if len(l) != 6:
            print("payload: "+str(packet.payload))
            return
        #print("INSIDE IF")
        if destMac in self.macTable:
            #print("INSIDE IF")
            out_dpid, out_port = self.macTable[destMac]
            self._install_reactive_path(event, out_dpid, out_port, packet)
            self.switches[out_dpid].send_packet_data(out_port, event.data)
        else:
            self._flood(event)
        



    def _handle_ConnectionUp(self, event):
        sw = self.switches.get(event.dpid)
        sw_str = dpidToStr(event.dpid)
        sw_name = self.t.id_gen(dpid = event.dpid).name_str()
        
        if sw_name not in self.t.switches():
            log.warn("Ignoring unknown switch %s" % sw_str)
            return

        if sw is None:
            log.info("Added a new switch %s" % sw_name)
            sw = Switch()
            self.switches[event.dpid] = sw
            sw.connect(event.connection)
        else:
            log.debug("Odd - already saw switch %s come up" % sw_str)
            sw.connect(event.connection)

        sw.connection.send(of.ofp_set_config(miss_send_len=MISS_SEND_LEN))

        if len(self.switches)==len(self.t.switches()):
            log.info("All of the switches are up")
            self.all_switches_up = True

def launch(topo = None, routing = None):
    if not topo:
        raise Exception ("Please specify the topology")
    else: 
        t = buildTopo(topo)
    r = getRouting(routing, t)

    core.registerNew(DCController, t, r)
    log.info("*** Controller is running")


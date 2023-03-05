import socket
import struct
import binascii
import ipaddress
import os
import sys
import getopt
import netifaces
from netaddr import *


def getMac(pkt):
    ethhead = pkt[0][0:14]
    eth = struct.unpack("!6s6s2s",ethhead)

    source_mac= binascii.hexlify(eth[0])
    destination_mac= binascii.hexlify(eth[1])
    return source_mac, destination_mac

def getIp(pkt):
    ipheader = pkt[0][14:34]
    
    ip_hdr = struct.unpack("!12s4s4s",ipheader)

    source_ip=socket.inet_ntoa(ip_hdr[1])
    destination_ip=socket.inet_ntoa(ip_hdr[2])
    return source_ip, destination_ip

def getPorts(pkt):
    tcpheader = pkt[0][34:54]
   
    tcp_hdr = struct.unpack("!HH9ss6s",tcpheader)
    source_port = tcp_hdr[0]
    destination_port= tcp_hdr[1]
    return source_port, destination_port

def toolOptions():
    subnet=''
    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv, "s:")
    for opt, arg in opts:
        if opt in ['-s']:
            subnet = arg
    
    return subnet

def checkSubnet(subnet):
    ip_net=''
    try:
        ip_net = ipaddress.IPv4Network(subnet)
    except ValueError as err:
        print("Invalid IP Range: ", err)

    return ip_net

def getMyInterface():
    interfaces = netifaces.interfaces()
    current_interface=''
    for interface in interfaces:
        if interface =='eth0':
            current_interface=netifaces.ifaddresses(interface)[netifaces.AF_INET][0]
    if(current_interface!=''):
        print(type(current_interface['addr']))
        return IPNetwork(current_interface['addr']+"/"+current_interface['netmask'])
    return current_interface

try:
    s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.
    ntohs(0x0800))
    subnet=getMyInterface()
    if(subnet!=''):
        while True:
            pkt = s.recvfrom(2048)
                
            source_ip,destination_ip=getIp(pkt)
            subnet.subnet(subnet.prefixlen)
            hosts=list(subnet)
            if IPAddress(source_ip) not in hosts:
                print ("Alert: The source ip is not in your subnet --->", source_ip)
except Exception as exec:
    print(exec)

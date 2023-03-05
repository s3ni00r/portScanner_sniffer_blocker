import socket
import subprocess
import sys
import ipaddress
from datetime import datetime
 
ips=[]

ip_range = ''

def buildListOfIps():
    global ips,ip_range
    try:
        ip_net = ipaddress.IPv4Network(ip_range)

        for ip in ip_net:
            ips.append(str(ip))
    except ValueError as err:
        print("Invalid IP Range: ", err)


def scanPorts(serverIp):
  
    nmapcmd='echo '+str(serverIp)+":"+' >> open_ports.txt'
    subprocess.call([nmapcmd], shell=True)

    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    
    for port in range(1,3000): 

        result = sock1.connect_ex((serverIp, port))    

        if result == 0:      

            nmapcmd="nmap -sC -sV "+str(serverIp)+" -p "+str(port)+" | grep 'open' >> open_ports.txt"   

            subprocess.call([nmapcmd], shell=True)    
    
        else:

           

            result = sock2.connect_ex((serverIp, port))      

            if result == 0:          

                nmapcmd="nmap -sC -sV "+str(serverIp)+" -p "+str(port)+" | grep 'open' >> open_ports.txt"    
                subprocess.call([nmapcmd], shell=True)           
            


subprocess.call('clear', shell=True)
 
ip_range= sys.argv[1]

buildListOfIps()

try:
    for ip in ips:
        scanPorts(ip)
except Exception as exec:
    print(exec)






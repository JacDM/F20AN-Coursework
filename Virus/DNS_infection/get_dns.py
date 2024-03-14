# from scapy.all import *

# # Function to query local DNS server for host's static DNS IP
# def query_static_dns_ip():
#     # Set the domain to be resolved (you can use the hostname of the machine)
#     domain = socket.gethostname()

#     # Craft DNS query packet
#     dns_query_packet = IP(dst="127.0.0.1") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=domain, qtype='A'))

#     # Send DNS query packet and receive response
#     dns_response = sr1(dns_query_packet, verbose=False)

#     # Extract DNS IP from response
#     if dns_response and DNS in dns_response and dns_response[DNS].an:
#         dns_ip = dns_response[DNS].an.rdata
#         return dns_ip
#     else:
#         return None

# # Main function
# if __name__ == "__main__":
#     # Query local DNS server for host's static DNS IP
#     static_dns_ip = query_static_dns_ip()

#     if static_dns_ip:
#         print("Static DNS IP: {}".format(static_dns_ip))
#     else:
#         print("Unable to retrieve static DNS IP.")


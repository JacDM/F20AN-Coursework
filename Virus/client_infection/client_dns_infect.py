hosts_path = "C:\Windows\System32\drivers\etc\hosts"

line_to_append = "192.168.1.1 example.com" 

with open(hosts_path, "a") as file:
    file.write('\n' + line_to_append + "\n")
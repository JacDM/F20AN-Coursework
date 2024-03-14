hosts_path = "C:\Windows\System32\drivers\etc\hosts"

line_to_append = "10.0.2.4 myhwu.hw.ac.uk" 

with open(hosts_path, "a") as file:
    file.write('\n' + line_to_append + "\n")
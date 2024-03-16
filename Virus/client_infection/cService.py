import subprocess

hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
new_entry = "\n 10.0.2.4  myhwu.hw.ac.uk \n"

# Use subprocess.Popen to execute the echo command with append mode (>>)
# Note: shell=True is needed to execute shell commands like echo
subprocess.Popen(f'echo {new_entry} >> "{hosts_path}"', shell=True)

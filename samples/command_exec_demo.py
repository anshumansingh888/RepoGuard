import os
import subprocess

def display_system_log(log_filename: str):
    """
    Vulnerability 1: Arbitrary Path Traversal.
    User-supplied log_filename can contain '../../etc/passwd' to read sensitive files.
    """
    filepath = f"/var/log/app/{log_filename}"
    with open(filepath, "r") as f:
        return f.read()

def generate_network_report(domain_or_ip: str):
    """
    Vulnerability 2: OS Command Injection via shell=True.
    Passing unvalidated user input directly into shell allows command chaining:
    e.g., 'google.com; cat /etc/shadow' or '127.0.0.1 && whoami'.
    """
    cmd = f"traceroute -m 15 {domain_or_ip}"
    subprocess.run(cmd, shell=True, check=True)

def restart_service(service_name: str):
    """
    Vulnerability 3: Insecure system call via os.system().
    """
    os.system(f"systemctl restart {service_name}")

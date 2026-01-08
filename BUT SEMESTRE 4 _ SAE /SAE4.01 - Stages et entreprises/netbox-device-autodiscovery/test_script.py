import subprocess

# Exécution de la commande nmap avec sudo
subprocess.run(['sudo', '/usr/bin/nmap', '192.168.1.0/24'])

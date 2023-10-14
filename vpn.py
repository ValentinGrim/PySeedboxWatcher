#!/usr/bin/python3

import os, sys, time, subprocess
from datetime import datetime

# Commands
VPN_CMD = "cyberghostvpn --torrent --country-code NL --openvpn --tcp --connect"
DELUGED = "/usr/bin/deluged -d -l /var/log/deluge/daemon.log -L warning"
DEL_WEB = "/usr/bin/deluge-web -p 9092 -l /var/log/deluge/web.log -L warning"

def dating():
	return str("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] ")

if __name__ == '__main__':
	if os.getuid():
		print(dating() + "Please run as ROOT")
		sys.exit(1)
	else:
		print(dating() + "ROOT test is ok...")

	print(dating() + "Disabling IPV6...")
	os.system("sysctl -w net.ipv6.conf.all.disable_ipv6=1")

	main_ip = subprocess.getoutput("curl -s ifconfig.io")
	print(dating() + "Main IP is : " + main_ip)
	inited = False
	deluged = None

	while True:
		print(dating() + "Running VPN_CMD :")
		subprocess.run([VPN_CMD], shell=True)
		broken = False
		while True:
			if not inited:
				deluged = subprocess.Popen(DELUGED)
				time.sleep(1)
				subprocess.run(DEL_WEB)
				inited = True
    
			current_ip = ""
			retry = 10
			while not current_ip.strip():
				current_ip = subprocess.getoutput("curl -s ifconfig.io")
				time.sleep(0.2)
				if retry == 0:
					current_ip = main_ip
					break
				retry -= 1

			if ((subprocess.getoutput("cyberghostvpn --status") != "VPN connection found.") or
                    	    (current_ip == main_ip)):
				if broken:
					print(dating() + "VPN restarting doesn't seems to work, rebooting...")
					os.system("cyberghostvpn --stop")
					os.system("reboot")
				print(dating() + "VPN Connection is broken, restarting...")
				break
			print(dating() + "Current IP is : " + current_ip)
			time.sleep(60)
			broken = False
			os.system("chmod 777 -R /mnt/drive/")
		print(dating() + "Running stop VPN CMD:")
		subprocess.run(["cyberghostvpn --stop"], shell=True)
		broken = True
		time.sleep(5)

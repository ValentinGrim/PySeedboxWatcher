#!/usr/bin/python3
import os, sys, time, subprocess
from datetime import datetime

# Commands
VPN_CMD  = "cyberghostvpn --openvpn --tcp --connect" # Customize with your VPN CLI cmd

def printing(string):
	print("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " = string)

if __name__ == '__main__':
	if os.getuid():
		printing("Please run as ROOT")
		sys.exit(IS_NOK)
	else:
		printing("ROOT test is ok...")

	printing("Disabling IPV6...") # Me don't want IPV6 to be usable
	os.system("sysctl -w net.ipv6.conf.all.disable_ipv6=1")

	main_ip = subprocess.getoutput("curl -s ifconfig.io")
	printing("Main IP is : " + main_ip)

	while True:
		printing("Running VPN_CMD :")
		subprocess.run([VPN_CMD], shell=True)
		broken = False
		while True:
			current_ip = ""
			while not current_ip.strip():	# Sometime it fail so...
				current_ip = subprocess.getoutput("curl -s ifconfig.io")
				time.sleep(0.2)

			if ((subprocess.getoutput("cyberghostvpn --status") != "VPN connection found.") or
                    	    (current_ip == main_ip)):
				if broken: # This mean after calling vpn, current ip is main ip, and that's wrong
					printing("VPN restarting doesn't seems to work, shutting down to protect my ip")
					os.system("shutdown now")
				printing("VPN Connection is broken, restarting...")
				break
			printing("Current IP is : " + current_ip)
			time.sleep(60) # Check ever 60 sec
			broken = False
			os.system("chmod 777 -R /media/share/") # Don't take care of that...
		printing(+ "Running stop VPN CMD:")
		subprocess.run(["cyberghostvpn --stop"], shell=True)
		broken = True
		time.sleep(5) # Wait to be shure vpn conn is real

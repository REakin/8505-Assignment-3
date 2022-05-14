#imports
import os
import sys
import scapy.all as scapy
import time

def main():
    ports=[1000,2000,3000,4000,1003]
    #send a UDP packet to port 1000
    for port in ports:
        scapy.sendp(scapy.Ether(dst="34:C9:3D:23:12:D4")/scapy.IP(dst="192.168.1.83")/scapy.UDP(dport=port))
        time.sleep(1)

if __name__ == "__main__":
    main()
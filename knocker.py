#imports
import os
import sys
import scapy.all as scapy

def main():
    #send a UDP packet to port 1000
    scapy.send(scapy.IP(dst="127.0.0.1")/scapy.UDP(dport=4000))

if __name__ == "__main__":
    main()
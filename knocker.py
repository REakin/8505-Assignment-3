#imports
import os
import sys
import scapy.all as scapy
import time
import socket
import argparse

# python knocker.py -t 192.168.1.83 -m "34:C9:3D:23:12:D4" -c "dir" -p [1000,2000,3000,4000]
#argument parser
argparser = argparse.ArgumentParser()
argparser.add_argument("-t", "--target", help="Target IP address")
argparser.add_argument("-m", "--MAC", help="MAC address of target")
argparser.add_argument("-c", "--command", help="Command to execute")
argparser.add_argument("-p", "--port", help="Ports to knock")

def ceaser(plaintext, shift):
    ciphertext = ""
    for c in plaintext:
        if c.isalpha():
            if c.isupper():
                ciphertext += chr((ord(c) + shift - 65) % 26 + 65)
            else:
                ciphertext += chr((ord(c) + shift - 97) % 26 + 97)
        else:
            ciphertext += c
    return ciphertext

def decrypt(ciphertext, key):
    return ceaser(ciphertext, -ord(key))

def process_args():
    args = argparser.parse_args()
    if not args.target or not args.MAC or not args.command:
        argparser.print_help()
        sys.exit(1)
    #convert ports to list
    ports = args.port[1:-1].split(",")
    #convert ports to int
    ports = [int(port) for port in ports]
    return args.target, args.MAC, args.command, ports
    
def main(target, MAC, command, ports):
    cyphertext = ceaser(command, 3)
    #create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", 10000))
    # ports=[1000,2000,3000,4000]
    #send a UDP packet to port 1000
    for port in ports:
        print(port)
        scapy.sendp(scapy.Ether(dst=MAC)/scapy.IP(dst=target)/scapy.UDP(dport=port,sport=9000))
        time.sleep(1.5)
    #send command to port 9000
    scapy.sendp(scapy.Ether(dst=MAC)/scapy.IP(dst=target)/scapy.UDP(dport=9000,sport=10000)/cyphertext)
    #read packets on port 9000
    while True:
        data, addr = s.recvfrom(1024)
        print(data.decode())
        break
    
if __name__ == "__main__":
    args = process_args()
    main(args[0], args[1], args[2], args[3])
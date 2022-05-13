#Port Knocking Script
#libpcap
from audioop import add
import sunau
import libpcap
libpcap.config(LIBPCAP=None)
import subprocess
import os
import sys
import threading
import socket
import time
connections={}

def openfirewall(addr):
    #open the firewall to addr for 10 seconds
    subprocess.call(["sudo", "iptables", "-A", "INPUT", "-p", "udp", "-s", addr, "--dport", "1000", "-j", "ACCEPT"])

def closefirewall(addr):
    time.sleep(10)
    subprocess.call(["sudo", "iptables", "-D", "INPUT", "-p", "udp", "-s", addr, "--dport", "1000", "-j", "ACCEPT"])

def listener(port, iter):
    global connections
    #create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #bind to the port
    s.bind(('', port))
    while True:
        #receive data
        data, addr = s.recvfrom(1024)
        if addr not in connections:
            connections[addr] = [0,0,0,0]
            connections[addr][iter] = 1
        #print out the data
        else:
            connections[addr][iter] = 1
            print("connection from", addr , "on port", port)
            print(connections[addr])
        #check if the address has knocked on all ports
        if sum(connections[addr]) == 4:
            #open the firewall
            openfirewall(addr[0])
            #remove the address from the list
            del connections[addr]

def main():
    ports = [1000,2000,3000,4000]
    iter = 0
    for port in ports:
        #create a thread for each port
        t = threading.Thread(target=listener, args=(port,iter,))
        iter+=1
        t.start()
    
def print_packet(pkt):
    print(pkt)

if __name__ == "__main__":
    #run dir
    subprocess.run("dir", shell=True)
    main()
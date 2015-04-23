import argparse
import socket
import struct
from uuid import getnode as get_mac
from random import randint

MAX_BYTES = 65535
server_port = 10067
client_port = 10068
class DHCPDiscover:
    def __init__(self):
        self.transactionID = b''
        for i in range(4):
            t = randint(0, 255)
            self.transactionID += struct.pack('!B', t)

    def buildPacket(self):
        #macb = getMacInBytes()
        packet = b''
        packet += b'\x01'   #Message type: Boot Request (1)
        packet += b'\x01'   #Hardware type: Ethernet
        packet += b'\x06'   #Hardware address length: 6
        packet += b'\x00'   #Hops: 0
        packet += self.transactionID       #Transaction ID
        packet += b'\x00\x00'    #Seconds elapsed: 0
        packet += b'\x80\x00'   #Bootp flags: 0x8000 (Broadcast) + reserved flags
        packet += b'\x00\x00\x00\x00'   #Client IP address: 0.0.0.0
        packet += b'\x00\x00\x00\x00'   #Your (client) IP address: 0.0.0.0
        packet += b'\x00\x00\x00\x00'   #Next server IP address: 0.0.0.0
        packet += b'\x00\x00\x00\x00'   #Relay agent IP address: 0.0.0.0
        packet += b'\x00\x26\x9e\x04\x1e\x9b'   #Client MAC address: 00:26:9e:04:1e:9b
        #packet += macb
        packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'   #Client hardware address padding: 00000000000000000000
        packet += b'\x00' * 67  #Server host name not given
        packet += b'\x00' * 125 #Boot file name not given
        packet += b'\x63\x82\x53\x63'   #Magic cookie: DHCP
        packet += b'\x35\x01\x01'   #Option: (t=53,l=1) DHCP Message Type = DHCP Discover
        #packet += b'\x3d\x06\x00\x26\x9e\x04\x1e\x9b'   #Option: (t=61,l=6) Client identifier
        packet += b'\x3d\x06\x00\x26\x9e\x04\x1e\x9b'
        packet += b'\x37\x03\x03\x01\x06'   #Option: (t=55,l=3) Parameter Request List
        packet += b'\xff'   #End Option
        return packet

class DHCPOffer:
    def __init__(self, data, transID):
        self.data = data
        self.transID = transID
        self.offerIP = ''
        self.nextServerIP = ''
        self.DHCPServerIdentifier = ''
        self.leaseTime = ''
        self.router = ''
        self.subnetMask = ''
        self.DNS = []
        self.unpack()

    def unpack(self):
        if self.data[4:8] == self.transID :
            self.offerIP = '.'.join(map(lambda x:str(x), data[16:20]))
            self.nextServerIP = '.'.join(map(lambda x:str(x), data[20:24]))  #c'est une option
            self.DHCPServerIdentifier = '.'.join(map(lambda x:str(x), data[245:249]))
            self.leaseTime = str(struct.unpack('!L', data[251:255])[0])
            self.router = '.'.join(map(lambda x:str(x), data[257:261]))
            self.subnetMask = '.'.join(map(lambda x:str(x), data[263:267]))
            dnsNB = int(data[268]/4)
            for i in range(0, 4 * dnsNB, 4):
                self.DNS.append('.'.join(map(lambda x:str(x), data[269 + i :269 + i + 4])))

    def printOffer(self):
        key = ['DHCP Server', 'Offered IP address', 'subnet mask', 'lease time (s)' , 'default gateway']
        val = [self.DHCPServerIdentifier, self.offerIP, self.subnetMask, self.leaseTime, self.router]
        for i in range(4):
            print('{0:20s} : {1:15s}'.format(key[i], val[i]))

        print('{0:20s}'.format('DNS Servers') + ' : ')
        if self.DNS:
            print('{0:15s}'.format(self.DNS[0]))
        if len(self.DNS) > 1:
            for i in range(1, len(self.DNS)):
                print('{0:22s} {1:15s}'.format(' ', self.DNS[i]))


def server(port):
    dhcps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dhcps.bind(('127.0.0.1', port))
    while True:
        print('Listening at {}'.format(dhcps.getsockname()))
        while True:
            data, address = dhcps.recvfrom(1024)
            text = data.decode('ascii')
            print('The client at {} says: {!r}'.format(address, text))
            break
        dhcps.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #broadcast
        text = '140.123.104.108'
        dhcps.sendto(text.encode('ascii'), address)
        while True:
            data, address = dhcps.recvfrom(1024)
            text = data.decode('ascii')
            print('The client at {} says: {!r}'.format(address, text))
            dhcps.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #broadcast
            text = 'ACKNOWLEDGEMENT'
            dhcps.sendto(text.encode('ascii'), address)
            break

def client(port):
    dhcps2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dhcps2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #broadcast
    try:
        dhcps2.bind(('', port))    #we want to send from port 68
    except Exception as e:
        print('port %d in use...' % port)
        dhcps2.close
        input('press any key to quit...')
        exit()

    #buiding and sending the DHCPDiscover packet
    text = 'client DISCOVERY'
    dhcps2.sendto(text.encode('ascii'), ('127.0.0.1', server_port))
    print('DHCP Discover sent waiting for reply...')
    print('Sending at {}'.format(dhcps2.getsockname()))
    try:
        while True:
            data, address = dhcps2.recvfrom(1024)
            text = data.decode('ascii')
            print('The server at {} says: {!r}'.format(address, text))
            break
    except socket.timeout as e:
        print(e)
    text = 'client REQUEST'
    dhcps2.sendto(text.encode('ascii'), ('127.0.0.1', server_port))
    try:
        while True:
            data, address = dhcps2.recvfrom(1024)
            text = data.decode('ascii')
            print('The server at {} says: {!r}'.format(address, text))
            break

	    
    except socket.timeout as e:
        print(e)

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')
    parser.add_argument('role', choices=choices, help='which role to play')
    args = parser.parse_args()
    function = choices[args.role]
    if args.role == 'server':
    	function(server_port)
    else:
    	function(client_port)


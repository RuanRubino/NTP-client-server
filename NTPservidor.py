import socket
import struct
import time
leapVersionMod,stratum,poll,precision,rootDelay,rootDispersio,referenceID,referenceTimestamp, originateTimestamp,transmitTimestam,receiveTimestamp = 0
NTP_EPOCH_OFFSET = 2208988800 
udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address =  ('192.168.100.187', 123)

udp_server_socket.bind(server_address)

def check_rcv():

def unpack_msg():

def define_timestamp():
    
def pack_msg():
    
def send_time():

def main():

if __name__ == "__main__":
    main()
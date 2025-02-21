import socket
import struct
import time
udp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

timeClientsend=0
timeClientsend_frac=0

timeClientRecive=0
timeClientRecive_frac=0

timeServerRecive=0
timeServerRecive_frac=0

timeServerTransmit=0
timeServerTransmit_frac=0

def ntp_timestamp():
    # Diferença entre a época Unix (1970) e a época NTP (1900) em segundos
    NTP_EPOCH_OFFSET = 2208988800
    # Obtém o tempo atual em segundos desde a época Unix
    unix_time = time.time()
    # Converte para segundos desde a época NTP
    ntp_seconds = int(unix_time + NTP_EPOCH_OFFSET)
    # Calcula a fração de segundos (parte fracionária)
    fraction = int((unix_time - int(unix_time)) * (2**32))
    # Empacota o timestamp NTP em 8 bytes (64 bits)
    timestamp = struct.pack('!II', ntp_seconds, fraction)
    return timestamp

def pack_msg():
    global timeClientsend
    leapVersionMode = b'\x23'               #leep+verion+mode   =   1 byte
    stratum = b'\x00'                       #stratum            =   1 byte
    poll = b'\x06'                          #poll               =   1 byte
    precision = b'\xFA'                     #precision          =   1 byte
    rootDelay = b'\x00\x00\x00\x00'         #rootDelay          =   4 bytes
    rootDispersion = 4* b'\x00'             #rootDispersion     =   4 bytes
    referenceID = 4 * b'\x00'               #referenceID        =   4 bytes
    referenceTimestamp = 8* b'\x00'         #referenceTimestamp =   8 bytes     
    originateTimestamp = ntp_timestamp()    #originateTimestamp =   8 bytes  
    receiveTimestamp = 8* b'\x00'           #receiveTimestamp   =   8 bytes
    transmitTimestamp  =  originateTimestamp #transmitTimestamp  =   8 bytes
    timeClientsend = struct.unpack("!Q", originateTimestamp)[0]
    msg = leapVersionMode + stratum + poll + precision + rootDelay + rootDispersion +referenceID +referenceTimestamp + originateTimestamp +receiveTimestamp + transmitTimestamp
    return msg


def unpack_msg(data):
    global timeServerRecive
    global timeServerTransmit

    timeServerRecive = struct.unpack("!6Q", data)[4]
    timeServerTransmit = struct.unpack("!6Q", data)[5]    # Pega o timestamp de segundos

    ntp_timestamp = struct.unpack("!12I", data)[10]       # Pega o timestamp de segundos
    ntp_timestamp_frac = struct.unpack("!12I", data)[11]  # Pega a fração de segundo
    epoch_time = ntp_timestamp - 2208988800               # Ajusta para a época UNIX (1970)
    
    print(f"Timestamp NTP: {ntp_timestamp} segundos e {ntp_timestamp_frac} fração")
    print(f"Tempo Unix: {epoch_time} segundos")
    print(f"Tempo UTC: {time.ctime(epoch_time)}")
    udp_client_socket.close()

def send_msg(dest_ip):
    global timeClientRecive
    dest_port = 123 # Porta de destino
    server_address = (dest_ip, dest_port)
    msg = pack_msg()
    udp_client_socket.sendto(msg, server_address)
    data, _ = udp_client_socket.recvfrom(1024)
    timeClientRecivePACK = ntp_timestamp()
    timeClientRecive = struct.unpack("!Q", timeClientRecivePACK)[0]
    unpack_msg(data)

def offset():
    global timeClientRecive
    global timeClientsend
    global timeServerRecive
    global timeServerTransmit
    offsetCalc =((timeServerRecive/ - timeClientsend) + (timeServerTransmit - timeClientRecive))
    return (offsetCalc-2208988800)/2000000000

def delay():
    
    global timeClientRecive
    global timeClientsend
    global timeServerRecive
    global timeServerTransmit
    delayCalc = ((timeClientRecive - timeClientsend) - (timeServerTransmit - timeServerRecive))
    return (delayCalc-2208988800)/1000000000

def main():
    print("Digite o IP do servidor NTP: ");
    ntpip = input()
    send_msg(ntpip)
    print(f"Offset:{offset()}")
    print(f"Delay:{delay()}")
    print("timeClientRecive: ",timeClientRecive)
    print("timeClientsend: ",timeClientsend)
    print("timeserverrevice: ",timeServerRecive)
    print("timeservertrabs: ",timeServerTransmit)
    
if __name__ == "__main__":
	main()
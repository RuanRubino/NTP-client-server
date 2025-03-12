import socket
import struct
import time
import hmac
import hashlib

# Diferença entre a época Unix (1970) e a época NTP (1900) em segundos
NTP_EPOCH_OFFSET = 2208988800

# Parâmetros para autenticação 
AUTH_KEY = b'poggers' # Chave pré-compartilhada
KEY_ID = 1            # Identificador da chave

# Criar socket UDP para comunicação 
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
    global NTP_EPOCH_OFFSET

    # Obtém o tempo atual e converte para o formato NTP (64 bits: 32 bits para segundos + 32 bits para fração).
    unix_time = time.time()
    ntp_seconds = int(unix_time + NTP_EPOCH_OFFSET)
    fraction = int((unix_time - int(unix_time)) * (2**32))

    # Empacota o timestamp NTP em 8 bytes (64 bits)
    timestamp = struct.pack('!II', ntp_seconds, fraction)
    return timestamp

def add_auth(msg):
    # Calcula o HMAC-SHA256 do pacote e anexa: 4 bytes do KEY_ID e 32 do digest
    key_id_bytes = struct.pack("!I", KEY_ID)
    digest = hmac.new(AUTH_KEY, msg, hashlib.sha256,).digest()
    return msg + key_id_bytes + digest

def verify_auth(data):
    # Verfica se os bytes do KEY_ID e do digest estão corretos.

    if len(data) < 48 + 4 + 32:
        print('Mensagem sem autenticação completa...')
        return False
    msg = data[:48]
    key_id_recv = struct.unpack("!I", data[48:52])[0]
    digest_recv = data[52:84]
    
    if key_id_recv != KEY_ID:
        print("KEY ID inválido...")
        return False

    expected_digest = hmac.new(AUTH_KEY, msg, hashlib.sha256).digest()
    if expected_digest != digest_recv:
        print('Digest inválido...')
        return False
    
    return True

def pack_msg():
    global timeClientsend
    global timeClientsend_frac

    leapVersionMode     = b'\x23'                 #leep+verion+mode   =   1 byte
    stratum             = b'\x00'                 #stratum            =   1 byte
    poll                = b'\x06'                 #poll               =   1 byte
    precision           = b'\xFA'                 #precision          =   1 byte
    rootDelay           = b'\x00\x00\x00\x00'     #rootDelay          =   4 bytes
    rootDispersion      = 4* b'\x00'              #rootDispersion     =   4 bytes
    referenceID         = 4 * b'\x00'             #referenceID        =   4 bytes
    referenceTimestamp  = 8* b'\x00'           #referenceTimestamp =   8 bytes     
    originateTimestamp  = ntp_timestamp()      #originateTimestamp =   8 bytes  
    receiveTimestamp    = 8* b'\x00'             #receiveTimestamp   =   8 bytes
    transmitTimestamp   =  originateTimestamp  #transmitTimestamp  =   8 bytes

    # Armazena o timestamp do envio (T1) para cálculo de delay e offset  
    timeClientsend, timeClientsend_frac = struct.unpack("!II", originateTimestamp)
    timeClientsend = timeClientsend + (timeClientsend_frac/2**32)

    msg = (leapVersionMode + stratum + poll + precision +
           rootDelay + rootDispersion + referenceID +
           referenceTimestamp + originateTimestamp +
           receiveTimestamp + transmitTimestamp)
    #msg = add_auth(msg)

    return msg


def unpack_msg(data):

    global NTP_EPOCH_OFFSET, timeServerRecive, timeServerTransmit
    #if not verify_auth(data):
     #   print("Falha na autenticação da resposta...")
      #  return
    
    header = data[:48]
    unpacked = struct.unpack("!12I", header)
    sec_rec = unpacked[8]
    frac_rec = unpacked[9]
    sec_trans = unpacked[10]
    frac_trans = unpacked[11]
    timeServerRecive = sec_rec + (frac_rec / 2**32)
    timeServerTransmit = sec_trans + (frac_trans / 2**32)

    epoch_time = sec_trans - NTP_EPOCH_OFFSET # Desfaz a conversão de NTP
    print(f"Servidor: Timestamp NTP: {sec_trans} segundos e {frac_trans} fração")
    print(f"Servidor: Tempo Unix: {epoch_time} segundos")
    print(f"Servidor: Tempo UTC: {time.ctime(epoch_time)}")

    udp_client_socket.close()

def send_msg(dest_ip):
    global timeClientRecive, timeClientRecive_frac
    # Envia o pacote NTP para o servidor e aguarda resposta
    # Registra o timestamp de recepção (T4) e chama unpack_msg() para processar a chamada
    dest_port = 5000 # Porta de destino
    server_address = (dest_ip, dest_port)

    try:
        msg = pack_msg()
        udp_client_socket.sendto(msg, server_address)
        data, _ = udp_client_socket.recvfrom(1024)

        # (T4) Tempo de recebimento da mensagem
        timeClientRecivePACK = ntp_timestamp()
        timeClientRecive, timeClientRecive_frac = struct.unpack("!II", timeClientRecivePACK)
        timeClientRecive = timeClientRecive + (timeClientRecive_frac/2**32) 
        unpack_msg(data)

    except socket.error as e:
        print(f"Erro ao enviar/receber mensagem: {e}")
    finally:
        udp_client_socket.close()

def print_time():
    print("timeClientRecive: ",timeClientRecive)
    print("timeClientsend  : ",timeClientsend)
    print("timeServerRecivce: ",timeServerRecive)
    print("timeServerTransmit : ",timeServerTransmit)

def offset():

    # Calcula o offset usando : offset = ((T2 - T1) + (T3 - T4)) / 2 para estimar a diferença entre cliente e servidor
    offsetCalc = ((timeServerRecive - timeClientsend) + (timeServerTransmit - timeClientRecive)) / 2
    return offsetCalc

def delay():

    # Calcula o delay usando : delay = (T4 - T1) + (T3 - T2) para estimar a diferença entre cliente e servidor
    delayCalc = ((timeClientRecive - timeClientsend) - (timeServerTransmit - timeServerRecive))
    return delayCalc

def main():

    ntpip = input("Digite o IP do servidor NTP: ")
    
    send_msg(ntpip)
    print_time()

    print(f"Offset:{offset()}")
    print(f"Delay:{delay()}")
    
if __name__ == "__main__":
	main()
import socket
import struct
import time
import hmac 
import hashlib

NTP_EPOCH_OFFSET = 2208988800 

# Parâmetros de autenticação 
AUTH_KEY = b'12345'
KEY_ID = 1

# Cria servidor UDP e vincula à porta 123 

udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address =  ('0.0.0.0', 123)
udp_server_socket.bind(server_address)

def ntp_timestamp():

    unixTime = time.time()
    ntp_seconds = int(unixTime + NTP_EPOCH_OFFSET)
    fraction = int((unixTime - int(unixTime)) * (2**32))
    return struct.pack("!II", ntp_seconds, fraction)

def add_auth(msg):

    # Calcula o HMAC-SHA256 do pacote e anexa: 4 bytes do KEY_ID e 32 do digest
    key_id_bytes = struct.pack("!I", KEY_ID)
    digest = hmac.new(AUTH_KEY, msg, hashlib.sha256,).digest()
    return msg + digest

def verify_auth(data):

    # Verfica se os bytes do KEY_ID e do digest estão corretos.
    if len(data) < 48 + 32:
        print('Mensagem sem autenticação completa...')
        return False
    
    msg = data[:48]
    #key_id_recv = struct.unpack("!I", data[48:52])[0]
    digest_recv = data[48:80]
    
    '''if key_id_recv != KEY_ID:
        print("KEY ID inválido...")
        return False'''

    expected_digest = hmac.new(AUTH_KEY, msg, hashlib.sha256).digest()
    if expected_digest != digest_recv:
        print('Digest inválido...')
        return False
    
    return True

def process_request(data):
    
    # Processa requisição do cliente, verifica autenticação, extrai o originateTimestamp (T1) enviado pelo cliente
    if not verify_auth(data):
       print("Erro na autenticação da requisição...")
       return None
    
    header = data[:48]
    fields = struct.unpack("!12I", header)
    T1 = fields[8] + fields[9] / 2**32  # Originate Timestamp do cliente

    return header, T1

def pack_response(request_header, T2, T3):

    # Constrói resposta do servidor com os campos:
    #
    #   - leapVersionMode: 0x24 (LI=0, VN=4, Mode=4 – servidor)
    #   - stratum: 1 (servidor de referência)
    #   - poll, precision, rootDelay, rootDispersion, referenceID, referenceTimestamp: conforme padrão
    #   - originateTimestamp: copiado do pacote do cliente (T1)
    #   - receiveTimestamp (T2) e transmitTimestamp (T3): marcados com o tempo atual

    leapVersionMode = b'\x24'  # LI=0, VN=4, Mode=4 (servidor)
    stratum         = b'\x01'
    poll            = b'\x06'
    precision       = b'\xFA'
    rootDelay       = b'\x00\x00\x00\x00'
    rootDispersion  = 4 * b'\x00'
    referenceID     = b'\x00\x00\x00\x00'
    referenceTimestamp = ntp_timestamp()  # Tempo de referência do servidor
    # Repete o originateTimestamp enviado pelo cliente (campo que o cliente usa para identificar sua requisição)
    originateTimestamp = request_header[40:48]

    def pack_time(t):

        sec = int(t)
        frac = int((t - sec) * (2**32))
        return struct.pack("!II", sec, frac)
    
    receiveTimestamp = pack_time(T2)
    transmitTimestamp = pack_time(T3)
    
    msg = (leapVersionMode + stratum + poll + precision +
           rootDelay + rootDispersion + referenceID +
           referenceTimestamp + originateTimestamp +
           receiveTimestamp + transmitTimestamp)
    msg = add_auth(msg)

    return msg

def main():

    while True:
        try:
            print('Aguardando requisição...')
            data, addr = udp_server_socket.recvfrom(1024)
            print('Pacote recebido de: ', addr)
            result = process_request(data)

            if result is None:
                print('Requisição descartada...')
                continue 
            request_header, T1 = result

            # (T2) Tempo que server recebeu requisição 
            T2 = time.time() + NTP_EPOCH_OFFSET
            
            # (T3) Tempo que servidor enviou a resposta
            T3 = time.time() + NTP_EPOCH_OFFSET
            
            response = pack_response(request_header, T2, T3)
            udp_server_socket.sendto(response, addr)
            print('Reposta enviada para:', addr)

        except Exception as e:
            print('Erro no servidor...')

if __name__ == "__main__":
    main()
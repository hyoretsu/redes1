from constants import *
from utils import *
from scapy.layers.inet import IP, Packet, UDP
from scapy.sendrecv import sr1


source_port = 59155
sock = IP(dst=server_addr[0], proto="udp")


def build_udp_header(src_port: int, dst_port: int, payload: bytearray) -> str:
    header = bytearray()
    # Porta de origem
    header.extend(src_port.to_bytes(2))
    # Porta de destino
    header.extend(dst_port.to_bytes(2))
    # Comprimento do segmento
    header.extend((8 + len(payload)).to_bytes(2))
    # Checksum (valor provisório de 0x0000)
    header.extend(b"\x00\x00")

    return header


def build_pseudo_ip_header(udp_segment: bytearray) -> str:
    source_ip = get_local_ip()

    header = bytearray()
    # Preparação para adição de IP's dinâmica
    bytes = {
        "source": [int(each) for each in source_ip.split(".")],
        "server": [int(each) for each in server_addr[0].split(".")],
    }

    # IP de origem
    for i in [0, 2]:
        header.extend(int(bytes["source"][i] << 8 | bytes["source"][i + 1]).to_bytes(2))

    # IP de destino
    for i in [0, 2]:
        header.extend(int(bytes["server"][i] << 8 | bytes["server"][i + 1]).to_bytes(2))

    # Byte 0 + Número de protocolo de transporte
    header.extend((0 << 8 | 17).to_bytes(2))

    # Comprimento do segmento UDP
    header.extend(len(udp_segment).to_bytes(2))

    return header


def calculate_checksum(
    udp_header: bytearray, udp_payload: bytearray, pseudo_ip_header: bytearray
) -> bytes:
    sum = 0

    sum += sum_every_two_bytes(pseudo_ip_header)
    sum += sum_every_two_bytes(udp_header)
    sum += sum_every_two_bytes(
        udp_payload + b"\x00" if len(udp_payload) < 4 else udp_payload
    )

    # Complemento de dois funcional, retirado do StackOverflow/ChatGPT pois não uso isso desde o P1 e nunca precisei usar operador bitwise em mais de 5 anos, não fazia ideia como fazer sozinho
    while sum >> 16:
        sum = (sum & 0xFFFF) + (sum >> 16)

    return (~sum & 0xFFFF).to_bytes(2)


def send_message(message_kind: int) -> str:
    # Associando o tipo da requisição vindo da interface aos tipos definidos na especificação
    message_kind = message_kind_assoc(message_kind)

    payload = build_message(message_type, message_kind)
    udp_header = build_udp_header(source_port, server_addr[1], payload)
    udp_segment: bytearray = udp_header + payload

    pseudo_ip_header = build_pseudo_ip_header(udp_segment)
    checksum = calculate_checksum(udp_header, payload, pseudo_ip_header)

    request: Packet = (
        sock
        / UDP(
            sport=source_port,
            dport=server_addr[1],
            len=len(udp_segment),
            chksum=int.from_bytes(checksum),
        )
        / payload
    )

    # Envia e recebe a mensagem do servidor
    response = sr1(request, verbose=0)

    # A variável `response` é uma classe do tipo `Packet`, e sua última camada é a resposta do servidor, a `Raw`
    data = response.lastlayer()
    # É necessário converter a camada em uma sequência de bytes, usando o construtor `bytes()` (compatível apenas com Python 3) ou a função `raw()` do Scapy (compatível com Python 2 e 3)
    data = bytes(data)

    answer = parse_response(data)

    return answer

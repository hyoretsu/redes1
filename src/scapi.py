from constants import *
from utils import *
from scapy.compat import raw
from scapy.layers.inet import IP, UDP
from scapy.sendrecv import sr1

socket = IP(dst=ip) / UDP(dport=port)


def send_message(message_kind: int) -> str:
    # Associando o tipo da requisição vindo da interface aos tipos definidos na especificação
    message_kind -= 1

    # Mesagens do tipo requisição são sempre 0
    message_type = 0

    request = socket / build_message(message_type, message_kind)

    # Envia e recebe a mensagem do servidor
    response = sr1(request, verbose=0)

    # A variável `response` é uma classe do tipo `Packet`, e sua última camada é a resposta do servidor, a `Raw`
    data = response.lastlayer()
    # É necessário converter a camada em uma sequência de bytes, usando o construtor `bytes()` (compatível apenas com Python 3) ou a função `raw()` do Scapy (compatível com Python 2 e 3)
    data = raw(data)

    answer = parse_response(data)

    return answer

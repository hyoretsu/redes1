from constants import *
from utils import *
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_message(message_kind: int) -> str:
    # Associando o tipo da requisição vindo da interface aos tipos definidos na especificação
    message_kind = message_kind_assoc(message_kind)

    message = build_message(message_type, message_kind)

    # Envia a mensagem para o servidor
    sock.sendto(message, server_addr)

    # Lê a resposta que o servidor enviou
    data, addr = sock.recvfrom(1024)

    answer = parse_response(data)

    return answer

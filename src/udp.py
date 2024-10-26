import random
import socket

server = ("15.228.191.109", 50000)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_message(message_kind: int) -> str:
    # Associando o tipo da requisição vindo da interface aos tipos definidos na especificação
    message_kind -= 1

    # Mesagens do tipo requisição são sempre 0
    message_type = 0

    id = random.randint(1, 65535)

    message = bytearray()
    # Concatena o tipo da mensagem com o tipo de pedido (4 bits + 4 bits) e os transforma em um único byte
    message.extend((message_type << 4 | message_kind).to_bytes())
    message.extend(id.to_bytes(2))

    # Envia a mensagem para o servidor
    sock.sendto(message, server)

    # Lê a resposta que o servidor enviou
    data, addr = sock.recvfrom(1024)

    # Seleciona apenas os 4 últimos bits do primeiro byte da mensagem, referentes ao tipo da resposta
    type = data[0] & 0x0F
    if type == 3:
        raise Exception("Tipo de mensagem inválida. Tente novamente.")

    # Pula os 3 primeiro bytes da resposta, referentes ao cabeçalho
    answer = data[4:]
    # Tratativa de byte para int/str
    if type == 2:
        answer = int.from_bytes(answer)
    else:
        answer = answer.decode("utf-8")

    return answer

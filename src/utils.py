import random
import socket


def build_message(message_type: int, message_kind: int) -> bytearray:
    id = random.randint(1, 65535)
    message = bytearray()

    # Concatena o tipo da mensagem com o tipo de pedido (4 bits + 4 bits) e os transforma em um único byte
    message.extend((message_type << 4 | message_kind).to_bytes(1))

    message.extend(id.to_bytes(2))

    return message


def get_local_ip() -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 1))

    local_ip = sock.getsockname()[0]

    return local_ip


def message_kind_assoc(message_kind: int) -> int:
    return message_kind - 1


def parse_response(response: bytes) -> str:
    # Seleciona apenas os 4 últimos bits do primeiro byte da mensagem, referentes ao tipo da resposta
    type = response[0] & 0x0F
    if type == 3:
        raise Exception("Tipo de mensagem inválida. Tente novamente.")

    # Pula os 3 primeiro bytes da resposta, referentes ao cabeçalho
    answer = response[4:]

    # Tratativa de byte para int/str
    if type == 2:
        answer = int.from_bytes(answer)
    else:
        answer = answer.decode("utf-8")

    return answer


def sum_every_two_bytes(data: bytes) -> int:
    sum = 0

    # Soma de números binários
    for i in range(0, len(data), 2):
        sum += data[i] << 8 | data[i + 1]

    return sum

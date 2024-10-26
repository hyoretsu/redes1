import random


def build_message(message_type: int, message_kind: int) -> bytearray:
    id = random.randint(1, 65535)
    message = bytearray()

    # Concatena o tipo da mensagem com o tipo de pedido (4 bits + 4 bits) e os transforma em um único byte
    message.extend((message_type << 4 | message_kind).to_bytes())

    message.extend(id.to_bytes(2))

    return message


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

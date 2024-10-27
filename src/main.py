# Aran Leite de Gusmão
# Camila Louzada Moraes
import udp
import scapi


def show_menu():
    print("\nEscolha uma opção de requisição:")
    print("1. Data e hora atual")
    print("2. Mensagem motivacional para o fim do semestre")
    print("3. Quantidade de respostas emitidas pelo servidor")
    print("4. Sair")


def cliente(send_message):
    while True:
        show_menu()

        try:
            escolha = int(input("Digite o número da sua escolha: "))
        except ValueError:
            print("Entrada inválida. Por favor, insira um número entre 1 e 4.")
            continue
        if escolha in [1, 2, 3]:
            resposta = send_message(escolha)
            print("Resposta do servidor:", resposta)
        elif escolha == 4:
            print("Saindo...")

            # Fechando o socket para não depender do OS
            udp.sock.close()

            break
        else:
            print("Opção inválida. Por favor, escolha um número entre 1 e 4.")


if __name__ == "__main__":
    protocolo = int(
        input(
            "Escolha o protocolo para o envio da mensagem (1 para UDP e 2 para SCAPI): "
        )
    )

    # Executando o cliente usando a função send_message apropriada
    if protocolo == 1:
        cliente(udp.send_message)
    elif protocolo == 2:
        cliente(scapi.send_message)
    else:
        print("Protocolo inválido. Escolha entre '1' ou '2'.")
        exit(1)

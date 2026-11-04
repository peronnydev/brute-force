import sys
import unicodedata

MAPA_HOMOGLIFOS = {
    "a": "а",
    "e": "е",
    "o": "о",
    "p": "р",
    "c": "с",
    "x": "х",
    "i": "і",
    "l": "ӏ",
}


def gerar_variantes(texto):
    variantes = []
    for original, falso in MAPA_HOMOGLIFOS.items():
        if original in texto:
            variantes.append(texto.replace(original, falso))
    return variantes


def para_punycode(dominio):
    try:
        return dominio.encode("idna").decode("ascii")
    except Exception:
        return "(nao codificavel como IDNA)"


def detectar(texto):
    suspeito = False
    scripts = set()
    for caractere in texto:
        if caractere in ".-/:_":
            continue
        nome = unicodedata.name(caractere, "")
        if "CYRILLIC" in nome:
            scripts.add("CIRILICO")
            suspeito = True
        elif "GREEK" in nome:
            scripts.add("GREGO")
            suspeito = True
        elif "LATIN" in nome or caractere.isascii():
            scripts.add("LATINO")
    return suspeito, scripts


def modo_gerar(texto):
    print("Original:   ", texto, "->", para_punycode(texto))
    for variante in gerar_variantes(texto):
        print("Homoglifo:  ", variante, "->", para_punycode(variante))


def modo_detectar(texto):
    suspeito, scripts = detectar(texto)
    print("Texto:", texto)
    print("Scripts encontrados:", ", ".join(sorted(scripts)) or "nenhum")
    print("Punycode:", para_punycode(texto))
    if suspeito:
        print("ALERTA: mistura de alfabetos -> possivel homoglifo/link falso")
    else:
        print("OK: apenas caracteres latinos/ascii")


def main():
    if len(sys.argv) < 3:
        print("Uso:")
        print("  python homoglifos.py gerar <dominio>")
        print("  python homoglifos.py detectar <dominio>")
        print("Exemplos:")
        print("  python homoglifos.py gerar login-example.com")
        print("  python homoglifos.py detectar аpple-example.com")
        return

    modo = sys.argv[1]
    texto = sys.argv[2]

    if modo == "gerar":
        modo_gerar(texto)
    elif modo == "detectar":
        modo_detectar(texto)
    else:
        print("Modo invalido. Use 'gerar' ou 'detectar'.")


if __name__ == "__main__":
    main()

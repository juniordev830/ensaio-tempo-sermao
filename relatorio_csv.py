import csv


def celula(valor):
    """Mantém texto com aparência de fórmula como texto em planilhas."""
    if isinstance(valor, str) and valor.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + valor
    return valor


def linhas(relatorio):
    for item in relatorio['blocos']:
        yield (item['nome'], item['palavras'], item['segundos'],)


def escrever_csv(relatorio, destino):
    escritor = csv.writer(destino, delimiter=";", quoting=csv.QUOTE_ALL, lineterminator="\n")
    escritor.writerow(('nome', 'palavras', 'segundos'))
    for linha in linhas(relatorio):
        escritor.writerow([celula(valor) for valor in linha])

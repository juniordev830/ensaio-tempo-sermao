'Estime a duração de cada bloco e descubra quanto precisa ajustar para caber no horário.'

import argparse
import sys
from relatorio_csv import escrever_csv
import json
import re
from pathlib import Path
from unicodedata import normalize

PALAVRA = re.compile(r"[^\W_]+(?:[-‐‑’'][^\W_]+)*")


def texto(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Use texto não vazio.")
    if re.search(r"[\ud800-\udfff]", value):
        raise ValueError("O texto contém um caractere Unicode incompleto.")
    return value.strip()


def inteiro(value, minimo=0):
    if type(value) is not int or value < minimo:
        raise ValueError(f"Use um número inteiro a partir de {minimo}.")
    return value


def run(data):
    if not isinstance(data, dict):
        raise ValueError("A entrada deve ser um objeto JSON.")
    if not isinstance(data["blocos"], list) or any(not isinstance(item, dict) for item in data["blocos"]):
        raise ValueError("O campo blocos deve ser uma lista de objetos.")
    ritmo = inteiro(data["palavras_por_minuto"], 1)
    limite = inteiro(data["limite_minutos"], 1) * 60
    agenda = []
    for item in data["blocos"]:
        trecho = normalize("NFC", texto(item["texto"]))
        palavras = len(PALAVRA.findall(trecho))
        segundos_fala = (palavras * 60 + ritmo - 1) // ritmo
        segundos = segundos_fala + inteiro(item.get("pausa_segundos", 0))
        agenda.append({"nome": texto(item["nome"]), "palavras": palavras, "segundos": segundos})
    total = sum(item["segundos"] for item in agenda)
    return {"blocos": agenda, "duracao_total_segundos": total,
            "folga_segundos": max(0, limite - total), "excesso_segundos": max(0, total - limite)}


def objeto_sem_campos_repetidos(pares):
    objeto = {}
    for chave, valor in pares:
        if chave in objeto:
            raise ValueError(f"Campo JSON repetido: {chave!r}.")
        objeto[chave] = valor
    return objeto


def rejeitar_constante_json(constante):
    raise ValueError(f"Constante numérica inválida em JSON: {constante}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", type=Path, help="Arquivo JSON com os dados")
    parser.add_argument("--csv", action="store_true", help="Exportar os tempos de cada bloco do ensaio em CSV")
    args = parser.parse_args()

    try:
        with args.entrada.open(encoding="utf-8-sig") as source:
            data = json.load(
                source,
                object_pairs_hook=objeto_sem_campos_repetidos,
                parse_constant=rejeitar_constante_json,
            )
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    if args.csv:
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
        escrever_csv(result, sys.stdout)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()


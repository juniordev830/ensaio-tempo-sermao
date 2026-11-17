'Estime a duração de cada bloco e descubra quanto precisa ajustar para caber no horário.'


def texto(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Use texto não vazio.")
    return value.strip()


def inteiro(value, minimo=0):
    if type(value) is not int or value < minimo:
        raise ValueError(f"Use um número inteiro a partir de {minimo}.")
    return value


import re
from unicodedata import normalize


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
        palavras = len(re.findall(r"[^\W_]+(?:[-’'][^\W_]+)*", trecho))
        segundos_fala = (palavras * 60 + ritmo - 1) // ritmo
        segundos = segundos_fala + inteiro(item.get("pausa_segundos", 0))
        agenda.append({"nome": texto(item["nome"]), "palavras": palavras, "segundos": segundos})
    total = sum(item["segundos"] for item in agenda)
    return {"blocos": agenda, "duracao_total_segundos": total,
            "folga_segundos": max(0, limite - total), "excesso_segundos": max(0, total - limite)}


import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", type=Path, help="Arquivo JSON com os dados")
    args = parser.parse_args()

    try:
        with args.entrada.open(encoding="utf-8-sig") as source:
            data = json.load(source)
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()


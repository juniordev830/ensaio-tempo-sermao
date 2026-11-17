import json
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys
import unittest

from app import run

ROOT = Path(__file__).resolve().parent


class ProjetoTest(unittest.TestCase):
    def test_exemplo_documentado(self):
        data = json.loads((ROOT / "exemplo.json").read_text(encoding="utf-8"))
        result = run(data)
        self.assertEqual(result['duracao_total_segundos'], 34)

    def test_acento_decomposto_tem_a_mesma_contagem(self):
        blocos = [{"nome": "Abertura", "texto": "reflexa\u0303o bíblica"}]
        result = run({"blocos": blocos, "palavras_por_minuto": 60, "limite_minutos": 1})
        self.assertEqual(result["blocos"][0]["palavras"], 2)
        self.assertEqual(result["duracao_total_segundos"], 2)

    def test_arredondamento_inteiro_preserva_um_segundo(self):
        result = run({
            "blocos": [{"nome": "Abertura", "texto": "Introdução", "pausa_segundos": 2}],
            "palavras_por_minuto": 10 ** 400,
            "limite_minutos": 1,
        })
        self.assertEqual(result["duracao_total_segundos"], 3)

    def test_cli_aceita_json_utf8_com_bom(self):
        exemplo = (ROOT / "exemplo.json").read_text(encoding="utf-8")
        with TemporaryDirectory() as pasta:
            entrada = Path(pasta) / "entrada.json"
            entrada.write_text(exemplo, encoding="utf-8-sig")
            resultado = subprocess.run(
                [sys.executable, str(ROOT / "app.py"), str(entrada)],
                capture_output=True, text=True, encoding="utf-8", check=True,
            )
        self.assertEqual(json.loads(resultado.stdout), run(json.loads(exemplo)))

    def test_cli_com_exemplo(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "app.py"), str(ROOT / "exemplo.json")],
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        self.assertEqual(json.loads(result.stdout)['duracao_total_segundos'], 34)

    def test_rejeita_dados_incompletos(self):
        with self.assertRaises((KeyError, ValueError, TypeError)):
            run({})

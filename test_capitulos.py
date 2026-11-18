import json
import shutil
import subprocess
import unittest
from pathlib import Path

from app import run


ROOT = Path(__file__).parent


@unittest.skipUnless(shutil.which("perl"), "O exportador usa Perl")
class CapitulosTest(unittest.TestCase):
    def exportar(self, report):
        return subprocess.run(
            ["perl", ROOT / "capitulos.pl"],
            input=json.dumps(report).encode(), capture_output=True,
        )

    def test_relatorio_real(self):
        report = run(json.loads((ROOT / "exemplo.json").read_text(encoding="utf-8")))
        result = self.exportar(report)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("00:00:00.000 --> 00:00:15.000\nIntrodução", result.stdout.decode())
        self.assertIn("00:00:15.000 --> 00:00:34.000\nConclusão", result.stdout.decode())

    def test_bloco_vazio_e_caracteres_reservados(self):
        result = self.exportar({"blocos": [
            {"nome": "Sem duração", "segundos": 0},
            {"nome": "A\n& <B> --> C", "segundos": 3661},
        ]})
        self.assertEqual(result.stdout.decode(), "WEBVTT\n\n00:00:00.000 --> 01:01:01.000\nA &amp; &lt;B&gt; --&gt; C\n")

    def test_rejeita_duracao_negativa_sem_saida_parcial(self):
        result = self.exportar({"blocos": [{"nome": "A", "segundos": -1}]})
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, b"")

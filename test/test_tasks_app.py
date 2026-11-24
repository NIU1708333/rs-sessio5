import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


ARREL = Path(__file__).resolve().parent.parent
SCRIPT = ARREL / "src" / "tasks_app.py"
MODEL = ARREL / "src" / "models.py"


@pytest.fixture
def projecte_aillat(tmp_path):
    directori_src = tmp_path / "src"
    directori_src.mkdir()
    shutil.copy2(MODEL, directori_src / "models.py")
    shutil.copy2(SCRIPT, directori_src / "tasks_app.py")

    directori_dades = tmp_path / "data"
    directori_dades.mkdir()
    fitxer_tasques = directori_dades / "tasks.json"
    fitxer_tasques.write_text("[]", encoding="utf-8")
    return tmp_path, fitxer_tasques


def executar_cli(projecte, *arguments):
    directori, _ = projecte
    return subprocess.run(
        [sys.executable, "src/tasks_app.py", *arguments],
        cwd=directori,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )


def test_gs01_afegir_tasca(projecte_aillat):
    resultat = executar_cli(
        projecte_aillat,
        "add",
        "--title",
        "Pràctica 1",
        "--subject",
        "RS",
    )

    assert resultat.stdout.strip() == "Tasca [ID: 1] creada amb èxit"

    _, fitxer_tasques = projecte_aillat
    tasques = json.loads(fitxer_tasques.read_text(encoding="utf-8"))
    assert tasques == [
        {
            "id": 1,
            "títol": "Pràctica 1",
            "assignatura": "RS",
            "estat": "pendent",
        }
    ]


def test_gs02_llistat_buit(projecte_aillat):
    resultat = executar_cli(projecte_aillat, "list")

    assert resultat.stdout.splitlines() == ["Registre de tasques buit."]


def test_gs03_llistat_amb_tasques(projecte_aillat):
    _, fitxer_tasques = projecte_aillat
    fitxer_tasques.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "títol": "Pràctica 1",
                    "assignatura": "RS",
                    "estat": "pendent",
                },
                {
                    "id": 2,
                    "títol": "Examen parcial",
                    "assignatura": "SO",
                    "estat": "pendent",
                },
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    resultat = executar_cli(projecte_aillat, "list")

    assert resultat.stdout.splitlines() == [
        "[1] Pràctica 1 (RS) - estat: pendent",
        "[2] Examen parcial (SO) - estat: pendent",
    ]

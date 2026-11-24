import argparse
import json
from pathlib import Path

try:
    from models import Task
except ImportError:
    from src.models import Task


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "tasks.json"


def carregar_tasques():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")
        return []
    with DATA_FILE.open(encoding="utf-8") as fitxer:
        dades = json.load(fitxer)
    return [Task.from_dict(registre) for registre in dades]


def desar_tasques(tasques):
    with DATA_FILE.open("w", encoding="utf-8") as fitxer:
        json.dump(
            [tasca.to_dict() for tasca in tasques],
            fitxer,
            ensure_ascii=False,
            indent=2,
        )
        fitxer.write("\n")


def afegir_tasca(titol, assignatura):
    tasques = carregar_tasques()
    identificador = max((tasca.id for tasca in tasques), default=0) + 1
    tasca = Task(
        id=identificador,
        titol=titol,
        assignatura=assignatura,
        estat="pendent",
    )
    tasques.append(tasca)
    desar_tasques(tasques)
    print(f"Tasca [ID: {identificador}] creada amb èxit")


def llistar_tasques():
    tasques = carregar_tasques()
    if not tasques:
        print("Registre de tasques buit.")
        return
    for tasca in tasques:
        print(
            f"[{tasca.id}] {tasca.titol} "
            f"({tasca.assignatura}) - estat: {tasca.estat}"
        )


def construir_parser():
    parser = argparse.ArgumentParser(
        description="Gestiona les tasques acadèmiques."
    )
    subparsers = parser.add_subparsers(dest="comandament", required=True)

    parser_add = subparsers.add_parser("add", help="Crea una tasca nova.")
    parser_add.add_argument("--title", required=True, help="Títol de la tasca.")
    parser_add.add_argument(
        "--subject", required=True, help="Assignatura de la tasca."
    )

    subparsers.add_parser("list", help="Mostra totes les tasques.")
    return parser


def main():
    arguments = construir_parser().parse_args()
    if arguments.comandament == "add":
        afegir_tasca(arguments.title, arguments.subject)
    elif arguments.comandament == "list":
        llistar_tasques()


if __name__ == "__main__":
    main()

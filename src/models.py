import json
from dataclasses import dataclass


@dataclass
class Task:
    id: int
    titol: str
    assignatura: str
    estat: str = "pendent"

    def to_dict(self):
        return {
            "id": self.id,
            "títol": self.titol,
            "assignatura": self.assignatura,
            "estat": self.estat,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, dades):
        titol = dades["títol"] if "títol" in dades else dades["title"]
        assignatura = (
            dades["assignatura"]
            if "assignatura" in dades
            else dades["subject"]
        )
        return cls(
            id=int(dades["id"]),
            titol=titol,
            assignatura=assignatura,
            estat=dades.get("estat", dades.get("status", "pendent")),
        )

    @classmethod
    def from_json(cls, text):
        return cls.from_dict(json.loads(text))

import csv
from pathlib import Path


_mesures = []
_index_courant = 0


def charger_csv(csv_path: str | Path) -> int:
    """Charge les mesures depuis un CSV et reset l'index de lecture."""
    global _mesures, _index_courant

    chemin = Path(csv_path)
    with chemin.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        _mesures = []
        for row in reader:
            _mesures.append(
                {
                    "t_s": float(row["t_s"]),
                    "cap_cons_deg": float(row["cap_cons_deg"]),
                    "cap_compas_deg": float(row["cap_compas_deg"]),
                    "potentiometre_deg": float(row["potentiometre_deg"]),
                    "vent_deg": float(row["vent_deg"]),
                    "vent_ms": float(row["vent_ms"]),
                }
            )

    _index_courant = 0
    return len(_mesures)


def nb_mesures() -> int:
    return len(_mesures)


def set_index(index: int) -> None:
    """Positionne la mesure courante par index."""
    if not _mesures:
        raise RuntimeError("Aucune mesure chargee. Appeler charger_csv() d'abord.")
    if index < 0 or index >= len(_mesures):
        raise IndexError(f"Index mesure hors limite: {index}")

    global _index_courant
    _index_courant = index


def mesure_courante() -> dict:
    """Retourne la ligne CSV courante."""
    if not _mesures:
        raise RuntimeError("Aucune mesure chargee. Appeler charger_csv() d'abord.")
    return _mesures[_index_courant]

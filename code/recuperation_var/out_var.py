# recupere toutes les variables via un module par capteur

from pathlib import Path

from .recuperation_cap_consigne import cap_consigne
from .recuperation_compas import compas
from .recuperation_potentiometre import potentiometre
from .recuperation_vent import vent
from .source_donnees import charger_csv, mesure_courante, nb_mesures, set_index


def initialiser_source_csv(csv_path: str | Path) -> int:
	"""Charge les donnees d'entree capteurs depuis un CSV."""
	return charger_csv(csv_path)


def lire_entree_capteurs(index: int) -> dict:
	"""Retourne l'entree capteurs complete pour l'index demande."""
	set_index(index)
	vent_deg, vent_ms = vent()
	return {
		"t_s": mesure_courante()["t_s"],
		"cap_cons_deg": cap_consigne(),
		"cap_compas_deg": compas(),
		"potentiometre_deg": potentiometre(),
		"vent_deg": vent_deg,
		"vent_ms": vent_ms,
	}


def nombre_entrees() -> int:
	"""Retourne le nombre total d'entrees capteurs chargees."""
	return nb_mesures()

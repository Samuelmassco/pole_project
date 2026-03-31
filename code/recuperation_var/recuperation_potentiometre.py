from .source_donnees import mesure_courante


def potentiometre() -> float:
	"""Retourne la position potentiometre (degres) de la mesure courante."""
	return mesure_courante()["potentiometre_deg"]
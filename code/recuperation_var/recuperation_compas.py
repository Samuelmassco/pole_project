from .source_donnees import mesure_courante


def compas() -> float:
    """Retourne le cap compas (degres) de la mesure courante."""
    return mesure_courante()["cap_compas_deg"]
from .source_donnees import mesure_courante


def cap_consigne() -> float:
    """Retourne le cap de consigne (degres) de la mesure courante."""
    return mesure_courante()["cap_cons_deg"]

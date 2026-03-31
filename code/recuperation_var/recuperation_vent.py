from .source_donnees import mesure_courante


def vent() -> tuple[float, float]:
    """Retourne (direction_vent_deg, vitesse_vent_ms) de la mesure courante."""
    m = mesure_courante()
    return m["vent_deg"], m["vent_ms"]

## recense les differentes variables
import numpy as np
from recuperation_var.out_var import *

cap_cons = 5  # cap de consigne en degre

# Valeur actuelle + historique des mesures compas
cap_compas_actuel = None
cap_compas_l = np.array([], dtype=object)

# Valeur actuelle + historique des mesures potentiometre
potentiometre_actuel = None
potentiometre_l = np.array([], dtype=object)


def ajouter_mesure_compas():
	"""Lit la mesure compas, met a jour la valeur actuelle et l'historique."""
	global cap_compas_actuel, cap_compas_l
	cap_compas_actuel = compas()
	cap_compas_l = np.append(cap_compas_l, cap_compas_actuel)
	return cap_compas_actuel


def ajouter_mesure_potentiometre():
	"""Lit la mesure potentiometre, met a jour la valeur actuelle et l'historique."""
	global potentiometre_actuel, potentiometre_l
	potentiometre_actuel = potentiometre()
	potentiometre_l = np.append(potentiometre_l, potentiometre_actuel)
	return potentiometre_actuel


def maj_cap_et_potentiometre():
	"""Met a jour compas + potentiometre en une seule fonction."""
	return {
		"compas": ajouter_mesure_compas(),
		"potentiometre": ajouter_mesure_potentiometre(),
	}


def get_etat_compas():
	"""Retourne la valeur actuelle et les valeurs passees du compas."""
	return {
		"actuel": np.array([cap_compas_actuel], dtype=object),
		"passees": cap_compas_l.copy(),
	}


def get_etat_potentiometre():
	"""Retourne la valeur actuelle et les valeurs passees du potentiometre."""
	return {
		"actuel": np.array([potentiometre_actuel], dtype=object),
		"passees": potentiometre_l.copy(),
	}





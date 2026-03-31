import numpy as np


def normaliser_erreur_cap(erreur_deg):
    """Ramene une erreur de cap dans l'intervalle [-180, 180]."""
    return (erreur_deg + 180.0) % 360.0 - 180.0


def commande_barre_P(
    cap_cons,
    cap_compas_l,
    kp=1.0,
    ki=0.0,
    kd=0.0,
    dt=0.5,
    theta_barre_max=30.0,
):
    """Renvoie l'angle de barre via un PID simple sur l'erreur de cap.

    Args:
        cap_cons (float): cap de consigne (degres)
        cap_compas_l (array): historique des caps compas (degres)
        kp (float): gain proportionnel
        ki (float): gain integral
        kd (float): gain derive
        dt (float): periode de calcul (s)
        theta_barre_max (float): saturation de l'angle de barre (degres)

    Returns:
        float: angle de barre en degré
    """
    cap_hist = np.asarray(cap_compas_l, dtype=float)
    if cap_hist.size == 0:
        raise ValueError("cap_compas_l doit contenir au moins une mesure")
    if dt <= 0:
        raise ValueError("dt doit etre > 0")

    cap_comp = cap_hist[-1]
    erreur = normaliser_erreur_cap(cap_cons - cap_comp)

    erreurs_hist = normaliser_erreur_cap(cap_cons - cap_hist)

    p = kp * erreur
    i = ki * np.sum(erreurs_hist) * dt
    if cap_hist.size >= 2:
        d = kd * (erreurs_hist[-1] - erreurs_hist[-2]) / dt
    else:
        d = 0.0

    theta_barre = p + i + d
    theta_barre = float(np.clip(theta_barre, -theta_barre_max, theta_barre_max))
    return theta_barre





def commande_verrin(theta_barre,b,L,potentiometre_l):
    """renvoie la consigne verin à partir de la consigne d'angle de barre

    Args:
        theta_barre (float): angle  de barre en degré
            b (float): distance entre le point d'attache du vérin sur la barre et le centre de rotation de la barre
            L (float): distance entre le point d'attache du vérin sur le bateau et le centre de rotation de la barre

    Returns:
        float: consigne verin
    """
    x_verin_ancien=potentiometre_l[-1] #longueur du vérin à l'instant t-1
    theta_barre_rad=theta_barre*np.pi/180 #conversion en radian
    
    def f(x_verin):
        """renvoie l'angle de barre à partir de la position du verrin

        Args:
            x_verin (float): longueur du vérin en m

        Returns:
            float: angle de barre en radian
        """
        return np.arcsin((x_verin**2+b**2-L**2)/(2*x_verin*b))+np.arcsin((x_verin**2+L**2-b**2)/(2*x_verin*L))-theta_barre_rad
    
    # Import local pour eviter de rendre le module commande dependant de SciPy
    # si seule la commande de barre est utilisee.
    from scipy.optimize import fsolve

    x_verin = fsolve(f, x_verin_ancien)[0]
    return x_verin
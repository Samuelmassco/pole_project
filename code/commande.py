import numpy as np


def commande_barre_P(cap_cons, cap_compas_l):
    """renvoie l'angle de barre en fonction de la différence de cap

    Args:
        cap_cons (_type_): _description_
        cap_compas_l (array): _description_

    Returns:
        float: angle de barre en degré
    """
    
    Kp=1
    Ki=1
    Kd=1
    theta_barre_max=30   #en degré
    dcap=cap_cons-cap_compas_l[-1] #différence de cap
    theta_barre=Kp*(dcap) #correction proportionnel
    theta_barre=np.sign(theta_barre)*min(theta_barre_max,theta_barre) #on limite l'angle de barre à theta_barre_max
    
    return theta_barre




def commande_mot(theta_barre, pos_verin):
    return cons_mot
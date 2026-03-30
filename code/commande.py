import numpy as np



def commande_barre_P(cap_cons, cap_comp):
    """renvoie l'angle de barre en fonction de la différence de cap

    Args:
        cap_cons (_type_): _description_
        cap_comp (_type_): _description_

    Returns:
        float: angle de barre en degré
    """
    Kp=1
    Ki=1
    Kd=1
    theta_barre_max=30   #en degré
    
    theta_barre=K*(cap_cons-cap_comp) #correction proportionnel
    theta_barre=np.sign(theta_barre)*min(theta_barre_max,theta_barre)
    
    return theta_barre




def commande_mot(theta_barre, pos_verin):
    return cons_mot
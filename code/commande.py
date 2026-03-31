import numpy as np
from scipy.optimize import fsolve, brentq

def commande_barre_P(cap_cons, cap_compas_l):
    """renvoie l'angle de barre en fonction de la différence de cap grâce à un correcteur PID

    Args:
        cap_cons (_type_): _description_
        cap_compas_l (array): _description_

    Returns:
        float: angle de barre en degré
    """
    
    Kp=1
    Ki=1
    Kd=1
    cap_comp=cap_compas_l[-1] #cap actuel
    theta_barre_max=30   #en degré
    
    dcap=cap_cons-cap_comp #différence de cap
    
    
    P=Kp*(dcap) #correction proportionnelle
    I=Ki*np.sum(cap_cons-cap_compas_l) #correction intégrale
    D=Kd*(dcap-cap_cons+cap_compas_l[-2]) #correction dérivée
    theta_barre=P+I+D #angle de barre
    theta_barre=np.sign(theta_barre)*min(theta_barre_max,theta_barre) #on limite l'angle de barre à theta_barre_max
    
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
    
    x_verin = fsolve(f, x_verin_ancien)[0]
    return x_verin
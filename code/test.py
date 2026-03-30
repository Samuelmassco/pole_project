from gpiozero import PWMOutputDevice, DigitalOutputDevice
from time import sleep

# --- CONFIGURATION DES PINS ---
# GPIO 17 (Pin 11) : Le "Master Switch" (R_EN et L_EN)
enable = DigitalOutputDevice(17)

# GPIO 18 (Pin 12) : Sortie du vérin (RPWM)
pwm_sortir = PWMOutputDevice(18)

# GPIO 13 (Pin 33) : Rentrée du vérin (LPWM)
pwm_rentrer = PWMOutputDevice(13)

def test_systeme():
    try:
        print("Étape 1 : Activation du pont en H (Enable HIGH)...")
        enable.on() # On ouvre les barrières (R_EN et L_EN)
        sleep(0.5)

        print("Étape 2 : Sortie du vérin (30% puissance) pendant 1 seconde...")
        pwm_sortir.value = 0.3  # Vitesse lente pour sécurité
        pwm_rentrer.value = 0
        sleep(1)

        print("Étape 3 : Arrêt...")
        pwm_sortir.value = 0
        sleep(1)

        print("Étape 4 : Rentrée du vérin (30% puissance) pendant 1 seconde...")
        pwm_rentrer.value = 0.3
        pwm_sortir.value = 0
        sleep(1)

    except KeyboardInterrupt:
        print("\nTest interrompu par l'utilisateur.")
    
    finally:
        # SECURITÉ : On coupe tout avant de quitter
        pwm_sortir.value = 0
        pwm_rentrer.value = 0
        enable.off()
        print("Système désactivé. Fin du test.")

if __name__ == "__main__":
    test_systeme()
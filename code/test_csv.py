import argparse
import time
from pathlib import Path

import numpy as np

from commande import commande_barre_P, normaliser_erreur_cap
from recuperation_var.out_var import initialiser_source_csv, lire_entree_capteurs, nombre_entrees


def calcul_commande(entree_capteur: dict, cap_compas_hist: np.ndarray, dt_s: float) -> float:
    """Calcule la commande de barre a partir du cap consigne et du cap compas."""
    return commande_barre_P(
        cap_cons=entree_capteur["cap_cons_deg"],
        cap_compas_l=cap_compas_hist,
        kp=1.2,
        ki=0.02,
        kd=0.15,
        dt=dt_s,
        theta_barre_max=30.0,
    )


def simuler_depuis_csv(csv_path: Path, dt_capteurs_s: float, dt_barre_s: float) -> None:
    """Simule une lecture capteurs periodique et une mise a jour barre decalee."""
    nb = initialiser_source_csv(csv_path)
    print(f"{nb} mesures chargees depuis {csv_path.name}\n")

    t0 = time.monotonic()
    prochaine_lecture = t0
    prochaine_commande_barre = t0
    derniere_commande_barre = 0.0
    cap_compas_hist = np.array([], dtype=float)
    potentiometre_hist = np.array([], dtype=float)

    for i in range(nombre_entrees()):
        while True:
            maintenant = time.monotonic()
            attente = prochaine_lecture - maintenant
            if attente <= 0:
                break
            time.sleep(min(attente, 0.01))

        entree = lire_entree_capteurs(i)
        cap_compas_hist = np.append(cap_compas_hist, entree["cap_compas_deg"])
        potentiometre_hist = np.append(potentiometre_hist, entree["potentiometre_deg"])

        # Algo execute a chaque lecture capteur (cadence 0.5 s par defaut)
        commande = calcul_commande(entree, cap_compas_hist=cap_compas_hist, dt_s=dt_capteurs_s)
        erreur_cap = normaliser_erreur_cap(entree["cap_cons_deg"] - entree["cap_compas_deg"])
        barre_maj = False

        # Barre ajustee a sa propre cadence (0.7 s par defaut)
        maintenant = time.monotonic()
        if maintenant >= prochaine_commande_barre:
            derniere_commande_barre = commande
            barre_maj = True
            while prochaine_commande_barre <= maintenant:
                prochaine_commande_barre += dt_barre_s

        print(
            f"n={i:02d} | t_csv={entree['t_s']:>4.1f}s | cap_cons={entree['cap_cons_deg']:>6.1f} | "
            f"cap_comp={entree['cap_compas_deg']:>6.1f} | pot={entree['potentiometre_deg']:>5.1f} | "
            f"vent={entree['vent_deg']:>6.1f}deg {entree['vent_ms']:>4.1f}m/s | "
            f"err={erreur_cap:>+6.1f} | algo={commande:>5.1f} | barre={derniere_commande_barre:>5.1f} "
            f"({'MAJ' if barre_maj else 'HOLD'})"
        )

        prochaine_lecture += dt_capteurs_s


def main() -> None:
    parser = argparse.ArgumentParser(description="Test du pilote avec entrees capteurs depuis un CSV")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).with_name("donnees_capteurs_test.csv"),
        help="Chemin vers le CSV de donnees capteurs",
    )
    parser.add_argument(
        "--dt-capteurs",
        type=float,
        default=0.5,
        help="Periode de lecture capteurs et execution algo (s).",
    )
    parser.add_argument(
        "--dt-barre",
        type=float,
        default=0.7,
        help="Periode d'ajustement de la barre (s).",
    )
    args = parser.parse_args()

    if not args.csv.exists():
        raise FileNotFoundError(f"CSV introuvable: {args.csv}")

    if args.dt_capteurs <= 0:
        raise ValueError("--dt-capteurs doit etre > 0")
    if args.dt_barre <= 0:
        raise ValueError("--dt-barre doit etre > 0")

    simuler_depuis_csv(args.csv, dt_capteurs_s=args.dt_capteurs, dt_barre_s=args.dt_barre)


if __name__ == "__main__":
    main()

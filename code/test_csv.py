import argparse
import time
from pathlib import Path

from recuperation_var.out_var import initialiser_source_csv, lire_entree_capteurs, nombre_entrees

def calcul_commande_placeholder(entree_capteur: dict) -> float:
    """Placeholder: le calcul de commande sera ajoute plus tard."""
    _ = entree_capteur
    return 0.0


def simuler_depuis_csv(csv_path: Path, dt_capteurs_s: float, dt_barre_s: float) -> None:
    """Simule une lecture capteurs periodique et une mise a jour barre decalee."""
    nb = initialiser_source_csv(csv_path)
    print(f"{nb} mesures chargees depuis {csv_path.name}\n")

    t0 = time.monotonic()
    prochaine_lecture = t0
    prochaine_commande_barre = t0
    derniere_commande_barre = 0.0

    for i in range(nombre_entrees()):
        while True:
            maintenant = time.monotonic()
            attente = prochaine_lecture - maintenant
            if attente <= 0:
                break
            time.sleep(min(attente, 0.01))

        entree = lire_entree_capteurs(i)

        # Algo execute a chaque lecture capteur (cadence 0.5 s par defaut)
        commande = calcul_commande_placeholder(entree)
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
            f"algo={commande:>5.1f} | barre={derniere_commande_barre:>5.1f} "
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

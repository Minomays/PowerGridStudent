from StrategieReseau import StrategieReseauManuelle, StrategieReseauAuto
from Terrain import Terrain
from Reseau import Reseau
import os

if __name__ == "__main__":
    # Création du réseau
    reseau = Reseau()

    # Chargement du terrain
    terrain = Terrain()
    terrain.charger("terrains/t1.txt")

    os.system("clear")

    while True:
        # Menu principal
        print("Choissisez l'action à effectuer :")
        print("1 - Créer un réseau manuellement")
        print("2 - Créer un réseau automatiquement")
        print("3 - Afficher le terrain")
        print("4 - Charger un terrain")
        print("Q - Quitter")

        while True:
            choix = input("Votre choix : ")

            if choix == "1": # Créer un réseau manuellement
                os.system("clear")
                reseau.set_strategie(StrategieReseauManuelle())
                reseau.configurer(terrain)

                # Retour au menu principal
                os.system("clear")
                break
            elif choix == "2": # Créer un réseau automatiquement
                os.system("clear")
                reseau.set_strategie(StrategieReseauAuto())
                reseau.configurer(terrain)

                # Afficher le réseau
                print(f"Le réseau a un coût total de {reseau.calculer_cout()}M€.")
                reseau.afficher(terrain)

                # Retour au menu principal
                os.system("clear")
                break
            elif choix == "3": # Afficher le terrain
                os.system("clear")
                
                # Afficher le terrain et le réseau
                reseau.afficher(terrain)

                # Bloquer le programme jusqu'à ce que l'utilisateur appuie sur une touche
                input("Appuyez sur la touche Entrée pour continuer...")

                # Retour au menu principal
                os.system("clear")
                break
            elif choix == "4": # Charger un terrain
                os.system("clear")

                # Montrer les terrains disponibles
                print("Liste des terrains disponibles :")
                terrains = os.listdir("terrains")
                for i, t in enumerate(terrains):
                    print(f"{i+1} - {t}")
                print("r - Retour au menu principal")
                    
                # Récupérer le choix de l'utilisateur et charger le terrain
                while True:
                    choix = input("Votre choix : ")
                    if choix.isdigit():
                        terrain.charger(f"terrains/{terrains[int(choix)-1]}")
                        break
                    elif choix == "r": break
                    else: print("Choix invalide.")
                
                # Retour au menu principal
                os.system("clear")
                break
            elif choix == "Q" or choix == "q": exit() # Quitter le programme
            else: print("Choix invalide.") # Choix invalide
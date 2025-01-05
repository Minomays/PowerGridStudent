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

    # Temporaire
    #reseau.ajouter_noeud(0, (9, 17))
    #reseau.ajouter_noeud(1, (8, 17))
    #reseau.ajouter_noeud(2, (7, 17))
    #reseau.ajouter_noeud(3, (6, 17))
    #reseau.ajouter_noeud(4, (5, 17))
    #reseau.ajouter_noeud(5, (4, 17))
    #reseau.ajouter_noeud(6, (7, 16))
    #reseau.ajouter_noeud(7, (7, 15))
    #reseau.ajouter_noeud(8, (7, 14))
    #reseau.ajouter_noeud(9, (7, 13))
    #reseau.ajouter_noeud(10, (7, 12))
    #reseau.ajouter_noeud(11, (7, 11))
    #reseau.ajouter_noeud(12, (7, 10))
    #reseau.ajouter_noeud(13, (7, 9))
    #reseau.ajouter_noeud(14, (7, 8))
    #reseau.ajouter_noeud(15, (7, 7))
    #reseau.ajouter_noeud(16, (7, 6))
    #reseau.ajouter_noeud(17, (6, 9))
    #reseau.ajouter_noeud(18, (5, 9))
    #reseau.ajouter_noeud(19, (4, 9))
    #reseau.ajouter_noeud(20, (3, 9))
    #reseau.ajouter_noeud(21, (2, 9))
    #reseau.ajouter_noeud(22, (2, 10))
    #reseau.ajouter_arc(0, 1)
    #reseau.ajouter_arc(1, 2)
    #reseau.ajouter_arc(2, 3)
    #reseau.ajouter_arc(3, 4)
    #reseau.ajouter_arc(4, 5)
    #reseau.ajouter_arc(2, 6)
    #reseau.ajouter_arc(6, 7)
    #reseau.ajouter_arc(7, 8)
    #reseau.ajouter_arc(8, 9)
    #reseau.ajouter_arc(9, 10)
    #reseau.ajouter_arc(10, 11)
    #reseau.ajouter_arc(11, 12)
    #reseau.ajouter_arc(12, 13)
    #reseau.ajouter_arc(13, 14)
    #reseau.ajouter_arc(14, 15)
    #reseau.ajouter_arc(15, 16)
    #reseau.ajouter_arc(13, 17)
    #reseau.ajouter_arc(17, 18)
    #reseau.ajouter_arc(18, 19)
    #reseau.ajouter_arc(19, 20)
    #reseau.ajouter_arc(20, 21)
    #reseau.ajouter_arc(21, 22)

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
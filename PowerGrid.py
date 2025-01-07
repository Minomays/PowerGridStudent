from StrategieReseau import StrategieReseauManuelle, StrategieReseauAuto
from Terrain import Terrain
from Reseau import Reseau
import os

if __name__ == "__main__":
    # Création du réseau
    reseau = Reseau()

    # Chargement du terrain
    terrain = Terrain()
    terrain.charger("terrains/t1.txt", reseau)

    os.system("clear")

    while True:
        # Menu principal
        print("Bienvenue dans PowerGrid !")
        print("Choissisez l'action à effectuer :")
        print("1 - Créer un réseau manuellement")
        print("2 - Créer un réseau automatiquement")
        print(f"3 - Afficher le terrain ({terrain.fichier})")
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

                print("Création du réseau automatique...")

                # Passer en mode automatique
                reseau.set_strategie(StrategieReseauAuto())

                # Configurer le réseau
                try: reseau.configurer(terrain)
                except: print("Un problème est survenu lors de la création du réseau.")
                finally:
                    # Changer le texte
                    os.system("clear")
                    print("Création du réseau automatique terminée.")

                    # Afficher le coût du réseau
                    print(f"Le réseau a un coût total de {reseau.calculer_cout(terrain)}M€.")

                    # Afficher la validation du réseau
                    if reseau.valider_reseau() and reseau.valider_distribution(terrain): print("Le réseau est valide.\n")
                    else: print("Le réseau n'est pas valide.\n")

                    # Afficher le terrain et le réseau
                    reseau.afficher(terrain)
                    
                # Bloquer le programme jusqu'à ce que l'utilisateur appuie sur une touche
                input("Appuyez sur la touche Entrée pour continuer...")

                # Retour au menu principal
                os.system("clear")
                break
            elif choix == "3": # Afficher le terrain
                os.system("clear")

                # Afficher le coût du réseau
                print(f"Le réseau a un coût total de {reseau.calculer_cout(terrain)}M€.")

                # Afficher la validation du réseau
                if reseau.valider_reseau() and reseau.valider_distribution(terrain): print("Le réseau est valide.\n")
                else: print("Le réseau n'est pas valide.\n")
                
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
                print(f"Liste des terrains disponibles ({terrain.fichier}) :")
                terrains = [f for f in os.listdir("terrains") if f.endswith(".txt")]
                for i, t in enumerate(terrains):
                    print(f"{i+1} - {t.split('.')[0]}")
                print("r - Retour au menu principal")
                    
                # Récupérer le choix de l'utilisateur et charger le terrain
                while True:
                    choix = input("Votre choix : ")
                    if choix.isdigit():
                        # Charger le terrain
                        terrain.charger(f"terrains/{terrains[int(choix)-1]}", reseau)

                        # Retour au menu principal
                        break
                    elif choix == "r": break
                    else: print("Choix invalide.")
                
                # Retour au menu principal
                os.system("clear")
                break
            elif choix == "Q" or choix == "q": exit() # Quitter le programme
            else: print("Choix invalide.") # Choix invalide
from Terrain import Terrain, Case
from typing import TypedDict, Tuple
from itertools import permutations
from copy import deepcopy
import os

class NoeudDict(TypedDict):
    id: int
    coords: Tuple[int, int]

class StrategieReseau:
    def configurer(self, t: Terrain, noeuds: dict[int, tuple[int, int]], arcs: list[tuple[int, int]]) -> tuple[int, dict[int, tuple[int, int]], list[int]]:
        return -1, {}, []

class StrategieReseauManuelle(StrategieReseau):
    def configurer(self, t: Terrain, noeuds: dict[int, tuple[int, int]], arcs: list[tuple[int, int]]) -> tuple[int, dict[int, tuple[int, int]], list[int]]:
        def afficher_terrain(noeuds, arcs):
            # Supprimer la console
            os.system("clear")

            # Affichage du terrain
            print("Vue du terrain : ")
            t.afficher_avec_terrain(noeuds)

            # Affichage du réseau
            print("\nVue du réseau : ")
            t.afficher_avec_reseau(noeuds, arcs)
        def obtenir_id_noeud(coords: tuple[int, int]) -> int | None: return [id for id, c in noeuds.items() if c == coords][0]
        # Retourne la liste des voisins non-connectés à un noeud
        def noeuds_a_connecter(id_noeud: int) -> NoeudDict | list[None]:
            # Obtenir les voisins du noeud
            voisins = []
            if (noeuds[id_noeud][0] > 0 and (noeuds[id_noeud][0] - 1, noeuds[id_noeud][1]) in noeuds.values()): voisins.append({'id': obtenir_id_noeud((noeuds[id_noeud][0] - 1, noeuds[id_noeud][1])), 'coords': (noeuds[id_noeud][0] - 1, noeuds[id_noeud][1])})
            if (noeuds[id_noeud][0] < len(t.cases) - 1 and (noeuds[id_noeud][0] + 1, noeuds[id_noeud][1]) in noeuds.values()): voisins.append({'id': obtenir_id_noeud((noeuds[id_noeud][0] + 1, noeuds[id_noeud][1])), 'coords': (noeuds[id_noeud][0] + 1, noeuds[id_noeud][1])})
            if (noeuds[id_noeud][1] > 0 and (noeuds[id_noeud][0], noeuds[id_noeud][1] - 1) in noeuds.values()): voisins.append({'id': obtenir_id_noeud((noeuds[id_noeud][0], noeuds[id_noeud][1] - 1)), 'coords': (noeuds[id_noeud][0], noeuds[id_noeud][1] - 1)})
            if (noeuds[id_noeud][1] < len(t.cases[0]) - 1 and (noeuds[id_noeud][0], noeuds[id_noeud][1] + 1) in noeuds.values()): voisins.append({'id': obtenir_id_noeud((noeuds[id_noeud][0], noeuds[id_noeud][1] + 1)), 'coords': (noeuds[id_noeud][0], noeuds[id_noeud][1] + 1)})

            # Obtenir les arcs non connectés au noeud
            if len(voisins) > 0:
                # Supprimer les voisins connectés au noeud
                i = 0
                while i < len(voisins):
                    voisin = voisins[i]

                    # Vérifier si le voisin n'est pas connecté au noeud
                    if (id_noeud, voisin['id']) not in arcs and (voisin['id'], id_noeud) not in arcs: i += 1
                    else: del voisins[i]
                
                if len(voisins) > 0:
                    # Trier les voisins par ID croissant
                    voisins = sorted(voisins, key = lambda v: v['id'])
                    
                    return voisins
                # Tous les voisins sont connectés au noeud
                else: return [None]
            # Le noeud n'a pas de voisins
            else: return [None]

        predictions = {
            'noeud': {
                'prediction': {
                    'id': None,
                    'coords': None,
                },
                'direction': (None, None),
                'precedent': {
                    'id': None,
                    'coords': None
                }
            },
            'arc': None,
            'action': 'n',
        }

        # Récupérer les prédictions du noeud
        prediction = predictions['noeud']['prediction']
        direction = predictions['noeud']['direction']
        precedent = predictions['noeud']['precedent']

        # Charger les valeurs à prédire
        id_noeud = max(noeuds) if noeuds else None
        precedent['id'] = id_noeud; precedent['coords'] = noeuds[id_noeud] if noeuds else None
        if id_noeud != None:
            predictions['arc'] = noeuds_a_connecter(id_noeud)[0] if noeuds else None

            # Prédiction de l'ID du prochain noeud
            prediction['id'] = id_noeud + 1
            while prediction['id'] in noeuds: prediction['id'] += 1

        while True:
            afficher_terrain(noeuds, arcs)
            action = input("Voulez-vous ajouter un élément (a), modifier un élément (m), supprimer un élément (s) ou terminer (t) ? (a) : ")
            if action == '': action = 'a'

            if action == 't' or action == 'T': break
            elif action == 'a' or action == 'A':
                # Choix de l'élément à ajouter
                type_element = input(f"Voulez-vous ajouter un noeud (n) ou un arc (a), ou retourner au menu précédent (r) ? ({predictions['action']}) : ")
                if type_element == '': type_element = predictions['action']

                # Ajout d'un noeud
                if type_element == 'n' or type_element == 'N':
                    # Prédiction du prochain ajout
                    predictions['action'] = 'n'

                    # Obtenir l'ID du nouveau noeud
                    while True:
                        user_input = input(f"Entrez l'ID du noeud ({prediction['id']}) : " if prediction['id'] else "Entrez l'ID du noeud : ")
                        if (user_input == 'r' or user_input == 'R'): break
                        id_noeud = int(user_input) if user_input else (prediction['id'] if prediction['id'] != None else -1)
                        
                        if id_noeud in noeuds: print("Cet ID de noeud existe déjà. Veuillez en entrer un autre.")
                        else: break
                    # Retourner au menu principal
                    if (user_input == 'r' or user_input == 'R'): continue
                    
                    # Obtenir les coordonnées du nouveau noeud
                    while True:
                        # x input
                        while True:
                            user_input = input(f"- Entrez la coordonnée x du noeud ({prediction['coords'][1]}) : " if prediction['coords'] else f"- Entrez la coordonnée x du noeud (précedemment {precedent['coords'][1]}) : ")
                            if (user_input == 'r' or user_input == 'R'): break
                            x = int(user_input) if user_input else (prediction['coords'][1] if prediction['coords'] else (precedent['coords'][1] if precedent['coords'] != None else -1))
                            
                            if x < 0 or x >= len(t.cases[0]): print(f"La coordonnée x doit être comprise entre 0 et {len(t.cases[0]) - 1}.")
                            else: break
                        # Retourner au menu principal
                        if (user_input == 'r' or user_input == 'R'): break
                        
                        # y input
                        while True:
                            user_input = input(f"- Entrez la coordonnée y du noeud ({prediction['coords'][0]}) : " if prediction['coords'] else f"- Entrez la coordonnée y du noeud (précédemment {precedent['coords'][0]}) : ")
                            if (user_input == 'r' or user_input == 'R'): break
                            y = int(user_input) if user_input else (prediction['coords'][0] if prediction['coords'] else (precedent['coords'][0] if precedent['coords'] else -1))
                            
                            if y < 0 or y >= len(t.cases): print(f"La coordonnée y doit être comprise entre 0 et {len(t.cases) - 1}.")
                            else: break
                        # Retourner au menu principal
                        if (user_input == 'r' or user_input == 'R'): break

                        if (y, x) in noeuds.values():
                            print("Un noeud existe déjà à ces coordonnées. Veuillez en entrer d'autres.")
                            continue
                        
                        if (prediction['coords'] == None or (y == prediction['coords'][0] and x == prediction['coords'][1])):
                            # Prédiction de la direction
                            if precedent['coords'] is None: direction = (None, None)
                            elif precedent['coords'][0] == y-1 and precedent['coords'][1] == x: direction = (1, 0)
                            elif precedent['coords'][0] == y+1 and precedent['coords'][1] == x: direction = (-1, 0)
                            elif precedent['coords'][0] == y and precedent['coords'][1] == x-1: direction = (0, 1)
                            elif precedent['coords'][0] == y and precedent['coords'][1] == x+1: direction = (0, -1)
                            else: direction = (None, None)

                            # Vérification des coordonnées par rapport à la direction
                            if direction != (None, None) and (
                                (direction[0] == 1 and y == len(t.cases) - 1) or
                                (direction[0] == -1 and y == 0) or
                                (direction[1] == 1 and x == len(t.cases[0]) - 1) or
                                (direction[1] == -1 and x == 0) or
                                (y + direction[0], x + direction[1]) in noeuds.values()
                            ): direction = (None, None)
                            
                            prediction['coords'] = (y + direction[0], x + direction[1]) if direction != (None, None) else None
                        else:
                            direction = (None, None)
                            prediction['coords'] = None

                        # Ajout du noeud
                        noeuds[id_noeud] = (y, x)

                        # Prédiction du premier noeud de l'arc
                        predictions['arc'] = id_noeud

                        # Mise à jour du noeud précédent
                        precedent['id'] = id_noeud; precedent['coords'] = (y, x)

                        # Prédiction du prochain noeud
                        while id_noeud in noeuds: id_noeud += 1
                        prediction['id'] = id_noeud

                        break
                # Ajout d'un arc
                elif type_element == 'a' or type_element == 'A':
                    # Prédiction du prochain ajout
                    predictions['action'] = 'a'

                    while True:
                        # Obtenir l'ID du noeud de départ
                        while True:
                            user_input = input(f"Entrez l'ID du noeud de départ ({predictions['arc']}) : " if predictions['arc'] and noeuds_a_connecter(predictions['arc'])[0] else "Entrez l'ID du noeud de départ : ")
                            if (user_input == 'r' or user_input == 'R'): break
                            noeud_depart = int(user_input) if user_input else (predictions['arc'] if predictions['arc'] else -1)

                            # Vérifier si l'ID du noeud de départ existe
                            if noeud_depart not in noeuds:
                                print("Ce noeud n'existe pas. Veuillez en choisir un autre.")
                                continue
                            
                            # Vérifier si le noeud a des voisins non-connectés
                            voisin = noeuds_a_connecter(noeud_depart)[0]
                            if voisin:
                                pred_noeud_arrivee = voisin['id']
                                break
                            # Aucun noeud n'est connecté à ce noeud
                            else: print("Aucun noeud à connecter aux alentours. Veuillez en entrer un autre.")
                        # Retourner au menu principal
                        if (user_input == 'r' or user_input == 'R'): break
                        
                        # Obtenir l'ID du noeud d'arrivée
                        while True:
                            user_input = input(f"Entrez l'ID du noeud d'arrivée ({pred_noeud_arrivee}) : ")
                            if (user_input == 'r' or user_input == 'R'): break
                            noeud_arrivee = int(user_input) if user_input else pred_noeud_arrivee

                            # Vérifier si l'ID du noeud d'arrivée existe
                            if noeud_arrivee not in noeuds: print("Ce noeud n'existe pas. Veuillez en choisir un autre.")
                            else: break
                        # Retourner au menu principal
                        if (user_input == 'r' or user_input == 'R'): break

                        # Vérifier si l'arc existe déjà
                        if (noeud_depart, noeud_arrivee) in arcs or (noeud_arrivee, noeud_depart) in arcs: print("Cet arc existe déjà. Veuillez en entrer un autre.")
                        else:
                            # Ajout de l'arc
                            arcs.append((noeud_depart, noeud_arrivee))

                            # Prédiction du noeud de départ
                            if noeuds_a_connecter(noeud_arrivee)[0]: predictions['arc'] = noeud_arrivee
                            else: predictions['arc'] = None

                            break
                # Retourner au menu principal
                elif type_element != 'r' and type_element != 'R': print("Action non reconnue. Veuillez entrer 'n', 'a' ou 'r'.")
            elif action == 'm' or action == 'M':
                type_element = input(f"Voulez-vous modifier un noeud (n) ou un arc (a), ou retourner (r) ? ({predictions['action']}) : ")
                if (type_element == ''): type_element = predictions['action']

                if type_element == 'n' or type_element == 'N':
                    # Chercher le noeud à modifier
                    while True:
                        # Obtenir l'ID du noeud à modifier
                        user_input = input(f"Entrez l'ID du noeud à modifier ({prediction['id']}) : " if prediction['id'] else "Entrez l'ID du noeud à modifier : ")
                        if (user_input == 'r' or user_input == 'R'): break
                        id_noeud = int(user_input) if user_input else (prediction['id'] if prediction['id'] else -1)

                        # Vérifier si l'ID du noeud existe
                        if id_noeud not in noeuds: print("Cet ID de noeud n'existe pas. Veuillez en entrer un autre.")
                        else: break
                    # Retourner au menu principal
                    if (user_input == 'r' or user_input == 'R'): continue

                    # Obtenir les nouvelles coordonnées du noeud
                    while True:
                        # x input
                        while True:
                            user_input = input(f"- Entrez la nouvelle coordonnée x du noeud ({noeuds[id_noeud][1]}) : ")
                            if (user_input == 'r' or user_input == 'R'): break
                            x = int(user_input) if user_input else (noeuds[id_noeud][1] if noeuds[id_noeud][1] != None else -1)
                            
                            if x < 0 or x >= len(t.cases[0]): print("La coordonnée x doit être comprise entre 0 et la largeur du terrain.")
                            else: break
                        
                        if (user_input == 'r' or user_input == 'R'): break
                        # y input
                        while True:
                            user_input = input(f"- Entrez la nouvelle coordonnée y du noeud ({noeuds[id_noeud][0]}) : ")
                            if (user_input == 'r' or user_input == 'R'): break
                            y = int(user_input) if user_input else (noeuds[id_noeud][0] if noeuds[id_noeud][0] != None else -1)
                            
                            if y < 0 or y >= len(t.cases): print("La coordonnée y doit être comprise entre 0 et la hauteur du terrain.")
                            else: break
                        # Retourner au menu principal
                        if (user_input == 'r' or user_input == 'R'): break

                        # Vérifier si un noeud existe déjà à ces coordonnées
                        if (y, x) in noeuds.values():
                            print("Un noeud existe déjà à ces coordonnées. Veuillez en entrer d'autres.")
                            continue
                        
                        # Modifier le noeud dans la liste
                        noeuds[id_noeud] = (y, x)

                        # Modifier la prédiction du noeud
                        if direction: prediction['coords'] = (y + direction[0], x + direction[1])
                elif type_element == 'a' or type_element == 'A':
                    ## Chercher l'arc à modifier
                    print("Identification de l'arc à modifier :")

                    # Obtenir l'ID du noeud de départ
                    while True:
                        user_input = input(f"- Entrez l'ID du noeud de départ ({predictions['arc']}) : " if predictions['arc'] else "- Entrez l'ID du noeud de départ : ")
                        if (user_input == 'r' or user_input == 'R'): break
                        noeud_depart = int(user_input) if user_input else (predictions['arc'] if predictions['arc'] else -1)

                        # Vérifier si l'ID du noeud de départ existe
                        if noeud_depart not in noeuds:
                            print("- Cet ID de noeud n'existe pas. Veuillez en entrer un autre.")
                            continue
                            
                        # Obtenir les voisins et vérifier si le noeud a des arcs
                        voisins = [arc for arc in arcs if arc[0] == noeud_depart or arc[1] == noeud_depart]
                        if not voisins:
                            print("Cet ID de noeud n'est pas un noeud de départ d'un arc. Veuillez en entrer un autre.")
                            continue
                    # Retourner au menu principal
                    if (user_input == 'r' or user_input == 'R'): continue

                    # Obtenir l'ID du noeud d'arrivée
                    while True:
                        user_input = input(f"- Entrez l'ID du noeud d'arrivée ({voisins[0]}) : ")
                        if (user_input == 'r' or user_input == 'R'): break
                        noeud_arrivee = int(user_input) if user_input else voisins[0]

                        # Vérifier si l'ID du noeud d'arrivée existe
                        if noeud_arrivee not in noeuds:
                            print("Cet ID de noeud n'existe pas. Veuillez en entrer un autre.")
                            continue

                        # Vérifier si l'arc existe
                        if (noeud_depart, noeud_arrivee) in voisins:
                            print("Cet arc n'existe pas. Veuillez en entrer un autre.")
                            continue
                        
                        break
                    # Retourner au menu principal
                    if (user_input == 'r' or user_input == 'R'): continue

                    # Modifier l'arc
                    arc = (noeud_depart, noeud_arrivee)
                    id_arc = [i for i, a in enumerate(arcs) if a == arc][0]


                    ## Modification de l'arc
                    print("Modification de l'arc :")
                    while True:
                        # Obtenir l'ID du noeud de départ
                        while True:
                            user_input = input(f"- Entrez l'ID du noeud de départ ({noeud_arrivee}) : ")
                            if (user_input == 'r' or user_input == 'R'): break
                            new_noeud_depart = int(user_input) if user_input else noeud_arrivee

                            # Vérifier si l'ID du noeud de départ existe
                            if new_noeud_depart not in noeuds: print("Cet ID de noeud n'existe pas. Veuillez en entrer un autre.")
                            else: break
                        # Retourner au menu principal
                        if (user_input == 'r' or user_input == 'R'): break

                        # Obtenir l'ID du noeud d'arrivée
                        while True:
                            user_input = input(f"- Entrez l'ID du noeud d'arrivée ({noeud_depart}) : ")
                            if (user_input == 'r' or user_input == 'R'): break
                            new_noeud_arrivee = int(user_input) if user_input else noeud_depart

                            # Vérifier si l'ID du noeud d'arrivée existe
                            if new_noeud_arrivee not in noeuds: print("Cet ID de noeud n'existe pas. Veuillez en entrer un autre.")
                            else: break
                        # Retourner au menu principal
                        if (user_input == 'r' or user_input == 'R'): break
                        
                        # Vérifier si au moins l'un des noeuds fait partie de l'arc à modifier
                        if ((new_noeud_depart != noeud_depart and new_noeud_arrivee != noeud_arrivee) or
                            (new_noeud_depart != noeud_arrivee and new_noeud_arrivee != noeud_depart)):
                            print("Au moins un des noeuds doit être identique à un des noeuds de l'arc à modifier.")
                            continue

                        # Vérifier si le nouvel arc choisi existe déjà
                        if (new_noeud_depart, new_noeud_arrivee) in arcs or (new_noeud_arrivee, new_noeud_depart) in arcs:
                            print("Cet arc existe déjà. Veuillez en entrer un autre.")
                            continue

                        # Modifier l'arc dans la liste
                        arcs[id_arc] = (new_noeud_depart, new_noeud_arrivee)

                        # Prédiction de l'arc
                        predictions['arc'] = new_noeud_arrivee

                        break
                elif type_element != 'r' and type_element != 'R': print("Action non reconnue. Veuillez entrer 'n', 'a' ou 'r'.")
            elif action == 's' or action == 'S':
                type_element = input(f"Voulez-vous supprimer un noeud (n) ou un arc (a), ou retourner (r) ? ({predictions['action']}) ")
                if (type_element == ''): type_element = predictions['action']

                if type_element == 'n' or type_element == 'N':
                    while True:
                        # Obtenir l'ID du noeud à supprimer
                        user_input = input(f"- Entrez l'ID du noeud à supprimer ({prediction['id']}) : " if prediction['id'] != None else "- Entrez l'ID du noeud à supprimer : ")
                        if (user_input == 'r' or user_input == 'R'): break
                        id_noeud = int(user_input) if user_input else (prediction['id'] if prediction['id'] != None else -1)

                        # Vérifier si l'ID du noeud existe
                        if id_noeud not in noeuds: print("Ce noeud n'existe pas. Veuillez en choisir un autre.")
                        else: break
                    # Retourner au menu principal
                    if (user_input == 'r' or user_input == 'R'): continue
                    
                    # Supprimer le noeud de la liste
                    del noeuds[id_noeud]

                    # Supprimer les arcs liés au noeud
                    arcs = [arc for arc in arcs if arc[0] != id_noeud and arc[1] != id_noeud]

                    # Enlever les prédictions du noeud
                    if precedent['id'] == id_noeud:
                        precedent['id'] = None; prediction['coords'] = None
                        prediction['id'] = None;  prediction['coords'] = None
                        direction = (None, None)
                    
                    # Enlever la prédiction de l'arc si l'arc prédit le noeud supprimé
                    if predictions['arc'] == id_noeud: predictions['arc'] = None
                elif type_element == 'a' or type_element == 'A':
                    while True:
                        # Obtenir l'ID du noeud de départ
                        while True:
                            user_input = input(f"- Entrez l'ID du noeud de départ ({predictions['arc']}) : " if predictions['arc'] else "- Entrez l'ID du noeud de départ : ")
                            if (user_input == 'r' or user_input == 'R'): break
                            noeud_depart = int(user_input) if user_input else (predictions['arc'] if predictions['arc'] else -1)

                            # Vérifier si l'ID du noeud de départ existe
                            if noeud_depart not in noeuds: print("Cet ID de noeud n'existe pas. Veuillez en entrer un autre.")
                            else: break

                            # Obtenir les voisins et vérifier si le noeud a des arcs
                            voisins = [arc for arc in arcs if arc[0] == noeud_depart or arc[1] == noeud_depart]
                            if not voisins:
                                print("Ce noeud n'a pas d'arc. Veuillez entrer un autre noeud.")
                                continue

                            break
                        # Retourner au menu principal
                        if (user_input == 'r' or user_input == 'R'): break

                        # Obtenir l'ID du noeud d'arrivée
                        while True:
                            user_input = input(f"- Entrez l'ID du noeud d'arrivée ({voisins[0]}) : ")
                            if (user_input == 'r' or user_input == 'R'): break
                            noeud_arrivee = int(user_input) if user_input else voisins[0]

                            # Vérifier si l'ID du noeud d'arrivée existe
                            if noeud_arrivee not in noeuds: print("Ce noeud n'existe pas. Veuillez en entrer un autre.")
                            else: break
                        # Retourner au menu principal
                        if (user_input == 'r' or user_input == 'R'): break
                        
                        # Vérifier si l'arc existe
                        if (noeud_depart, noeud_arrivee) not in arcs:
                            print("Cet arc n'existe pas. Veuillez en entrer un autre.")
                            continue
                        
                        # Supprimer l'arc de la liste
                        arcs = [arc for arc in arcs if arc != (noeud_depart, noeud_arrivee)]
                            
                        # Enlever la prédiction de l'arc
                        if predictions['arc'] == noeud_arrivee: predictions['arc'] = None
                        
                        break
                elif type_element != 'r' and type_element != 'R': print("Action non reconnue. Veuillez entrer 'n', 'a' ou 'r'.")
            else: print("Action non reconnue. Veuillez entrer 'a', 'm', 's' ou 't'.")
        
        # Obtenir l'ID du noeud de l'entrée
        id_entree = [id_noeud for id_noeud, coord in noeuds.items() if coord == t.get_entree()]
        id_entree = id_entree[0] if id_entree else -1
        
        return id_entree, noeuds, arcs

class StrategieReseauAuto(StrategieReseau):
    def configurer(self, t: Terrain, noeuds: dict[int, tuple[int, int]], arcs: list[tuple[int, int]]) -> tuple[int, dict[int, tuple[int, int]], list[int]]:
        def creer_simulation(sim: dict[str, any],
                             cout: float,
                             noeud_depart: tuple[int, int],
                             noeud_arrivee: tuple[int, int],
                             direction: tuple[int, int] = None,
                             obstacle: tuple[int, int] = None,
                             arcs_a_eviter: list[tuple[int, int]] = []) -> dict[str, any] | list[dict[str, any]]:
            if noeud_arrivee in sim['noeuds'].values(): return sim

            if (obstacle == None):
                # Vérifier si un chemin direct est possible
                if (noeud_depart[0] == noeud_arrivee[0]):
                    # Créer une direction
                    dir = 1 if noeud_depart[1] < noeud_arrivee[1] else -1

                    for x in range(noeud_depart[1] + dir, noeud_arrivee[1] + dir, dir):
                        # Vérifier si un obstacle est présent
                        if ((noeud_depart[0], x) not in t.get_obstacles()):
                            # Vérifier si un noeud est déjà présent, sinon le créer
                            if (noeud_depart[0], x) not in sim['noeuds'].values():
                                id_noeud = len(sim['noeuds'])
                                sim['noeuds'][id_noeud] = (noeud_depart[0], x)
                                sim['cout'] += 1

                                # Vérifier le coût du chemin
                                if (sim['cout'] > cout): return None
                            else: id_noeud = [id_noeud for id_noeud, coord in sim['noeuds'].items() if coord == (noeud_depart[0], x)][0]

                            # Vérifier si un arc est déjà présent, sinon le créer
                            id_noeud_precedent = [id_noeud for id_noeud, coord in sim['noeuds'].items() if coord == (noeud_depart[0], x - dir)][0]
                            if ((id_noeud_precedent, id_noeud) not in sim['arcs']):
                                sim['arcs'].append((id_noeud_precedent, id_noeud))
                                sim['cout'] += 1.5

                                # Vérifier le coût du chemin
                                if (sim['cout'] > cout): return None
                            elif ((id_noeud_precedent, id_noeud) in arcs_a_eviter): return None
                        else:
                            # Créer deux simulations verticales
                            sim1 = creer_simulation(deepcopy(sim), cout, (noeud_depart[0], x - dir), noeud_arrivee, (-1, 0), (0, dir), deepcopy(arcs_a_eviter)) if direction is None or direction[0] == -1 else None
                            sim2 = creer_simulation(deepcopy(sim), cout, (noeud_depart[0], x - dir), noeud_arrivee, (1, 0), (0, dir), deepcopy(arcs_a_eviter)) if direction is None or direction[0] == 1 else None
                            
                            if (sim1 != None and sim2 != None):
                                if (type(sim1) == list and type(sim2) == list): return sim1 + sim2
                                elif (type(sim1) == list and type(sim2) == dict): return sim1 + [sim2]
                                elif (type(sim1) == dict and type(sim2) == list): return [sim1] + sim2
                                elif (type(sim1) == dict and type(sim2) == dict): return [sim1, sim2]
                            elif (sim1 != None): return sim1
                            elif (sim2 != None): return sim2
                            else: return None
                    return sim
                elif (noeud_depart[1] == noeud_arrivee[1]):
                    # Créer une direction
                    dir = 1 if noeud_depart[0] < noeud_arrivee[0] else -1

                    for y in range(noeud_depart[0] + dir, noeud_arrivee[0] + dir, dir):
                        # Vérifier si un obstacle est présent
                        if ((y, noeud_depart[1]) not in t.get_obstacles()):
                            # Vérifier si un noeud est déjà présent, sinon le créer
                            if (y, noeud_depart[1] not in sim['noeuds'].values()):
                                id_noeud = len(sim['noeuds'])
                                sim['noeuds'][id_noeud] = (y, noeud_depart[1])
                                sim['cout'] += 1

                                # Vérifier le coût du chemin
                                if (sim['cout'] > cout): return None
                            else: id_noeud = [id_noeud for id_noeud, coord in sim['noeuds'].items() if coord == (y, noeud_depart[1])][0]

                            # Vérifier si un arc est déjà présent, sinon le créer
                            id_noeud_precedent = [id_noeud for id_noeud, coord in sim['noeuds'].items() if coord == (y - dir, noeud_depart[1])][0]
                            if ((id_noeud_precedent, id_noeud) not in sim['arcs']):
                                sim['arcs'].append((id_noeud_precedent, id_noeud))
                                sim['cout'] += 1.5

                                # Vérifier le coût du chemin
                                if (sim['cout'] > cout): return None
                            elif ((id_noeud_precedent, id_noeud) in arcs_a_eviter): return None
                        else:
                            # Créer deux simulations horizontales
                            sim1 = creer_simulation(deepcopy(sim), cout, (y - dir, noeud_depart[1]), noeud_arrivee, (0, -1), (dir, 0), deepcopy(arcs_a_eviter)) if direction is None or direction[1] == -1 else None
                            sim2 = creer_simulation(deepcopy(sim), cout, (y - dir, noeud_depart[1]), noeud_arrivee, (0, 1), (dir, 0), deepcopy(arcs_a_eviter)) if direction is None or direction[1] == 1 else None
                            
                            if (sim1 != None and sim2 != None):
                                if (type(sim1) == list and type(sim2) == list): return sim1 + sim2
                                elif (type(sim1) == list and type(sim2) == dict): return sim1 + [sim2]
                                elif (type(sim1) == dict and type(sim2) == list): return [sim1] + sim2
                                elif (type(sim1) == dict and type(sim2) == dict): return [sim1, sim2]
                            elif (sim1 != None): return sim1
                            elif (sim2 != None): return sim2
                            else: return None
                    return sim
                elif (direction == None):
                    # Créer deux simulations pour chaque noeud
                    simulations = []
                    for noeud in sim['noeuds'].values():
                        # Créer deux directions
                        directions = [
                            (1, 0) if noeud[0] < noeud_arrivee[0] else (-1, 0),
                            (0, 1) if noeud[1] < noeud_arrivee[1] else (0, -1)
                        ]

                        # Créer deux simulations, une verticale et une horizontale
                        sim1 = creer_simulation(deepcopy(sim), cout, noeud, noeud_arrivee, directions[0], None, deepcopy(arcs_a_eviter)) # Simulation verticale
                        sim2 = creer_simulation(deepcopy(sim), cout, noeud, noeud_arrivee, directions[1], None, deepcopy(arcs_a_eviter)) # Simulation horizontale

                        if (sim1 != None):
                            if (type(sim1) == list): simulations += sim1
                            else: simulations.append(sim1)
                        if (sim2 != None):
                            if (type(sim2) == list): simulations += sim2
                            else: simulations.append(sim2)
                        
                    if (len(simulations) == 0): return None
                    elif (len(simulations) == 1): return simulations[0]
                    else: return simulations
                elif (direction[0] != 0):
                    for y in range(noeud_depart[0] + direction[0], noeud_arrivee[0] + direction[0], direction[0]):
                        # Vérifier si un obstacle est présent
                        if ((y, noeud_depart[1]) not in t.get_obstacles()):
                            # Vérifier si un noeud est déjà présent, sinon le créer
                            if ((y, noeud_depart[1]) not in sim['noeuds'].values()):
                                id_noeud = len(sim['noeuds'])
                                sim['noeuds'][id_noeud] = (y, noeud_depart[1])
                                sim['cout'] += 1

                                # Vérifier le coût du chemin
                                if (sim['cout'] > cout): return None
                            else: id_noeud = [id_noeud for id_noeud, coord in sim['noeuds'].items() if coord == (y, noeud_depart[1])][0]

                            # Vérifier si un arc est déjà présent, sinon le créer
                            id_noeud_precedent = [id_noeud for id_noeud, coord in sim['noeuds'].items() if coord == (y - direction[0], noeud_depart[1])][0]
                            if (((id_noeud_precedent, id_noeud) not in sim['arcs']) and ((id_noeud, id_noeud_precedent) not in sim['arcs'])):
                                sim['arcs'].append((id_noeud_precedent, id_noeud))
                                sim['cout'] += 1.5

                                # Vérifier le coût du chemin
                                if (sim['cout'] > cout): return None
                            elif ((id_noeud_precedent, id_noeud) in arcs_a_eviter): return None
                        else:
                            if ((y == 0 or y == len(t.cases) - 1) and (y == noeud_arrivee[0])):
                                dir = 1 if noeud_depart[1] < noeud_arrivee[1] else -1

                                if (t.cases[y][noeud_depart[1] + dir] == Case.OBSTACLE): return None

                            # Créer deux simulations horizontales
                            sim1 = creer_simulation(deepcopy(sim), cout, (y - direction[0], noeud_depart[1]), noeud_arrivee, (0, -1), direction, deepcopy(arcs_a_eviter))
                            sim2 = creer_simulation(deepcopy(sim), cout, (y - direction[0], noeud_depart[1]), noeud_arrivee, (0, 1), direction, deepcopy(arcs_a_eviter))
                            
                            if (sim1 != None and sim2 != None):
                                if (type(sim1) == list and type(sim2) == list): return sim1 + sim2
                                elif (type(sim1) == list and type(sim2) == dict): return sim1 + [sim2]
                                elif (type(sim1) == dict and type(sim2) == list): return [sim1] + sim2
                                elif (type(sim1) == dict and type(sim2) == dict): return [sim1, sim2]
                            elif (sim1 != None): return sim1
                            elif (sim2 != None): return sim2
                            else: return None
                    return creer_simulation(deepcopy(sim), cout, (y, noeud_depart[1]), noeud_arrivee, None, None, deepcopy(arcs_a_eviter))
                elif (direction[1] != 0):
                    for x in range(noeud_depart[1] + direction[1], noeud_arrivee[1] + direction[1], direction[1]):
                        # Vérifier si un obstacle est présent
                        if ((noeud_depart[0], x) not in t.get_obstacles()):
                            # Vérifier si un noeud est déjà présent, sinon le créer
                            if (noeud_depart[0], x) not in sim['noeuds'].values():
                                id_noeud = len(sim['noeuds'])
                                sim['noeuds'][id_noeud] = (noeud_depart[0], x)
                                sim['cout'] += 1

                                # Vérifier le coût du chemin
                                if (sim['cout'] > cout): return None
                            else: id_noeud = [id_noeud for id_noeud, coord in sim['noeuds'].items() if coord == (noeud_depart[0], x)][0]

                            # Vérifier si un arc est déjà présent, sinon le créer
                            id_noeud_precedent = [id_noeud for id_noeud, coord in sim['noeuds'].items() if coord == (noeud_depart[0], x - direction[1])][0]
                            if (((id_noeud_precedent, id_noeud) not in sim['arcs']) and ((id_noeud, id_noeud_precedent) not in sim['arcs'])):
                                sim['arcs'].append((id_noeud_precedent, id_noeud))
                                sim['cout'] += 1.5

                                # Vérifier le coût du chemin
                                if (sim['cout'] > cout): return None
                            elif ((id_noeud_precedent, id_noeud) in arcs_a_eviter): return None
                        else:
                            if ((x == 0 or x == len(t.cases[0]) - 1) and (x == noeud_arrivee[1])):
                                dir = 1 if noeud_depart[0] < noeud_arrivee[0] else -1

                                if (t.cases[noeud_depart[0] + dir][x] == Case.OBSTACLE): return None
                            
                            # Créer deux simulations verticales
                            sim1 = creer_simulation(deepcopy(sim), cout, (noeud_depart[0], x - direction[1]), noeud_arrivee, (-1, 0), deepcopy(direction), deepcopy(arcs_a_eviter))
                            sim2 = creer_simulation(deepcopy(sim), cout, (noeud_depart[0], x - direction[1]), noeud_arrivee, (1, 0), deepcopy(direction), deepcopy(arcs_a_eviter))
                            
                            if (sim1 != None and sim2 != None):
                                if (type(sim1) == list and type(sim2) == list): return sim1 + sim2
                                elif (type(sim1) == list and type(sim2) == dict): return sim1 + [sim2]
                                elif (type(sim1) == dict and type(sim2) == list): return [sim1] + sim2
                                elif (type(sim1) == dict and type(sim2) == dict): return [sim1, sim2]
                            elif (sim1 != None): return sim1
                            elif (sim2 != None): return sim2
                            else: return None
                    return creer_simulation(deepcopy(sim), cout, (noeud_depart[0], x), noeud_arrivee, None, None, deepcopy(arcs_a_eviter))
            elif (direction[1] == -1):
                for x in range(noeud_depart[1] - 1, -1, -1):
                    # Vérifier si un obstacle est présent
                    if ((noeud_depart[0], x) not in t.get_obstacles()):
                        # Vérifier si un noeud est déjà présent, sinon le créer
                        if (noeud_depart[0], x) not in sim['noeuds'].values():
                            id_noeud = len(sim['noeuds'])
                            sim['noeuds'][id_noeud] = (noeud_depart[0], x)
                            sim['cout'] += 1
                            
                            # Vérifier le coût du chemin
                            if (sim['cout'] > cout): return None
                        else: id_noeud = [id_noeud for id_noeud, coord in sim['noeuds'].items() if coord == (noeud_depart[0], x)][0]
                        
                        # Vérifier si un arc est déjà présent, sinon le créer
                        id_noeud_precedent = [id_noeud for id_noeud, coord in sim['noeuds'].items() if coord == (noeud_depart[0], x + 1)][0]
                        if (((id_noeud_precedent, id_noeud) not in sim['arcs']) and ((id_noeud, id_noeud_precedent) not in sim['arcs'])):
                            sim['arcs'].append((id_noeud_precedent, id_noeud))
                            arcs_a_eviter.append((id_noeud_precedent, id_noeud))
                            sim['cout'] += 1.5

                            # Vérifier le coût du chemin
                            if (sim['cout'] > cout): return None
                        # Invalider le chemin si l'arc a déjà été parcouru
                        elif ((id_noeud_precedent, id_noeud) in arcs_a_eviter): return None

                        # Vérifier si l'obstacle a été contourné avec succès
                        if ((noeud_depart[0] + obstacle[0], x) not in t.get_obstacles()):
                            return creer_simulation(deepcopy(sim), cout, (noeud_depart[0], x), noeud_arrivee, deepcopy(obstacle), None, deepcopy(arcs_a_eviter))
                    else:
                        # Créer deux simulations verticales
                        sim1 = creer_simulation(deepcopy(sim), cout, (noeud_depart[0], x + 1), noeud_arrivee, (-1, 0), (0, -1), deepcopy(arcs_a_eviter))
                        sim2 = creer_simulation(deepcopy(sim), cout, (noeud_depart[0], x + 1), noeud_arrivee, (1, 0), (0, -1), deepcopy(arcs_a_eviter))
                        
                        if (sim1 != None and sim2 != None):
                            if (type(sim1) == list and type(sim2) == list): return sim1 + sim2
                            elif (type(sim1) == list and type(sim2) == dict): return sim1 + [sim2]
                            elif (type(sim1) == dict and type(sim2) == list): return [sim1] + sim2
                            elif (type(sim1) == dict and type(sim2) == dict): return [sim1, sim2]
                        elif (sim1 != None): return sim1
                        elif (sim2 != None): return sim2
                        else: return None
                
                # Le bord gauche est atteint, invalider le chemin
                return None
            elif (direction[1] == 1):
                for x in range(noeud_depart[1] + 1, len(t.cases[0])):
                    # Vérifier si un obstacle est présent
                    if ((noeud_depart[0], x) not in t.get_obstacles()):
                        # Vérifier si un noeud est déjà présent, sinon le créer
                        if (noeud_depart[0], x) not in sim['noeuds'].values():
                            id_noeud = len(sim['noeuds'])
                            sim['noeuds'][id_noeud] = (noeud_depart[0], x)
                            sim['cout'] += 1
                            
                            # Vérifier le coût du chemin
                            if (sim['cout'] > cout): return None
                        else: id_noeud = [id_noeud for id_noeud, coord in sim['noeuds'].items() if coord == (noeud_depart[0], x)][0]
                        
                        # Vérifier si un arc est déjà présent, sinon le créer
                        id_noeud_precedent = [id_noeud for id_noeud, coord in sim['noeuds'].items() if coord == (noeud_depart[0], x - 1)][0]
                        if (((id_noeud_precedent, id_noeud) not in sim['arcs']) and ((id_noeud, id_noeud_precedent) not in sim['arcs'])):
                            sim['arcs'].append((id_noeud_precedent, id_noeud))
                            arcs_a_eviter.append((id_noeud_precedent, id_noeud))
                            sim['cout'] += 1.5

                            # Vérifier le coût du chemin
                            if (sim['cout'] > cout): return None
                        # Invalider le chemin si l'arc a déjà été parcouru
                        elif ((id_noeud_precedent, id_noeud) in arcs_a_eviter): return None

                        # Vérifier si l'obstacle a été contourné avec succès
                        if ((noeud_depart[0] + obstacle[0], x) not in t.get_obstacles()):
                            return creer_simulation(deepcopy(sim), cout, (noeud_depart[0], x), noeud_arrivee, deepcopy(obstacle), None, deepcopy(arcs_a_eviter))
                    else:
                        # Créer deux simulations verticales
                        sim1 = creer_simulation(deepcopy(sim), cout, (noeud_depart[0], x - 1), noeud_arrivee, (-1, 0), (0, 1), deepcopy(arcs_a_eviter))
                        sim2 = creer_simulation(deepcopy(sim), cout, (noeud_depart[0], x - 1), noeud_arrivee, (1, 0), (0, 1), deepcopy(arcs_a_eviter))
                        
                        if (sim1 != None and sim2 != None):
                            if (type(sim1) == list and type(sim2) == list): return sim1 + sim2
                            elif (type(sim1) == list and type(sim2) == dict): return sim1 + [sim2]
                            elif (type(sim1) == dict and type(sim2) == list): return [sim1] + sim2
                            elif (type(sim1) == dict and type(sim2) == dict): return [sim1, sim2]
                        elif (sim1 != None): return sim1
                        elif (sim2 != None): return sim2
                        else: return None
                        
                # Le bord droit est atteint, invalider le chemin
                return None
            elif (direction[0] == -1):
                for y in range(noeud_depart[0] - 1, -1, -1):
                    # Vérifier si un obstacle est présent
                    if ((y, noeud_depart[1]) not in t.get_obstacles()):
                        # Vérifier si un noeud est déjà présent, sinon le créer
                        if (y, noeud_depart[1]) not in sim['noeuds'].values():
                            id_noeud = len(sim['noeuds'])
                            sim['noeuds'][id_noeud] = (y, noeud_depart[1])
                            sim['cout'] += 1
                            
                            # Vérifier le coût du chemin
                            if (sim['cout'] > cout): return None
                        else: id_noeud = [id_noeud for id_noeud, coord in sim['noeuds'].items() if coord == (y, noeud_depart[1])][0]
                        
                        # Vérifier si un arc est déjà présent, sinon le créer
                        id_noeud_precedent = [id_noeud for id_noeud, coord in sim['noeuds'].items() if coord == (y + 1, noeud_depart[1])][0]
                        if (((id_noeud_precedent, id_noeud) not in sim['arcs']) and ((id_noeud, id_noeud_precedent) not in sim['arcs'])):
                            sim['arcs'].append((id_noeud_precedent, id_noeud))
                            arcs_a_eviter.append((id_noeud_precedent, id_noeud))
                            sim['cout'] += 1.5

                            # Vérifier le coût du chemin
                            if (sim['cout'] > cout): return None
                        # Invalider le chemin si l'arc a déjà été parcouru
                        elif ((id_noeud_precedent, id_noeud) in arcs_a_eviter): return None

                        # Vérifier si l'obstacle a été contourné avec succès
                        if ((y, noeud_depart[1] + obstacle[1]) not in t.get_obstacles()):
                            return creer_simulation(deepcopy(sim), cout, (y, noeud_depart[1]), noeud_arrivee, deepcopy(obstacle), None, deepcopy(arcs_a_eviter))
                    else:
                        # Créer deux simulations horizontales
                        sim1 = creer_simulation(deepcopy(sim), cout, (y + 1, noeud_depart[1]), noeud_arrivee, (0, -1), (1, 0), deepcopy(arcs_a_eviter))
                        sim2 = creer_simulation(deepcopy(sim), cout, (y + 1, noeud_depart[1]), noeud_arrivee, (0, 1), (1, 0), deepcopy(arcs_a_eviter))
                        
                        if (sim1 != None and sim2 != None):
                            if (type(sim1) == list and type(sim2) == list): return sim1 + sim2
                            elif (type(sim1) == list and type(sim2) == dict): return sim1 + [sim2]
                            elif (type(sim1) == dict and type(sim2) == list): return [sim1] + sim2
                            elif (type(sim1) == dict and type(sim2) == dict): return [sim1, sim2]
                        elif (sim1 != None): return sim1
                        elif (sim2 != None): return sim2
                        else: return None
                        
                # Le bord supérieur est atteint, invalider le chemin
                return None
            elif (direction[0] == 1):
                for y in range(noeud_depart[0] + 1, len(t.cases)):
                    # Vérifier si un obstacle est présent
                    if ((y, noeud_depart[1]) not in t.get_obstacles()):
                        # Vérifier si un noeud est déjà présent, sinon le créer
                        if (y, noeud_depart[1]) not in sim['noeuds'].values():
                            id_noeud = len(sim['noeuds'])
                            sim['noeuds'][id_noeud] = (y, noeud_depart[1])
                            sim['cout'] += 1
                            
                            # Vérifier le coût du chemin
                            if (sim['cout'] > cout): return None
                        else: id_noeud = [id_noeud for id_noeud, coord in sim['noeuds'].items() if coord == (y, noeud_depart[1])][0]
                        
                        # Vérifier si un arc est déjà présent, sinon le créer
                        id_noeud_precedent = [id_noeud for id_noeud, coord in sim['noeuds'].items() if coord == (y - 1, noeud_depart[1])][0]
                        if (((id_noeud_precedent, id_noeud) not in sim['arcs']) and ((id_noeud, id_noeud_precedent) not in sim['arcs'])):
                            sim['arcs'].append((id_noeud_precedent, id_noeud))
                            arcs_a_eviter.append((id_noeud_precedent, id_noeud))
                            sim['cout'] += 1.5

                            # Vérifier le coût du chemin
                            if (sim['cout'] > cout): return None
                        # Invalider le chemin si l'arc a déjà été parcouru
                        elif ((id_noeud_precedent, id_noeud) in arcs_a_eviter): return None

                        # Vérifier si l'obstacle a été contourné avec succès
                        if ((y, noeud_depart[1] + obstacle[1]) not in t.get_obstacles()):
                            return creer_simulation(deepcopy(sim), cout, (y, noeud_depart[1]), noeud_arrivee, deepcopy(obstacle), None, deepcopy(arcs_a_eviter))
                    else:
                        # Créer deux simulations horizontales
                        sim1 = creer_simulation(deepcopy(sim), cout, (y - 1, noeud_depart[1]), noeud_arrivee, (0, -1), (-1, 0), deepcopy(arcs_a_eviter))
                        sim2 = creer_simulation(deepcopy(sim), cout, (y - 1, noeud_depart[1]), noeud_arrivee, (0, 1), (-1, 0), deepcopy(arcs_a_eviter))
                        
                        if (sim1 != None and sim2 != None):
                            if (type(sim1) == list and type(sim2) == list): return sim1 + sim2
                            elif (type(sim1) == list and type(sim2) == dict): return sim1 + [sim2]
                            elif (type(sim1) == dict and type(sim2) == list): return [sim1] + sim2
                            elif (type(sim1) == dict and type(sim2) == dict): return [sim1, sim2]
                        elif (sim1 != None): return sim1
                        elif (sim2 != None): return sim2
                        else: return None
                        
                # Le bord inférieur est atteint, invalider le chemin
                return None
            else: return None

        meilleur_chemin = {'noeuds': {}, 'arcs': [], 'cout': float('inf')}
        for clients in permutations(t.get_clients()):
            liste_clients = [t.get_entree()] + list(clients)
            simulations = [{ 'noeuds': { 0: t.get_entree() }, 'arcs': [], 'cout': 1 }]

            for i in range(len(clients)):
                for s in deepcopy(simulations):
                    sims = creer_simulation(s, meilleur_chemin['cout'], liste_clients[0], liste_clients[i+1])
                    if (type(sims) == list): simulations += sims
                    elif (type(sims) == dict): simulations.append(sims)

                # Enlever les simulations qui n'ont pas atteint leur destination et les doublons
                simulations = [sim for sim in simulations if all(client in sim['noeuds'].values() for client in clients[:i+1])]
                def valider_chemin(sim, valides = [False] * (i + 1), id_noeud = 0, arcs_passes = []):
                    # Suivre les arcs
                    for arc in [arc for arc in sim['arcs'] if arc[0] == id_noeud]:
                        # Vérifier si l'arc a déjà été parcouru
                        if (arc in arcs_passes): return valides
                
                        # Vérifier si l'arc mène à un client
                        if (sim['noeuds'][arc[1]] in clients[:i+1]):
                            valides[clients.index([coord for id, coord in sim['noeuds'].items() if id == arc[1]][0])] = True
                        
                        # Ajouter l'arc aux arcs passés
                        arcs_passes.append(arc)
                
                        # Valider le prochain noeud
                        valides = valider_chemin(sim, valides, arc[1], arcs_passes)
                    return valides
                
                j = 0
                while (j < len(simulations)):
                    # Enlever les doublons
                    if (simulations[j] in simulations[:j]):
                        simulations.pop(j)
                        continue

                    # Vérifier si le chemin est valide
                    if all(valider_chemin(simulations[j])): j += 1
                    else: simulations.pop(j)
            
            # Garder le meilleur chemin
            for sim in simulations:
                if (sim['cout'] < meilleur_chemin['cout']): meilleur_chemin = sim

        return 0, meilleur_chemin['noeuds'], meilleur_chemin['arcs']
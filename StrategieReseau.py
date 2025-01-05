from Terrain import Terrain, Case
from itertools import permutations
from copy import deepcopy
import os

class StrategieReseau:
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[int]]:
        return -1, {}, []

class StrategieReseauManuelle(StrategieReseau):
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[int]]:
        def afficher_terrain(noeuds, arcs):
            # Affichage du terrain
            print("Vue du terrain : ")
            t.afficher_avec_terrain(noeuds)

            # Affichage du réseau
            print("\nVue du réseau : ")
            t.afficher_avec_reseau(noeuds, arcs)

        predictions = {
            'add': {
                'noeud': {
                    'id': 1,
                    'prediction': (None, None),
                    'direction': (None, None),
                    'precedent': t.get_entree()
                },
                'arc': {
                    'noeud': 0
                },
            },
            'action': 'n',
            'noeud': 0,
            'arc': None
        }
        
        noeuds = { 0: t.get_entree() }
        arcs = []
        while True:
            afficher_terrain(noeuds, arcs)
            action = input("Voulez-vous ajouter un élément (a), modifier un élément (m), supprimer un élément (s) ou terminer (t) ? (a) : ")
            if action == '': action = 'a'

            if action == 't': break
            elif action == 'a':
                # Choix de l'élément à ajouter
                type_element = input(f"Voulez-vous ajouter un noeud (n) ou un arc (a), ou retourner au menu précédent (r) ? ({predictions['action']}) : ")
                if type_element == '': type_element = predictions['action']

                # Ajout d'un noeud
                if type_element == 'n':
                    # Prédiction du prochain ajout
                    predictions['action'] = 'n'
                    prediction = predictions['add']['noeud']

                    # Obtenir l'ID du nouveau noeud
                    while True:
                        user_input = input(f"Entrez l'ID du noeud ({prediction['id']}) : " if prediction['id'] else "Entrez l'ID du noeud : ")
                        if (user_input == 'r'): break
                        id_noeud = int(user_input) if user_input else (prediction['id'] if prediction['id'] != None else -1)
                        
                        if id_noeud in noeuds: print("Cet ID de noeud existe déjà. Veuillez en entrer un autre.")
                        else: break
                    
                    # Obtenir les coordonnées du nouveau noeud
                    if (user_input == 'r'): continue
                    while True:
                        # x input
                        while True:
                            user_input = input(f"- Entrez la coordonnée x du noeud ({prediction['prediction'][1]}) : " if prediction['prediction'][1] else f"- Entrez la coordonnée x du noeud (précedemment {prediction['precedent'][1]}) : ")
                            if (user_input == 'r'): break
                            x = int(user_input) if user_input else (prediction['prediction'][1] if prediction['prediction'][1] != None else (prediction['precedent'][1] if prediction['precedent'][1] != None else -1))
                            
                            if x < 0 or x >= len(t.cases[0]): print("La coordonnée x doit être comprise entre 0 et la largeur du terrain.")
                            else: break
                        
                        # y input
                        if (user_input == 'r'): break
                        while True:
                            user_input = input(f"- Entrez la coordonnée y du noeud ({prediction['prediction'][0]}) : " if prediction['prediction'][0] else f"- Entrez la coordonnée y du noeud (précédemment {prediction['precedent'][0]}) : ")
                            if (user_input == 'r'): break
                            y = int(user_input) if user_input else (prediction['prediction'][0] if prediction['prediction'][0] != None else (prediction['precedent'][0] if prediction['precedent'][0] != None else -1))
                            
                            if y < 0 or y >= len(t.cases): print("La coordonnée y doit être comprise entre 0 et la hauteur du terrain.")
                            else: break

                        if (user_input == 'r'): break

                        if (y, x) in noeuds.values(): print("Un noeud existe déjà à ces coordonnées. Veuillez en entrer d'autres.")
                        else:
                            if (prediction['prediction'] == (None, None)):
                                # Prédiction de la direction
                                if (prediction['precedent'][0] == y-1 and prediction['precedent'][1] == x): prediction['direction'] = (1, 0)
                                elif (prediction['precedent'][0] == y+1 and prediction['precedent'][1] == x): prediction['direction'] = (-1, 0)
                                elif (prediction['precedent'][0] == y and prediction['precedent'][1] == x-1): prediction['direction'] = (0, 1)
                                elif (prediction['precedent'][0] == y and prediction['precedent'][1] == x+1): prediction['direction'] = (0, -1)
                                else: prediction['direction'] = (None, None)
                                
                                prediction['prediction'] = (y + prediction['direction'][0], x + prediction['direction'][1]) if prediction['direction'] != (None, None) else (None, None)
                            else:
                                # Vérifier si la direction a changé
                                if (y == prediction['prediction'][0] and x == prediction['prediction'][1]):
                                    # Prédiction de la direction
                                    if (prediction['precedent'][0] == y-1 and prediction['precedent'][1] == x): prediction['direction'] = (1, 0)
                                    elif (prediction['precedent'][0] == y+1 and prediction['precedent'][1] == x): prediction['direction'] = (-1, 0)
                                    elif (prediction['precedent'][0] == y and prediction['precedent'][1] == x-1): prediction['direction'] = (0, 1)
                                    elif (prediction['precedent'][0] == y and prediction['precedent'][1] == x+1): prediction['direction'] = (0, -1)
                                    else: prediction['direction'] = (None, None)

                                    prediction['prediction'] = (y + prediction['direction'][0], x + prediction['direction'][1]) if prediction['direction'] != (None, None) else (None, None)
                                else:
                                    prediction['direction'] = (None, None)
                                    prediction['prediction'] = (None, None)

                            prediction['precedent'] = (y, x)
                            # Prédiction de l'ID
                            if id_noeud + 1 not in noeuds: prediction['id'] = id_noeud + 1
                            else: prediction['id'] = None

                            # Prédiction de l'arc
                            predictions['add']['arc']['noeud'] = id_noeud
                            predictions['noeud'] = id_noeud

                            break
                    
                    if (user_input == 'r'): continue
                    noeuds[id_noeud] = (y, x)
                # Ajout d'un arc
                elif type_element == 'a':
                    # Prédiction du prochain ajout
                    predictions['action'] = 'a'
                    prediction = predictions['add']['arc']

                    while True:
                        # Obtenir l'ID du noeud de départ
                        while True:
                            user_input = input(f"Entrez l'ID du noeud de départ ({prediction['noeud']}) : " if prediction['noeud'] else "Entrez l'ID du noeud de départ : ")
                            if (user_input == 'r'): break
                            noeud_depart = int(user_input) if user_input else (prediction['noeud'] if prediction['noeud'] != None else -1)

                            # Vérifier si l'ID du noeud de départ existe
                            if noeud_depart not in noeuds: print("Cet ID de noeud n'existe pas. Veuillez en entrer un autre.")

                            # Vérifier s'il y a un noeud non connecté à ce noeud, et si oui prédire le premier noeud non connecté
                            noeud = noeuds[noeud_depart]
                            voisins = []
                            # Regarder la case en bas
                            if ((noeud[0] != len(t.cases) - 1) and (noeud[0] + 1, noeud[1]) in noeuds.values()):
                                id_noeud = [id for id in noeuds if noeuds[id] == (noeud[0] + 1, noeud[1])][0]
                                if (id_noeud, noeud_depart) not in arcs and (noeud_depart, id_noeud) not in arcs:
                                    voisins.append(id_noeud)
                            # Regarder la case en haut
                            if ((noeud[0] != 0) and (noeud[0] - 1, noeud[1]) in noeuds.values()):
                                id_noeud = [id for id in noeuds if noeuds[id] == (noeud[0] - 1, noeud[1])][0]
                                if (id_noeud, noeud_depart) not in arcs and (noeud_depart, id_noeud) not in arcs:
                                    voisins.append(id_noeud)
                            # Regarder la case à gauche
                            if ((noeud[1] != 0) and (noeud[0], noeud[1] - 1) in noeuds.values()):
                                id_noeud = [id for id in noeuds if noeuds[id] == (noeud[0], noeud[1] - 1)][0]
                                if (id_noeud, noeud_depart) not in arcs and (noeud_depart, id_noeud) not in arcs:
                                    voisins.append(id_noeud)
                            # Regarder la case à droite
                            if ((noeud[1] != len(t.cases[0]) - 1) and (noeud[0], noeud[1] + 1) in noeuds.values()):
                                id_noeud = [id for id in noeuds if noeuds[id] == (noeud[0], noeud[1] + 1)][0]
                                if (id_noeud, noeud_depart) not in arcs and (noeud_depart, id_noeud) not in arcs:
                                    voisins.append(id_noeud)
                            
                            if voisins:
                                prediction['noeud-arrivee'] = min(voisins)
                                break
                            # Aucun noeud n'est connecté à ce noeud
                            else: print("Aucun noeud à connecter aux alentours. Veuillez en entrer un autre.")
                        
                        # Obtenir l'ID du noeud d'arrivée
                        if (user_input == 'r'): break
                        while True:
                            user_input = input(f"Entrez l'ID du noeud d'arrivée ({prediction['noeud-arrivee']}) : ")
                            if (user_input == 'r'): break
                            noeud_arrivee = int(user_input) if user_input else (prediction['noeud-arrivee'] if prediction['noeud-arrivee'] != None else -1)

                            # Vérifier si l'ID du noeud d'arrivée existe
                            if noeud_arrivee not in noeuds: print("Cet ID de noeud n'existe pas. Veuillez en entrer un autre.")
                            else: break

                        # Vérifier si l'arc existe déjà
                        if (user_input == 'r'): break
                        if (noeud_depart, noeud_arrivee) in arcs or (noeud_arrivee, noeud_depart) in arcs: print("Cet arc existe déjà. Veuillez en entrer un autre.")
                        else:
                            prediction['noeud'] = noeud_arrivee
                            break
                    
                    if (user_input == 'r'): continue

                    arc = (noeud_depart, noeud_arrivee)
                    arcs.append(arc)
                    predictions['arc'] = arc
                # Retourner au menu principal
                elif type_element != 'r': print("Action non reconnue. Veuillez entrer 'n', 'a' ou 't'.")
            elif action == 'm':
                type_element = input(f"Voulez-vous modifier un noeud (n) ou un arc (a), ou retourner (r) ? ({predictions['action']}) : ")
                if (type_element == ''): type_element = predictions['action']

                if type_element == 'n':
                    # Chercher le noeud à modifier
                    while True:
                        # Obtenir l'ID du noeud à modifier
                        user_input = input(f"Entrez l'ID du noeud à modifier ({predictions['noeud']}) : " if predictions['noeud'] else "Entrez l'ID du noeud à modifier : ")
                        if (user_input == 'r'): break
                        id_noeud = int(user_input) if user_input else (predictions['noeud'] if predictions['noeud'] != None else -1)

                        # Vérifier si l'ID du noeud existe
                        if id_noeud not in noeuds: print("Cet ID de noeud n'existe pas. Veuillez en entrer un autre.")
                        else: break
                    
                    if (user_input == 'r'): continue
                    # Obtenir les nouvelles coordonnées du noeud
                    while True:
                        # x input
                        while True:
                            user_input = input(f"- Entrez la nouvelle coordonnée x du noeud ({noeuds[id_noeud][1]}) : ")
                            if (user_input == 'r'): break
                            x = int(user_input) if user_input else (noeuds[id_noeud][1] if noeuds[id_noeud][1] != None else -1)
                            
                            if x < 0 or x >= len(t.cases[0]): print("La coordonnée x doit être comprise entre 0 et la largeur du terrain.")
                            else: break
                        
                        if (user_input == 'r'): break
                        # y input
                        while True:
                            user_input = input(f"- Entrez la nouvelle coordonnée y du noeud ({noeuds[id_noeud][0]}) : ")
                            if (user_input == 'r'): break
                            y = int(user_input) if user_input else (noeuds[id_noeud][0] if noeuds[id_noeud][0] != None else -1)
                            
                            if y < 0 or y >= len(t.cases): print("La coordonnée y doit être comprise entre 0 et la hauteur du terrain.")
                            else: break
                        
                        if (user_input == 'r'): break
                        # Vérifier si un noeud existe déjà à ces coordonnées
                        if (y, x) in noeuds.values(): print("Un noeud existe déjà à ces coordonnées. Veuillez en entrer d'autres.")
                        else: break
                    
                    if (user_input == 'r'): continue
                    
                    # Modifier le noeud dans la liste
                    noeuds[id_noeud] = (y, x)
                elif type_element == 'a':
                    # Chercher l'arc à modifier
                    print("Identification de l'arc à modifier :")
                    while True:
                        # Obtenir l'ID du noeud de départ
                        while True:
                            user_input = input(f"- Entrez l'ID du noeud de départ ({predictions['arc'][0]}) : " if predictions['arc'] != None else "- Entrez l'ID du noeud de départ : ")
                            if (user_input == 'r'): break
                            noeud_depart = int(user_input) if user_input else (predictions['arc'][0] if predictions['arc'] != None else -1)

                            # Vérifier si l'ID du noeud de départ existe
                            if noeud_depart not in noeuds: print("- Cet ID de noeud n'existe pas. Veuillez en entrer un autre.")
                            else:
                                # Vérifier si l'ID du noeud de départ est correct
                                if noeud_depart not in [arc[0] for arc in arcs]: print("Cet ID de noeud n'est pas un noeud de départ d'un arc. Veuillez en entrer un autre.")
                                else: break
                        
                        if (user_input == 'r'): break
                        # Obtenir l'ID du noeud d'arrivée
                        while True:
                            user_input = input(f"- Entrez l'ID du noeud d'arrivée ({predictions['arc'][1]}) : " if predictions['arc'] != None else "- Entrez l'ID du noeud d'arrivée : ")
                            if (user_input == 'r'): break
                            noeud_arrivee = int(user_input) if user_input else (predictions['arc'][1] if predictions['arc'] != None else -1)

                            # Vérifier si l'ID du noeud d'arrivée existe
                            if noeud_arrivee not in noeuds: print("Cet ID de noeud n'existe pas. Veuillez en entrer un autre.")
                            else: break

                            # Vérifier si l'ID du noeud d'arrivée est correct
                            if noeud_arrivee not in [arc[1] for arc in arcs]: print("Cet ID de noeud n'est pas un noeud d'arrivée d'un arc. Veuillez en entrer un autre.")
                            else: break
                        
                        if (user_input == 'r'): break
                        # Vérifier si l'arc existe
                        if (noeud_depart, noeud_arrivee) not in arcs: print("Cet arc n'existe pas. Veuillez en entrer un autre.")
                        else: break
                    if (user_input == 'r'): continue

                    # Modifier l'arc
                    arc = (noeud_depart, noeud_arrivee)
                    id_arc = [i for i, a in enumerate(arcs) if a == arc][0]

                    print("Modification de l'arc :")
                    while True:
                        # Obtenir l'ID du noeud de départ
                        while True:
                            user_input = input(f"- Entrez l'ID du noeud de départ ({noeud_arrivee}) : ")
                            if (user_input == 'r'): break
                            new_noeud_depart = int(user_input) if user_input else noeud_arrivee

                            # Vérifier si l'ID du noeud de départ existe
                            if new_noeud_depart not in noeuds: print("- Cet ID de noeud n'existe pas. Veuillez en entrer un autre.")
                            else: break
                        
                        if (user_input == 'r'): break
                        # Obtenir l'ID du noeud d'arrivée
                        while True:
                            user_input = input(f"- Entrez l'ID du noeud d'arrivée ({noeud_depart}) : ")
                            if (user_input == 'r'): break
                            new_noeud_arrivee = int(user_input) if user_input else noeud_depart

                            # Vérifier si l'ID du noeud d'arrivée existe
                            if new_noeud_arrivee not in noeuds: print("Cet ID de noeud n'existe pas. Veuillez en entrer un autre.")
                            else: break

                        if (user_input == 'r'): break
                        # Vérifier si l'arc existe déjà
                        if ((new_noeud_depart, noeud_arrivee) in arcs or (new_noeud_arrivee, new_noeud_depart) in arcs) and not (arc == (new_noeud_arrivee, new_noeud_depart)) : print("Cet arc existe déjà. Veuillez en entrer un autre.")
                        else: break
                    
                    if (user_input == 'r'): continue

                    # Modifier l'arc dans la liste
                    arcs[id_arc] = (new_noeud_depart, new_noeud_arrivee)

                    # Prédiction de l'arc
                    predictions['arc'] = arcs[id_arc]
                elif type_element != 'r': print("Action non reconnue. Veuillez entrer 'n', 'a' ou 't'.")
            elif action == 's':
                type_element = input(f"Voulez-vous supprimer un noeud (n) ou un arc (a), ou retourner (r) ? ({predictions['action']}) ")
                if (type_element == ''): type_element = predictions['action']

                if type_element == 'n':
                    while True:
                        # Obtenir l'ID du noeud à supprimer
                        user_input = input(f"- Entrez l'ID du noeud à supprimer ({predictions['noeud']}) : " if predictions['noeud'] != None else "- Entrez l'ID du noeud à supprimer : ")
                        if (user_input == 'r'): break
                        id_noeud = int(user_input) if user_input else (predictions['noeud'] if predictions['noeud'] != None else -1)

                        # Vérifier si l'ID du noeud existe
                        if id_noeud not in noeuds: print("Cet ID de noeud n'existe pas. Veuillez en entrer un autre.")
                        else: break
                    
                    if (user_input == 'r'): continue
                    
                    # Supprimer le noeud de la liste
                    del noeuds[id_noeud]
                    # Supprimer les arcs liés au noeud
                    arcs = [arc for arc in arcs if arc[0] != id_noeud and arc[1] != id_noeud]
                    # Enlever la prédiction du noeud
                    predictions['noeud'] = None
                    # Enlever la prédiction de l'arc si l'arc prédit le noeud supprimé
                    if predictions['arc'] and (predictions['arc'][0] == id_noeud or predictions['arc'][1] == id_noeud): predictions['arc'] = None
                elif type_element == 'a':
                    while True:
                        # Obtenir l'ID du noeud de départ
                        while True:
                            user_input = input(f"- Entrez l'ID du noeud de départ ({predictions['arc'][0]}) : " if predictions['arc'] != None else "- Entrez l'ID du noeud de départ : ")
                            if (user_input == 'r'): break
                            noeud_depart = int(user_input) if user_input else (predictions['arc'][0] if predictions['arc'] != None else -1)

                            # Vérifier si l'ID du noeud de départ existe
                            if noeud_depart not in noeuds: print("Cet ID de noeud n'existe pas. Veuillez en entrer un autre.")
                            else: break
                        
                        if (user_input == 'r'): break
                        # Obtenir l'ID du noeud d'arrivée
                        while True:
                            user_input = input(f"- Entrez l'ID du noeud d'arrivée ({predictions['arc'][1]}) : " if predictions['arc'] != None else "- Entrez l'ID du noeud d'arrivée : ")
                            if (user_input == 'r'): break
                            noeud_arrivee = int(user_input) if user_input else (predictions['arc'][1] if predictions['arc'] != None else -1)

                            # Vérifier si l'ID du noeud d'arrivée existe
                            if noeud_arrivee not in noeuds: print("Cet ID de noeud n'existe pas. Veuillez en entrer un autre.")
                            else: break
                        if (user_input == 'r'): break
                        
                        # Vérifier si l'arc existe
                        if (noeud_depart, noeud_arrivee) not in arcs: print("Cet arc n'existe pas. Veuillez en entrer un autre.")
                        else:
                            arcs = [arc for arc in arcs if arc != (noeud_depart, noeud_arrivee)]
                            
                            # Enlever la prédiction de l'arc
                            predictions['arc'] = None
                            break
                elif type_element != 'r': print("Action non reconnue. Veuillez entrer 'n', 'a' ou 't'.")
            else: print("Action non reconnue. Veuillez entrer 'a', 'm', 's' ou 't'.")
        
        # Obtenir l'ID du noeud de l'entrée
        id_entree = [id_noeud for id_noeud, coord in noeuds.items() if coord == t.get_entree()]
        id_entree = id_entree[0] if id_entree else -1
        
        return id_entree, noeuds, arcs

class StrategieReseauAuto(StrategieReseau):
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[int]]:
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
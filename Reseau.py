
from Terrain import Terrain, Case
from StrategieReseau import StrategieReseau, StrategieReseauAuto

class Reseau:
    def __init__(self):
        self.strat = StrategieReseauAuto()
        self.noeuds = {}
        self.arcs = []

        self.noeud_entree = -1

    def definir_entree(self, n: int) -> None:
        if n in self.noeuds.keys():
            self.noeud_entree = n
        else:
            self.noeud_entree = -1

    def ajouter_noeud(self, n: int, coords: tuple[int, int]):
        if n in self.noeuds:
           raise ValueError(f"Le nœud {n} existe déjà avec les coordonnées {self.noeuds[n]}.")
        if n >= 0:
           self.noeuds[n] = coords

    def ajouter_arc(self, n1: int, n2: int) -> None:
        if n1 > n2:
            tmp = n2
            n2 = n1
            n1 = tmp
        if n1 not in self.noeuds.keys() or n2 not in self.noeuds.keys():
            return
        if (n1, n2) not in self.arcs:
            self.arcs.append((n1, n2))

    def set_strategie(self, strat: StrategieReseau):
        self.strat = strat

    def valider_reseau(self) -> bool: 
    # Vérifier que le nœud d'entrée est valide
        if self.noeud_entree == -1 or self.noeud_entree not in self.noeuds:
           return False

    # Ensemble pour suivre les nœuds visités
        visités = set()

    # Fonction récursive pour parcourir les nœuds connectés
        def dfs(noeud):
            visités.add(noeud)
            for arc in self.arcs:
                if arc[0] == noeud and arc[1] not in visités:
                    dfs(arc[1])
                elif arc[1] == noeud and arc[0] not in visités:
                    dfs(arc[0])

    # Lancer la recherche à partir du nœud d'entrée
        dfs(self.noeud_entree)

    # Vérifier que tous les nœuds sont accessibles depuis le nœud d'entrée
        return len(visités) == len(self.noeuds)


    def valider_distribution(self, t: Terrain) -> bool:    
        # Récupérer les coordonnées des clients sur le terrain
        clients = set()
        for ligne in range(len(t.cases)):
            for colonne in range(len(t.cases[ligne])):
                if t.cases[ligne][colonne] == Case.CLIENT:
                    clients.add((ligne, colonne))

        # Récupérer les coordonnées des nœuds du réseau
        noeuds_coords = set(self.noeuds.values())

        # Vérifier que chaque client est couvert par au moins un nœud
        return clients.issubset(noeuds_coords)


    def configurer(self, t: Terrain):
        self.noeud_entree, self.noeuds, self.arcs  = self.strat.configurer(t)

    def afficher(self) -> None:
        print("=== Configuration du Réseau ===")
        
        # Afficher le nœud d'entrée
        if self.noeud_entree in self.noeuds:
            print(f"Noeud d'entrée : {self.noeud_entree} (Coordonnées : {self.noeuds[self.noeud_entree]})")
        else:
            print("Noeud d'entrée : Aucun")

        # Afficher tous les nœuds
        print("\nNœuds :")
        if self.noeuds:
            for noeud_id, coords in self.noeuds.items():
                print(f"  - Noeud {noeud_id} : {coords}")
        else:
            print("  Aucun nœud défini.")

        # Afficher tous les arcs
        print("\nArcs :")
        if self.arcs:
            for arc in self.arcs:
                print(f"  - Arc entre {arc[0]} et {arc[1]}")
        else:
            print("  Aucun arc défini.")

        print("================================")

    def afficher_avec_terrain(self, t: Terrain) -> None:
        for ligne, l in enumerate(t.cases):
            for colonne, c in enumerate(l):
                if (ligne, colonne) not in self.noeuds.values():
                    if c == Case.OBSTACLE:
                        print("X", end="")
                    if c == Case.CLIENT:
                        print("C", end="")
                    if c == Case.VIDE:
                        print("~", end="")
                    if c == Case.ENTREE:
                        print("E", end="")
                    else:
                        print(" ", end="")
                else:
                    if c == Case.OBSTACLE:
                        print("T", end="")
                    if c == Case.CLIENT:
                        print("C", end="")
                    if c == Case.VIDE:
                        print("+", end="")
                    if c == Case.ENTREE:
                        print("E", end="")
                    else:
                        print(" ", end="")
            print()

    def calculer_cout(self, t: Terrain) -> float:
        cout = 0
        for _ in self.arcs:
            cout += 1.5
        for n in self.noeuds.values():
            if t[n[0]][n[1]] == Case.OBSTACLE:
                cout += 2
            else:
                cout += 1
        return cout


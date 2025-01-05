from Terrain import Terrain, Case
from StrategieReseau import StrategieReseau, StrategieReseauAuto

class Reseau:
    def __init__(self):
        self.strat = StrategieReseauAuto()
        self.noeuds = {}
        self.arcs = []

        self.noeud_entree = -1

    def definir_entree(self, n: int) -> None:
        if n in self.noeuds.keys(): self.noeud_entree = n
        else: self.noeud_entree = -1

    def ajouter_noeud(self, n: int, coords: tuple[int, int]):
        if n >= 0:
            if n in self.noeuds: raise ValueError("Le noeud existe déjà sous cet identifiant")
            self.noeuds[n] = coords

    def ajouter_arc(self, n1: int, n2: int) -> None:
        if n1 > n2:
            tmp = n2
            n2 = n1
            n1 = tmp
        if n1 not in self.noeuds.keys() and n2 not in self.noeuds.keys(): raise ValueError("Les noeuds n'existent pas")
        elif n1 not in self.noeuds.keys(): raise ValueError("Le noeud n1 n'existe pas")
        elif n2 not in self.noeuds.keys(): raise ValueError("Le noeud n2 n'existe pas")
        if (n1, n2) not in self.arcs: self.arcs.append((n1, n2))

    def set_strategie(self, strat: StrategieReseau): self.strat = strat

    def valider_reseau(self) -> bool:
        # Regarder si chaque noeud a au moins un arc
        for n in self.noeuds.keys():
            if not any([arc[0] == n or arc[1] == n for arc in self.arcs]): return False

        # Regarder tous les arcs
        for arc in self.arcs:
            # Vérifier que les noeuds de l'arc existent
            if arc[0] not in self.noeuds.keys() or arc[1] not in self.noeuds.keys(): return False

            # Vérifier que les noeuds de l'arc sont différents
            if arc[0] == arc[1]: return False

            # Vérifier que les noeuds de l'arc sont voisins
            if abs(self.noeuds[arc[0]][0] - self.noeuds[arc[1]][0]) + abs(self.noeuds[arc[0]][1] - self.noeuds[arc[1]][1]) != 1: return False

        return True

    def valider_distribution(self, t: Terrain) -> bool:
        # Vérifier qu'il y a un noeud sur l'entrée
        if t.get_entree() not in self.noeuds.values(): return False

        id_noeud_entree = [id_noeud for id_noeud, coords in self.noeuds.items() if coords == t.get_entree()][0]
        clients = t.get_clients()
        id_clients = {client: index for index, client in enumerate(clients)}
        
        def verifier(id_noeud: int, valides: list[bool] = [False] * len(clients), arcs_visites: list[tuple[int, int]] = []) -> list[bool]:
            # Obtenir les arcs PARTANT du noeud
            arcs = [arc for arc in self.arcs if arc[0] == id_noeud]

            for arc in arcs:
                # Vérifier que le noeud de destination existe et que l'arc n'a pas déjà été visité
                if arc[1] not in self.noeuds.keys(): return valides
                if arc in arcs_visites: return valides

                # Vérifier si le noeud de destination est un client
                if self.noeuds[arc[1]] in clients:
                    valides[id_clients[self.noeuds[arc[1]]]] = True

                # Vérifier les noeuds suivants
                arcs_visites.append(arc)
                valides = verifier(arc[1], valides, arcs_visites)
            return valides

        return all(verifier(id_noeud_entree))

    def configurer(self, t: Terrain): self.noeud_entree, self.noeuds, self.arcs = self.strat.configurer(t)

    def afficher(self, t: Terrain) -> None:
        # Affichage du terrain
        print("Vue du terrain : ")
        t.afficher_avec_terrain(self.noeuds)

        # Affichage du réseau
        print("\nVue du réseau : ")
        t.afficher_avec_reseau(self.noeuds, self.arcs)

    def calculer_cout(self, t: Terrain) -> float:
        cout = 0
        for _ in self.arcs: cout += 1.5
        for n in self.noeuds.values():
            if t[n[0]][n[1]] == Case.OBSTACLE: cout += 2
            else: cout += 1
        return cout
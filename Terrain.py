from enum import Enum

class Case(Enum):
    VIDE = 0
    OBSTACLE = 1
    CLIENT = 2
    ENTREE = 4

class Terrain:
    def __init__(self):
        self.largeur = 0
        self.hauteur = 0
        self.cases = []
        self.fichier = ""

    def charger(self, fichier, reseau):
        self.cases.clear()
        with open(fichier, "r") as f:
            ligne_max = 0
            for ligne in f:
                ligne = list(ligne)[:-1]
                ligne_cases = []
                n = 0
                for c in ligne:
                    n += 1
                    if c == " ": ligne_cases.append(Case.OBSTACLE)
                    elif c == "C": ligne_cases.append(Case.CLIENT)
                    elif c == "~": ligne_cases.append(Case.VIDE)
                    elif c == "E": ligne_cases.append(Case.ENTREE)
                    else: ligne_cases.append(Case.OBSTACLE)
                self.cases.append(ligne_cases)
                if ligne_max < n: ligne_max = n
        for i, l in enumerate(self.cases):
            while len(l) < ligne_max:
                self.cases[i].append(Case.OBSTACLE)
        self.largeur = ligne_max
        self.hauteur = len(self.cases)

        # Effacer la liste des noeuds et des arcs
        reseau.noeuds = {0: self.get_entree()}
        reseau.arcs = []
        self.fichier = fichier.split("/")[-1].split(".")[0]

    def __getitem__(self, l):
        return self.cases[l]

    def get_clients(self) -> list[tuple[int, int]]:
        clients = []
        for i, l in enumerate(self.cases):
            for j, c in enumerate(l):
                if c == Case.CLIENT:
                    clients.append((i, j))
        return clients

    def get_entree(self) -> tuple[int, int]:
        for i, l in enumerate(self.cases):
            for j, c in enumerate(l):
                if c == Case.ENTREE:
                    return (i, j)
        return (-1, -1)
    
    def get_obstacles(self) -> list[tuple[int, int]]:
        obstacles = []
        for i, l in enumerate(self.cases):
            for j, c in enumerate(l):
                if c == Case.OBSTACLE:
                    obstacles.append((i, j))
        return obstacles

    def afficher(self):
        for l in self.cases:
            for c in l:
                if c == Case.OBSTACLE: print("X", end = "")
                if c == Case.CLIENT: print("C", end = "")
                if c == Case.VIDE: print("~", end = "")
                if c == Case.ENTREE: print("E ", end = "")
                else: print(" ", end = "")
            print()

    def afficher_avec_terrain(self, noeuds: dict[int, tuple[int, int]]) -> None:
        for ligne, l in enumerate(self.cases):
            for colonne, c in enumerate(l):
                if (ligne, colonne) in noeuds.values():
                    if c == Case.OBSTACLE: print("\033[31m", end = "T ")
                    if c == Case.CLIENT: print("\033[34m", end = "C ")
                    if c == Case.VIDE: print("\033[37m", end = "+ ")
                    if c == Case.ENTREE: print("\033[32m", end = "E ")
                else:
                    if c == Case.OBSTACLE: print("\033[31m", end = "X ")
                    if c == Case.CLIENT: print("\033[34m", end = "C ")
                    if c == Case.VIDE: print("\033[90m", end = "~ ")
                    if c == Case.ENTREE: print("\033[32m", end = "E ")

                print("\033[0m", end = "")
            print()

    def afficher_avec_reseau(self, noeuds: dict[int, tuple[int, int]], arcs: list[tuple[int, int]]):
        # Obtenir la liste des identifiants des noeuds ainsi que l'identifiant le plus grand
        positions_noeuds = {(y, x): id_noeud for id_noeud, (y, x) in noeuds.items()}
        id_max = max(noeuds.keys()) if len(noeuds) > 0 else -1

        for i, ligne in enumerate(self.cases):
            # Apparation des cases, noeuds et arcs horizontaux
            for j, case in enumerate(ligne):
                if (i, j) in positions_noeuds:
                    # Récupérer l'identifiant du noeud
                    id_noeud = positions_noeuds[(i, j)]

                    # Vérifier le voisin de gauche si le noeud n'est pas suivit par un autre noeud
                    if not((i, j - 1) in positions_noeuds) and (id_noeud < 10 and id_max > 9): print(" ", end = "")
                    
                    # Afficher le noeud, et appliquer une couleur différente selon le type de case
                    if case == Case.OBSTACLE: print("\033[31m", end = f"{id_noeud}")
                    elif case == Case.CLIENT: print("\033[34m", end = f"{id_noeud}")
                    elif case == Case.VIDE: print("\033[37m", end = f"{id_noeud}")
                    elif case == Case.ENTREE: print("\033[32m", end = f"{id_noeud}")

                    # Vérifier le voisin de droite s'il y a un noeud
                    if (i, j + 1) in positions_noeuds:
                        id_voisin = positions_noeuds[(i, j + 1)]

                        if (id_noeud, id_voisin) in arcs:
                            if (id_voisin < 10 and id_max > 9): print("-", end = "")
                            if (id_voisin < 100 and id_max > 99): print("-", end = "")
                            print("→", end = "")
                        elif (id_voisin, id_noeud) in arcs:
                            print("←", end = "")
                            if (id_voisin < 10 and id_max > 9): print("-", end = "")
                            if (id_voisin < 100 and id_max > 99): print("-", end = "")
                        else:
                            if (id_voisin < 10 and id_max > 9): print(" ", end = "")
                            print(" ", end = "")
                            if (id_voisin < 100 and id_max > 99): print(" ", end = "")
                    else:
                        print(" ", end = "")
                        if (id_noeud < 100 and id_max > 99): print(" ", end = "")
                else:
                    if id_max > 9: print(" ", end = "")

                    if case == Case.OBSTACLE: print("\033[31m", end = "T ")
                    if case == Case.CLIENT: print("\033[34m", end = "C ")
                    if case == Case.VIDE: print("\033[90m", end = "+ ")
                    if case == Case.ENTREE: print("\033[32m", end = "E ")

                    if id_max > 99: print(" ", end = "")
            print("\033[37m")

            # Apparition des arcs verticaux
            if (i < len(self.cases) - 1):
                for j, case in enumerate(ligne):
                    if id_max > 9: print(" ", end = "")

                    if (i, j) in positions_noeuds:
                        id_noeud = positions_noeuds[(i, j)]

                        # Vérifier le voisin du bas
                        if (i + 1, j) in positions_noeuds:
                            id_voisin = positions_noeuds[(i + 1, j)]

                            if (id_noeud, id_voisin) in arcs: print("↓ ", end = "")
                            elif (id_voisin, id_noeud) in arcs: print("↑ ", end = "")
                            else: print("  ", end = "")
                        else: print("  ", end = "")
                    else: print("  ", end = "")
                    if id_max > 99: print(" ", end = "")
                print()
        print()
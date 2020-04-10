import numpy as np

from enum import Enum

# from this SO question
# https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python#comment3901803_3332860
from colorama import Fore, Style

# la fonction d'insertion la plus simple possible
def insertion_cost(base):
    return 1

# la fonction de substitution la plus simple possible
def substitution_cost(base1, base2):
    return 1 if base1 != base2 else 0


class Ruler:
    
    def __init__(self, dna1, dna2):
        self.dna1 = dna1
        self.dna2 = dna2
        self.costs = np.zeros(shape=(len(dna1)+1, len(dna2)+1), dtype=np.int64)


    @property
    def distance(self):
        return self.costs[-1, -1]


    def compute(self):
        """
        Élabore itérativement le tableau des coûts 
        par un parcours en diagonale
        """
        # raccourcis
        dna1, dna2, costs = self.dna1, self.dna2, self.costs
        len1 = len(dna1)
        len2 = len(dna2)

        # le parcours en diagonale - cf ci-dessus
        for c in range(len1 + len2 + 1):
            for i in range(c + 1):
                # on déduit j de c et i
                j = c - i
                # on ne considère que ceux qui tombent dans le rectangle 
                if 0 <= i <= len1 and 0 <= j <= len2:
                    if i == 0 and j == 0:  # le coin en haut a gauche
                        costs[i][j] = 0
                    elif j == 0:           # sur un bord : insertion 
                        costs[i][j] = costs[i-1][j] + insertion_cost(dna1[i-1])
                    elif i == 0:           # l'autre bord : insertion
                        costs[i][j] = costs[i][j-1] + insertion_cost(dna2[j-1])
                    else:                  # au milieu
                        costs[i][j] = min(
                            # substitution
                            costs[i-1][j-1] + substitution_cost(dna1[i-1], dna2[j-1]),
                            # insertion
                            costs[i][j-1] + insertion_cost(dna2[j-1]),
                        # insertion
                            costs[i-1][j] + insertion_cost(dna1[i-1]))


    # un exemple de ce qu'on peut faire du tableau de coûts

    class Outliner(Enum):
        TERMINAL = 1
        WEB = 2

        def outline(self, text, same):
            """
            if same is True, this returns text unchanged
            otherwise, it returns a string that outlines the text
            depending on the outlining mode chosen
            """
            if same:
                return text
            if self == self.TERMINAL:
                return f"{Fore.RED}{text}{Style.RESET_ALL}"
            if self == self.WEB:
                return f'<span style="color:red; background-color:#ccc">{text}</span>'
            return "unknown outliner"


    def report(self, outliner=None):
        """
        À partir du tableau de coûts tels que calculé dans la première phase, on retourne
        deux chaines destinées à être affichées une au dessus de l'autre pour visualiser
        les différences dans un terminal

        Les insertions sont remplacées par le caractère =, et les substitutions sont
        affichées en rouge (on utilise les codes ANSI)
        http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#8-colors
        """

        if outliner is None:
            outliner = self.Outliner.TERMINAL

        dash = outliner.outline('=', False)

        dna1, dna2, costs = self.dna1, self.dna2, self.costs
        # on commence au coin en bas a droite
        i = len(dna1)
        j = len(dna2)
        # les résultats, mais sous forme de listes de chaines, et à l'envers
        r1 = []
        r2 = []
        ### le parcours à proprement parler
        # on ne s'arrête que quand i==0 ET j==0
        while i > 0 or j > 0:
            # la valeur courante
            c = costs[i][j]
            # si on est au bord, les formules en i-1 ou j-1 
            # ne vont pas faire ce qu'on veut, il faut traiter 
            # ces cas à part
            if i == 0:                  # bord = insertion
                r1.append(dash)
                j -= 1
                r2.append(dna2[j])
            elif j == 0:                # bord = insertion
                i -= 1
                r1.append(dna1[i])
                r2.append(dash)
            # dans le milieu du tableau on regarde de quelle direction nous vient le minimum
            elif c == costs[i-1][j-1] + substitution_cost(dna1[i-1], dna2[j-1]):  # substitution
                # s'agit-t-il d'une vraie substitution ? 
                same = dna1[i-1] == dna2[j-1]
                i -= 1
                r1.append(outliner.outline(dna1[i], same))
                j -= 1
                r2.append(outliner.outline(dna2[j], same))
            elif c == costs[i][j-1] + insertion_cost(dna2[j-1]):    # insertion
                r1.append(dash)
                j -= 1
                r2.append(dna2[j])
            elif c == costs[i-1][j] + insertion_cost(dna1[i-1]):    # insertion
                i -= 1
                r1.append(dna1[i])
                r2.append(dash)

        # à ce stade il nous reste à retourner les listes, et les transformer en chaines
        if not isinstance(r1[0], str):
            r1 = list(str(x) for x in r1)
            r2 = list(str(x) for x in r2)
        s1 = "".join(reversed(r1))
        s2 = "".join(reversed(r2))
        return s1, s2

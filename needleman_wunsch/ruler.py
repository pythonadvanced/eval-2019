import numpy as np

from enum import Enum

# from this SO question
# https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python#comment3901803_3332860
from colorama import Fore, Style, init as colorama_init

# apparently this is required on Windows
colorama_init()

# the simplest possible insertion cost function
def insertion_cost(base):
    return 1

# the simplest possible substitution function
def substitution_cost(base1, base2):
    return 1 if base1 != base2 else 0


class Ruler:
    """
    the Ruler class knows how to compute the distance between 2 DNAs, and to produce
    reports that materialize this distance in terms of the set of 
    deletions / substitutions needed to transform one into the other
    """

    def __init__(self, dna1, dna2):
        self.dna1 = dna1
        self.dna2 = dna2
        # the cost matrix has one more line and one more row
        # than the input strings lengths
        self.costs = np.zeros(shape=(len(dna1)+1, len(dna2)+1), dtype=np.int64)


    # the requirements have the distance as an attribute
    # but for us it is a method, so let define a property
    @property
    def distance(self):
        return self.costs[-1, -1]


    def compute(self):
        """
        Iteratively compute the cost matrix 
        we fill the matrix along diagonals of the form 
        i+j = c, with c ranging from 
        0                the upper left corner
        to len1 + len2   the lower right corner
        """
        # shortcuts
        dna1, dna2, costs = self.dna1, self.dna2, self.costs
        len1 = len(dna1)
        len2 = len(dna2)

        # iterating this way ensures that we have computed the 
        # (maximum of 3) predecessor values
        for c in range(len1 + len2 + 1):
            # i is bounded by c
            for i in range(c + 1):
                # then j is deduced from c and i
                j = c - i
                # clip within the cost matrix domain
                if 0 <= i <= len1 and 0 <= j <= len2:
                    if i == 0 and j == 0:  # upper left corner
                        costs[i][j] = 0
                    elif j == 0:           # on one edge, only one insertion
                        costs[i][j] = costs[i-1][j] + insertion_cost(dna1[i-1])
                    elif i == 0:           # the other edge, ditto
                        costs[i][j] = costs[i][j-1] + insertion_cost(dna2[j-1])
                    else:                  # in the middle
                        costs[i][j] = min(
                            # substitution
                            costs[i-1][j-1] + substitution_cost(dna1[i-1], dna2[j-1]),
                            # insertion
                            costs[i][j-1] + insertion_cost(dna2[j-1]),
                            # insertion
                            costs[i-1][j] + insertion_cost(dna1[i-1]))


    # note that this class serves no purpose outside of Ruler
    # so there is no need to clobber the module namespace
    # and it is better to keep it embedded in the Ruler class
    class Outliner(Enum):
        """
        when writing the test assignment, I needed to be able to produce 
        an HTML-based rendering of the reports, so this code is a little 
        more complex than what was strictly required
        """
        
        # the 2 supported kinds of output
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


    def report(self, outliner=None):
        """
        Starting from the costs matrix as elaborated by compute(), 
        this method returns tw strings that have the same lengths
        and where the longest common substrings are aligned together
        when the reports are displayed on top of each other
        
        insertions are replaced with an '=' sign, and substitutions
        are outlined in red, using ANSI codes, see
    http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#8-colors
        """

        if outliner is None:
            outliner = self.Outliner.TERMINAL

        dash = outliner.outline('=', False)

        dna1, dna2, costs = self.dna1, self.dna2, self.costs
        
        # we need to walk the matrix back from lower-right 
        # up to the (0, 0) corner, following the path that resulted in
        # the minimal distance

        # staring from the lower-right corner
        i, j = len(dna1), len(dna2)
        # results are collected as reversed lists of characters
        r1, r2 = [], []
        
        # we need to go ALL THE WAY until the (0, 0) corner
        # and NOT stop at the first edge, as that would mean
        # missing parts of the desired result
        #
        # so we need to stop when i==0 AND j==0
        while i > 0 or j > 0:       # which we could have written not(i==0 and j==0)
            # current value
            c = costs[i][j]
            # if we are on an edge 
            # we need to handle specifically the edges (i==0 or j==0)
            # since in these cases the i-1 or j-1 formulas make no sense
            if i == 0:                  # edge = insertion
                r1.append(dash)
                j -= 1
                r2.append(dna2[j])
            elif j == 0:                # edge = insertion
                i -= 1
                r1.append(dna1[i])
                r2.append(dash)
            # in the middle of the matrix, we need to see which 
            # of the 3 directions we've been coming from
            elif c == costs[i-1][j-1] + substitution_cost(dna1[i-1], dna2[j-1]):  # substitution
                # is it a true substitution (does it need to be red)
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

        # at this point we need to reverse both result lists
        # and transform then into actual strings
        s1 = "".join(reversed(r1))
        s2 = "".join(reversed(r2))
        return s1, s2

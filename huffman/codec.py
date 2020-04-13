from collections import Counter

from graphviz import Digraph

# spelling out our data structures
from typing import Dict

FrequencyDict = Dict[str, int]
CodingMap =  Dict[str, str]


class Node:
    """
    a Node instance models a node in the Huffman binary tree; 
    it can be a leaf or a binary tree
    
    that is to say, it either has a 'char' attribute, 
    *or* it has both a left and right nodes
    
    the 'counts' attribute contains the number of occurrences of all characters
    in or below this node
    """

    def __init__(self, *, char=None, left=None, right=None, counts=0):
        # either it's a leaf, or it has 2 sons
        assert (
            (left is not None and right is not None and char is None)
            or (left is None and right is None and char is not None)
            )
        
        self.char = char
        self.left = left
        self.right = right
        self.counts = counts


    def __repr__(self):
        # we don't keep the chars of the nodes below, 
        # but we can easily compute them for making repr() clearer
        return (
            f"( {repr(self.left)} ) ^ ( {repr(self.right)} )={self.counts}" if self.left
            else f"['{self.char}'={self.counts}]" 
        )


    def coding_map(self) -> CodingMap:
        """
        returns a dictionary single-character -> code 
        code being a str with 0s and 1s
        """
        map = {}
        self._coding_map('', map)
        return map


    # the internal recursive scan that computes the coding map
    def _coding_map(self, prefix, map):
        if self.char:
            map[self.char] =  prefix
        else:
            for hop, tree in ('0', self.left), ('1', self.right):
                tree._coding_map(prefix+hop, map)


class TreeBuilder:
    """
    a TreeBuilder object allows to compute a Huffman binary tree
    
    it can be created from either a text, or a precomputed frequency dictionary
    
    in the former case, a frequency dictionary is computed from the text
    """
    
    def __init__(self, text=None, frequency_dict: FrequencyDict = None):
        # give exactly one argument
        assert (text is not None) ^ (frequency_dict is not None)
        if text is not None:
            frequency_dict = Counter(text)
        self.frequency_dict = frequency_dict


    def tree(self):
        """
        returns a Node object that materializes the Huffman tree
        associated to that frequency dictionary
        """
        freq_dict = self.frequency_dict
        nodes = [Node(char=k, counts=v) for (k, v) in freq_dict.items()]
        if len(nodes) <= 1:
            raise ValueError(f'compute_tree needs at least 2 characters')
        nodes.sort(key = lambda node: node.counts)
        while len(nodes) >= 2:
            left, right, *_ = nodes
            new_node = Node(left=left, right=right, counts=left.counts+right.counts)
            nodes[0:2] = [new_node]
            nodes.sort(key = lambda node: node.counts)
        return nodes[0]
        

class Codec:
    """
    a Codec object is created from a provided Huffman tree
    it then allows to encode or decode any string
    """
    def __init__(self, tree):
        self.tree = tree
        self.map = tree.coding_map()

    def encode(self, text):
        # encoding is strightforward
        result = ""
        for char in text:
            if char not in self.map:
                raise ValueError(f"cannot encode char {char}")
            result += self.map[char]
        return result


    def decode(self, encoded):
        # reverse coding map
        decoding = {code: char for char, code in self.map.items()}
        # compute max length of a code
        # this is mainly to issue errors as early as possible
        max_len = max(len(k) for k in decoding)
        result = ""
        while encoded:
            # check if a known code can be found at this point in the code
            for size in range(1, max_len+1):
                chunk = encoded[:size]
                if chunk in decoding:
                    result += decoding[chunk]
                    encoded = encoded[size:]
                    break
            # reminder: else after for
            #  runs when no 'break' has been found in the for loop
            else:
                raise ValueError(f"cannot decode at this point: {encoded}")
        return result

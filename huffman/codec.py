from collections import Counter

from graphviz import Digraph

# clarifying our data structures
from typing import Dict

FrequencyDict = Dict[str, int]
CodingMap =  Dict[str, str]


class Node:

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
        return (
            f"( {repr(self.left)} ) ^ ( {repr(self.right)} )={self.counts}" if self.left
            else f"['{self.char}'={self.counts}]" 
        )


    def coding_map(self) -> CodingMap:
        map = {}
        self._coding_map('', map)
        return map


    def _coding_map(self, prefix, map):
        if self.char:
            map[self.char] =  prefix
        else:
            for hop, tree in ('0', self.left), ('1', self.right):
                tree._coding_map(prefix+hop, map)


class TreeBuilder:
    
    def __init__(self, text=None, frequency_dict: FrequencyDict = None):
        # give exactly one argument
        assert (text is not None) ^ (frequency_dict is not None)
        if text is not None:
            frequency_dict = Counter(text)
        self.frequency_dict = frequency_dict


    def tree(self):
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
    
    def __init__(self, tree):
        self.tree = tree
        self.map = tree.coding_map()

    def encode(self, text):
        result = ""
        for char in text:
            if char not in self.map:
                raise ValueError(f"cannot encode char {char}")
            result += self.map[char]
        return result


    def decode(self, text):
        decoding = {v: k for k, v in self.map.items()}
        max_len = max(len(k) for k in decoding)
        result = ""
        while text:
            for size in range(1, max_len+1):
                chunk = text[:size]
                if chunk in decoding:
                    result += decoding[chunk]
                    text = text[size:]
                    break
            else:
                raise ValueError(f"cannot decode text at this point: {text}")
        return result
        

# -----
# one example illustrated for free by wikipedia
# https://en.wikipedia.org/wiki/Huffman_coding#/media/File:Huffman_coding_visualisation.svg
samples = [
    ('huffman1', "a dead dad ceded a bad babe a beaded abaca bed"),
    ('huffman2', "this is an example of a huffman tree"),
]


def test(text):
    builder = TreeBuilder(text)
    tree = builder.tree()
    codec = Codec(tree)
    encoded = codec.encode(text)
    decoded = codec.decode(encoded)
    print(f"{text} -> {encoded}")
    # bonus
    print(codec.map)

    if decoded == text:
        print(f"OK - encoded={encoded}")
    else:
        print(f"KO(1) encoded={encoded}")
        print(f"KO(2) decoded={decoded}")


if __name__ == '__main__':
    for _, sample in samples:
        test(sample)

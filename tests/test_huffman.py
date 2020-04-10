import sys
import time
import json

# H.json se trouve dans le même répertoire que ce module
from pathlib import Path

from huffman.codec import TreeBuilder, Codec

json_path = Path(__file__).parent / "H.json"

with json_path.open() as json_reference:
    # references is a list of items of the form
    references = json.loads(json_reference.read())


def run(text, builder_class, codec_class):
    beg = time.time()
    builder = builder_class(text)
    binary_tree = builder.tree()

    # on passe l'arbre binaire à un encodeur/décodeur
    codec = codec_class(binary_tree)
    # qui permet d'encoder
    encoded = codec.encode(text)
    # et de décoder
    decoded = codec.decode(encoded)
    # si cette assertion est fausse il y a un gros problème avec le code
    assert text == decoded
    duration = time.time() - beg
    return encoded, decoded, duration


def check(reference):
    (text, (encoded, duration)) = reference
    rencoded, rdecoded, rduration = run(text, TreeBuilder, Codec)
#   coding is not deterministic, when some letters have the same number of appearances
#   we have tested that both implementations check text == decoded
#   and here we just check that the encoded are of a same length
    assert len(encoded) == len(rencoded)
# no requirement on performance
#    assert (duration / rduration) <= 1.5

def test_refs():
    for reference in references:
        check(reference)

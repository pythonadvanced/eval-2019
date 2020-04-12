import sys
import time
import json

# H.json se trouve dans le même répertoire que ce module
from pathlib import Path

from needleman_wunsch.ruler import Ruler

json_path = Path(__file__).parent / "NW.json"

with json_path.open() as json_reference:
    # references is a list of items of the form
    references = json.loads(json_reference.read())


def run_strings(x1, x2, ruler_class):
    ruler = ruler_class(x1, x2)
    beg = time.process_time()    
    ruler.compute()
    distance = ruler.distance
    top, bottom = ruler.report()
    duration = time.process_time() - beg
    return distance, top, bottom, duration


def check(reference):
    ((x1, x2), (distance, top, bottom, duration)) = reference

    rdistance, rtop, rbottom, rduration = run_strings(x1, x2, Ruler)
   
    assert rdistance == distance
    assert rtop == top
    assert rbottom == bottom
    # allow the student to be twice as slow as our own code
    # however do this only on attempts longer than 0.1s 
    # because otherwise measurement can be noisy and thus unreliable
    if rduration >= 0.1:
        print("checking performance")
        assert (duration / rduration) <= 2.


def test_refs():
    for reference in references:
        check(reference)

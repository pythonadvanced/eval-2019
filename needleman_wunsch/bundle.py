from ruler import Ruler

from pathlib import Path


def do_one_couple(line1, line2, index):
    """
    manage a couple of input lines, i.e. compute and display the 
    distance and reports
    """
    ruler = Ruler(line1, line2)
    ruler.compute()
    print(f"===== exemple # {index} - distance = {ruler.distance}")
    report1, report2 = ruler.report()
    print(report1)            
    print(report2)


def batch(filename):
    """
    handle one filename: parse lines, skip empty ones
    and call do_one_couple on each pair
    """
    counter = 1
    # alternate between 0 and 1
    side = 0
    # the arguments to do_one_couple
    args = [None, None]
    with Path(filename).open() as input_file:
        for line in input_file:
            line = line.strip()
            # allow empty lines as separators
            if not line:
                continue
            # fill just-read line in the right slot in args
            args[side] = line
            # alternate
            side = (side + 1) % 2
            if side == 0:
                do_one_couple(*args, counter)
                counter += 1
          

def main():
    # I chose to use argparse because it is the usual way 
    # to deal with this kind of requirements
    # it would be OK to just iterate over sys.argv[1:]
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("filenames", nargs='+')
    args = parser.parse_args()
    
    for filename in args.filenames:
        batch(filename)


main()        
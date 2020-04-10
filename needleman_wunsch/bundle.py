from ruler import Ruler

from pathlib import Path


def do_one_couple(line1, line2, index):
    ruler = Ruler(line1, line2)
    ruler.compute()
    print(f"===== exemple {index}: distance={ruler.distance}")
    report1, report2 = ruler.report()
    print(report1)            
    print(report2)


def batch(filename):
    counter = 1
    side = 0
    args = [None, None]
    with Path(filename).open() as input_file:
        for line in input_file:
            line = line.strip()
            # allow empty lines as separators
            if not line:
                continue
            args[side] = line
            side = (side + 1) % 2
            if side == 0:
                do_one_couple(*args, counter)
                counter += 1
          
            
def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("filenames", nargs='+')
    args = parser.parse_args()
    
    for filename in args.filenames:
        batch(filename)


main()        
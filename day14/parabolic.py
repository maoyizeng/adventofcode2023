import sys

def main(filename):
    # a list holding the current load count for each column
    current_beam = []

    result = 0

    with open(filename, 'r') as file:
        lines = file.readlines()

        # the load of the first line
        most_load = len(lines)
        # the real line (for '#')
        current_load = most_load

        for line in lines:
            if len(current_beam) == 0:
                # first line; initialize the load count with the column count
                current_beam = [ most_load for _ in range(len(line))]
            else:
                # the real line (for '#')
                current_load = current_load - 1

            for i in range(len(line)):
                if line[i] == 'O':
                    # it will roll to the current board; count the load, and then the current board - 1
                    result = result + current_beam[i]
                    current_beam[i] = current_beam[i] - 1
                elif line[i] == '#':
                    # it will become the board
                    current_beam[i] = current_load - 1
                elif line[i] == '\n':
                    continue
                elif line[i] == '.':
                    continue
                else:
                    print("Unrecognized char!\n")
                    sys.exit(1)
    print(result)

if __name__=='__main__':
    if len(sys.argv) != 2:
        print("Usage: parabolic.py FILENAME\n")
        sys.exit(1)
    main(sys.argv[1])

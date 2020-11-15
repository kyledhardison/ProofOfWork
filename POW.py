import argparse
import hashlib


def targetgen(difficulty, target):
    """
    Generate a target of length 256 based on POW difficulty
    """
    length = 256
    difficulty = int(difficulty)
    target_string = "0" * difficulty
    target_string += "1" * (length - difficulty)

    print("Target Generated:")
    print(target_string)
    
    # Write as int for convenience
    with open(target, "w") as f:
        f.write(str(int(target_string, 2)))


def solutiongen(target_file, input_file, solution_file):
    with open(target_file, "r") as f:
        target = int(f.read())

    with open(input_file, "r") as f:
        input = f.read()

    h = hashlib.sha256()
    h.update(bytearray(input, "UTF-8"))

    s = 0
    while True:
        j = h.copy()
        j.update(bytearray(s))
        hash = int(j.hexdigest(), 16)
        if hash <= target:
            print("Solution: " + str(s))
            with open(solution_file, "w") as f:
                f.write(str(s))
            break
        s += 1
        

def verifysolution(input_file, solution_file, target_file):
    with open(input_file, "r") as f:
        input = f.read()

    with open(solution_file, "r") as f:
        solution = int(f.read())
    
    with open(target_file, "r") as f:
        target = int(f.read())
    
    h = hashlib.sha256()
    h.update(bytearray(input, "UTF-8"))
    h.update(bytearray(solution))
    hash = int(h.hexdigest(), 16)
    print(hash)
    print(target)
    print(solution)
    if hash <= target:
        print("Valid solution")
        print(1)
    else:
        print("Invalid solution")
        print(0)

# Main function
if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser("Generate a POW target or solution, or verify a solution")

    subparsers = parser.add_subparsers(help="Types of operations", dest="command")

    target_parser = subparsers.add_parser("targetgen")
    solution_parser = subparsers.add_parser("solutiongen")
    verify_parser = subparsers.add_parser("verify")

    target_parser.add_argument("difficulty", help="POW Difficulty")
    target_parser.add_argument("target", help="target file")

    solution_parser.add_argument("target", help="Target file")
    solution_parser.add_argument("input", help="Input file")
    solution_parser.add_argument("solution", help="Solution file")

    verify_parser.add_argument("input", help="Input file")
    verify_parser.add_argument("solution", help="Solution file")
    verify_parser.add_argument("target", help="Target file")


    args = parser.parse_args()

    # Run the chosen function based on passed arguments
    if (args.command == "targetgen"):
        targetgen(args.difficulty, args.target)
    elif (args.command == "solutiongen"):
        solutiongen(args.target, args.input, args.solution)
    elif (args.command == "verify"):
        verifysolution(args.input, args.solution, args.target)


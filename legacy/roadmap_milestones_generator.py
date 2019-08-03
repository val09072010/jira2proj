import sys

REQS_SRC = "reqs.txt"
MILESTONES_SRC = "milestones.txt"


def main():
    # 1 get milestones' list
    with open(MILESTONES_SRC) as f:
        milestones = f.read()
    if not milestones:
        sys.exit(-1)

    # 2 get reqs number
    with open(REQS_SRC) as f:
        i = 1
        for req in f.readlines():
            # 3 generate plan
            print(milestones.format(req.strip(), i))
            i += 1


if __name__ == "__main__":
    main()
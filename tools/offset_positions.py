import re


def main():
    waypoint_regex = re.compile(r"<\s*(\d+)\s*,\s*(\d+)\s*>")

    result = []
    for position in input("Positions: ").split(" "):
        if matches := waypoint_regex.match(position):
            x, y = int(matches.group(1)), int(matches.group(2))
            x += 32
            y += 32
            result.append(f"<{x},{y}>")
    print(' '.join(result))


if __name__ == '__main__':
    main()

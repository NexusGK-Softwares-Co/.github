from urllib.request import urlopen
import re

def decode_google_doc():
    url = "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"

    html = urlopen(url).read().decode("utf-8")

    # remove HTML tags
    text = re.sub(r"<[^>]+>", " ", html)
    tokens = text.split()

    points = []

    for i in range(len(tokens) - 2):
        a, b, c = tokens[i], tokens[i+1], tokens[i+2]

        # format: x y char OR x char y
        if a.isdigit() and c.isdigit():
            points.append((int(a), int(c), b))
        elif a.isdigit() and b.isdigit():
            points.append((int(a), int(b), c))

    if not points:
        print("No data parsed")
        return

    max_x = max(x for x, _, _ in points)
    max_y = max(y for _, y, _ in points)

    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for x, y, char in points:
        grid[y][x] = char

    for row in grid:
        print("".join(row))


# RUN
decode_google_doc()
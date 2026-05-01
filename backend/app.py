from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

GRID = 4
world = []
visited = []
agent = (0, 0)
KB = []
steps = 0
safe = set()
danger = set()


def init_world(n):
    global GRID, world, visited, agent, KB, steps, safe, danger
    GRID = n
    world = [["" for _ in range(n)] for _ in range(n)]
    visited = [[False] * n for _ in range(n)]
    KB = []
    steps = 0
    safe = {(0, 0)}
    danger = set()

    while True:
        wx, wy = random.randint(0, n - 1), random.randint(0, n - 1)
        if (wx, wy) != (0, 0):
            world[wx][wy] = "W"
            break

    for _ in range(n):
        while True:
            x, y = random.randint(0, n - 1), random.randint(0, n - 1)
            if world[x][y] == "" and (x, y) != (0, 0):
                world[x][y] = "P"
                break

    agent = (0, 0)


def nbr(x, y):
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    return [(x + dx, y + dy) for dx, dy in dirs if 0 <= x + dx < GRID and 0 <= y + dy < GRID]


def L(sym, x, y, neg=False):
    return ("~" if neg else "") + f"{sym}_{x}_{y}"


def percept(x, y):
    b = s = False
    for nx, ny in nbr(x, y):
        if world[nx][ny] == "P":
            b = True
        if world[nx][ny] == "W":
            s = True
    return b, s


def tell(x, y, b, s):
    nbs = nbr(x, y)
    pit_lits = {L("P", nx, ny) for nx, ny in nbs}
    wmp_lits = {L("W", nx, ny) for nx, ny in nbs}

    if b:
        KB.append(pit_lits)
    else:
        for nx, ny in nbs:
            KB.append({L("P", nx, ny, True)})

    if s:
        KB.append(wmp_lits)
    else:
        for nx, ny in nbs:
            KB.append({L("W", nx, ny, True)})


def neg_lit(lit):
    return lit[1:] if lit.startswith("~") else "~" + lit


def resolve(ci, cj):
    resolvents = []
    for a in ci:
        if neg_lit(a) in cj:
            resolvent = (ci - {a}) | (cj - {neg_lit(a)})
            resolvents.append(resolvent)
    return resolvents


def resolution(kb, query):
    """Return True if KB entails query (all literals in query must hold)."""
    global steps
    clauses = [frozenset(c) for c in kb]
    # Negate each query literal and add as unit clauses
    for q in query:
        clauses.append(frozenset({neg_lit(q)}))

    seen = set(clauses)

    while True:
        new_clauses = set()
        clause_list = list(clauses)
        n = len(clause_list)
        for i in range(n):
            for j in range(i + 1, n):
                for r in resolve(clause_list[i], clause_list[j]):
                    steps += 1
                    fr = frozenset(r)
                    if len(fr) == 0:
                        return True  
                    new_clauses.add(fr)

        if new_clauses.issubset(seen):
            return False  
        for c in new_clauses:
            if c not in seen:
                seen.add(c)
                clauses.append(c)


def ask_safe(x, y):
    """Return True only if KB proves both no-pit AND no-wumpus at (x,y)."""
    no_pit = resolution(KB, [L("P", x, y, True)])
    no_wumpus = resolution(KB, [L("W", x, y, True)])
    return no_pit and no_wumpus


def move():
    global safe, danger
    x, y = agent
    candidates = []
    for nx, ny in nbr(x, y):
        if not visited[nx][ny]:
            if ask_safe(nx, ny):
                safe.add((nx, ny))
                candidates.append((nx, ny))
            else:
                danger.add((nx, ny))

    if candidates:
        return candidates[0]
    return None


@app.route("/")
def home():
    return "Wumpus AI Ready"


@app.route("/init", methods=["POST"])
def init():
    size = request.json.get("size", 4)
    init_world(size)
    return jsonify({"pos": list(agent)})


@app.route("/step")
def step_api():
    global agent
    x, y = agent

    if not visited[x][y]:
        visited[x][y] = True
        b, s = percept(x, y)
        tell(x, y, b, s)
    else:
        b, s = percept(x, y)

    m = move()
    stuck = False
    if m:
        agent = m
    else:
        stuck = True

    return jsonify({
        "pos": list(agent),
        "breeze": b,
        "stench": s,
        "visited": visited,
        "steps": steps,
        "safe": [list(c) for c in safe],
        "danger": [list(c) for c in danger],
        "stuck": stuck
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
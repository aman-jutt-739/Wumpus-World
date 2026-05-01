from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

GRID = 4
world = []
visited = []
agent = (0,0)

KB = []
steps = 0

safe = set()
danger = set()

def init_world(n):
    global GRID, world, visited, agent, KB, steps, safe, danger

    GRID = n
    world = [["" for _ in range(n)] for _ in range(n)]
    visited = [[False]*n for _ in range(n)]
    KB = []
    steps = 0
    safe = {(0,0)}
    danger = set()

    # Wumpus
    wx, wy = random.randint(0,n-1), random.randint(0,n-1)
    world[wx][wy] = "W"

    # Pits
    for _ in range(n):
        while True:
            x,y = random.randint(0,n-1), random.randint(0,n-1)
            if world[x][y]=="" and (x,y)!=(0,0):
                world[x][y]="P"
                break

    agent = (0,0)

def nbr(x,y):
    d=[(1,0),(-1,0),(0,1),(0,-1)]
    return [(x+i,y+j) for i,j in d if 0<=x+i<GRID and 0<=y+j<GRID]


def L(sym,x,y,neg=False):
    return ("~" if neg else "") + f"{sym}_{x}_{y}"

def percept(x,y):
    b=s=False
    for nx,ny in nbr(x,y):
        if world[nx][ny]=="P": b=True
        if world[nx][ny]=="W": s=True
    return b,s

def tell(x,y,b,s):
    global KB

    nbs = nbr(x,y)

    pits = {L("P",nx,ny) for nx,ny in nbs}
    wump = {L("W",nx,ny) for nx,ny in nbs}

    # Breeze rule
    if b:
        KB.append(pits)
    else:
        for n in nbs:
            KB.append({L("P",n[0],n[1],True)})

    # Stench rule
    if s:
        KB.append(wump)
    else:
        for n in nbs:
            KB.append({L("W",n[0],n[1],True)})

def neg(l): return l[1:] if l.startswith("~") else "~"+l


def resolve(ci,cj):
    out=[]
    for a in ci:
        for b in cj:
            if a==neg(b):
                out.append((ci-{a})|(cj-{b}))
    return out


def resolution(kb,query):
    global steps

    clauses = kb[:]

    for q in query:
        clauses.append({neg(q)})

    new=set()

    while True:
        n=len(clauses)

        for i in range(n):
            for j in range(i+1,n):
                for r in resolve(clauses[i],clauses[j]):
                    steps += 1
                    if len(r)==0:
                        return True
                    new.add(frozenset(r))

        old=set(frozenset(c) for c in clauses)

        if new.issubset(old):
            return False

        for c in new:
            if set(c) not in clauses:
                clauses.append(set(c))

def ask_safe(x,y):
    return resolution(KB,[L("P",x,y,True)]) and resolution(KB,[L("W",x,y,True)])

def move():
    x,y=agent

    for nx,ny in nbr(x,y):
        if not visited[nx][ny]:
            if ask_safe(nx,ny):
                return (nx,ny)
    return None

@app.route("/")
def home():
    return "Wumpus AI Ready"


@app.route("/init",methods=["POST"])
def init():
    size=request.json["size"]
    init_world(size)
    return jsonify({"pos":agent})


@app.route("/step")
def step_api():
    global agent

    x,y=agent
    visited[x][y]=True

    b,s=percept(x,y)
    tell(x,y,b,s)

    m=move()
    if m: agent=m

    return jsonify({
        "pos":agent,
        "breeze":b,
        "stench":s,
        "visited":visited,
        "steps":steps,
        "safe":list(safe),
        "danger":list(danger)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
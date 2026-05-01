# Wumpus World – Knowledge-Based AI Agent  

A Web-based Intelligent Agent Simulation that solves the classic **Wumpus World Problem** using:

- Propositional Logic
- CNF Knowledge Base
- Resolution Refutation
- Dynamic Percept Reasoning
- Real-time Web Visualization

---

# Project Overview

This project implements a **Knowledge-Based Agent (KBA)** that navigates an unknown grid environment containing hidden dangers.

The world contains:

- **Pits** (deadly)
- **Wumpus** (deadly)
- **Breeze** (indicates nearby pits)
- **Stench** (indicates nearby Wumpus)

The agent has **no prior knowledge** of the environment and must use logical reasoning to infer safe cells before moving.

---

# AI Concepts Implemented

## 1. Knowledge Base (KB)

The agent maintains a **Knowledge Base in CNF (Conjunctive Normal Form)**.

It stores logical rules such as:

```text
B(x,y) ⇔ Pit exists in adjacent cells
S(x,y) ⇔ Wumpus exists in adjacent cells

2. Resolution Refutation
Before moving into a new cell, the agent asks:
KB ⊨ ¬P(x,y) ∧ ¬W(x,y)
The inference engine performs:


Negation of the query


Clause resolution


Contradiction detection


If contradiction occurs, the queried cell is proven SAFE.

3. Inference Engine
The project contains a simple automated reasoning engine that:


Tracks inference steps


Applies logical deduction


Uses resolution refutation


Determines safe movements dynamically



Features
Environment


Dynamic grid size


Randomly generated pits


Random Wumpus placement


Hidden world map



Agent Behavior
The intelligent agent:


Starts at (0,0)


Receives percepts:


Breeze


Stench




Updates the knowledge base


Uses logic to infer safe cells


Moves only to logically safe positions



Reasoning System
Implemented using:


Propositional Logic


CNF conversion


Resolution Refutation


Rule-based deduction



Web Visualization
Grid visualization uses colors to display knowledge states:
ColorMeaning🟩 GreenSafe Cell⚫ GrayUnknown Cell🔴 RedDangerous Cell🟨 GoldAgent Position

Live Metrics Dashboard
Displays:


Total inference steps


Current percepts


Agent movement decisions


Real-time updates



Tech Stack
Backend


Python


Flask


Frontend


HTML


CSS


JavaScript


Installation & Setup
1. Clone Repository
git clone https://github.com/aman-jutt-739/Wumpus-World.git

2. Navigate to Project
cd Wumpus-World

3. Install Dependencies
pip install flask
Or:
pip install -r requirements.txt

4. Run Application
python app.py

5. Open in Browser
http://127.0.0.1:5000

How It Works
Step 1 — Initialize World


User selects grid size


Random pits and Wumpus are generated


Agent starts at (0,0)



Step 2 — Receive Percepts
The agent senses:


Breeze → nearby pit


Stench → nearby Wumpus



Step 3 — Update Knowledge Base
The KB stores logical rules in CNF format.

Step 4 — Resolution Refutation
Before movement:
Prove:¬Pit(x,y) AND ¬Wumpus(x,y)
If proven true through contradiction, the cell is safe.

Step 5 — Agent Movement
The agent moves only to cells logically inferred as safe.

Sample Interface
Grid Colors
Green  → SafeGray   → UnknownRed    → DangerGold   → Agent

Academic Concepts Covered
This project demonstrates practical implementation of:


Knowledge-Based Agents


Propositional Logic


CNF Conversion


Automated Theorem Proving


Resolution Refutation


Intelligent Decision Making


AI Search & Inference



Learning Outcomes
After completing this project, you will understand:


How intelligent agents reason logically


How CNF knowledge bases work


How resolution refutation proves facts


How AI agents infer hidden information


How logical AI systems make decisions



Author
Aman Khurram

License
This project is created for educational and academic purposes.
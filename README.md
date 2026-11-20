# automata_string_visualizer_project
# Automata Lab – DFA/NFA String Processing Visualizer

**Course:** CSET302 – Automata Theory and Computability  
**Project:** Automata Theory Simulator Development Project  
**University:** Bennett University  

**Group ID:** 1  
**Team Members:**  TANVI CHAUHAN (S24CSEU0581), SUHANI SINGH (S24CSEU0566), SAMRIDDHI VISHNOI (S24CSEU0455), ANUSHKA PALLAVI (S24CSEU0645), SUJAL KUMAR(S24CSEU0568)

## 1. Project Overview

Automata Lab is an interactive web-based simulator developed using Python and Streamlit. It allows users to define and test Deterministic Finite Automata (DFA) and Non-Deterministic Finite Automata (NFA).

The application provides a visual representation of finite automata, an editable transition table, and step-by-step execution of input strings. Users can observe how an automaton processes each input symbol, identify its active state or states, and determine whether the input string is accepted or rejected.

The project aims to make the working of DFA and NFA easier to understand through interactive simulation and visualization.

## 2. Features

- **DFA Simulation:** Processes an input string by following exactly one transition for each input symbol.
- **NFA Simulation:** Tracks multiple possible active states during string processing.
- **Automaton Configuration:** Allows users to define states, alphabet symbols, start state, and final states.
- **Editable Transition Table:** Users can modify transitions according to their automaton.
- **Automaton Visualization:** Displays the automaton as a state-transition diagram using Graphviz.
- **Input Validation:** Checks automaton definitions and identifies invalid states, symbols, duplicate transitions, and missing DFA transitions.
- **Step-by-Step Execution:** Displays the execution trace, including the current step, input symbol, active state(s), and explanation.
- **Run, Next Step and Reset:** Provides controls to execute the complete simulation, move through execution steps, and reset the simulation.
- **Acceptance and Rejection:** Displays whether the input string is accepted or rejected by the selected automaton.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Interactive web application interface |
| Pandas | Transition table creation and data handling |
| Graphviz | Automaton state-transition diagrams |

## 4. Project Structure

text
Automata-Visualizer/
│
├── automata_visualizer.py
├── requirements.txt
├── README.md
│
├── Report/
│   └── Project_Report.pdf
│
├── Screenshots/
│   ├── home.png
│   ├── dfa_output.png
│   └── nfa_output.png
│
└── TestCases/
    └── test_cases.md

**Main file:**
- automata_visualizer.py – Contains the complete application, including automaton configuration, transition table generation, validation, DFA/NFA simulation, Graphviz visualization, and Streamlit interface.

The folders for the report, screenshots, and test cases can be added as the project documentation is completed.

## 5. Prerequisites

Before running the application, make sure you have:

- Python installed.
- pip package manager.
- Graphviz installed on your system.
- A code editor or terminal to execute the application.

## 6. Installation

### Step 1: Clone the repository

```bash
git clone <>
```

### Step 2: Navigate to the project directory

```bash
cd Automata-Visualizer
```

### Step 3: Create a virtual environment (recommended)

```bash
python3 -m venv venv
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### Step 4: Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Install Graphviz

Graphviz also requires its system installation.

On macOS, using Homebrew:

```bash
brew install graphviz
```

On Windows or Linux, install Graphviz using the appropriate package manager or official installer.

## 7. How to Run

From the project directory, execute:

```bash
streamlit run automata_visualizer.py
```

Streamlit will start the application and provide a local URL in the terminal. Open that URL in your web browser to access Automata Lab.

## 8. How to Use the Simulator

1. Select the automaton type: DFA or NFA.
2. Enter the set of states and alphabet symbols.
3. Specify the start state and final states.
4. Edit the transition table according to the required automaton.
5. Observe the generated state-transition diagram.
6. Enter the input string you want to test.
7. Click **Run full simulation** to execute the complete input.
8. Use **Next step** to examine the execution one step at a time.
9. Use **Reset** to clear the current simulation.
10. Observe the execution trace and final acceptance or rejection result.

### Example 1: DFA

The default DFA uses:

- States: {q0, q1}
- Alphabet: {0, 1}
- Start state: q0
- Final state: q1

Its transitions are:

| Current State | Input | Next State |
|---|---|---|
| q0 | 0 | q0 |
| q0 | 1 | q1 |
| q1 | 0 | q0 |
| q1 | 1 | q1 |

**Example input:** 1011

**Expected result:** Accepted.

This DFA accepts strings ending in 1.

### Example 2: NFA

The default NFA uses:

- States: {p0, p1, p2}
- Alphabet: {0, 1}
- Start state: p0
- Final state: p2

Its transitions are:

| Current State | Input | Next State(s) |
|---|---|---|
| p0 | 0 | p0 |
| p0 | 1 | p0, p1 |
| p1 | 1 | p2 |
| p2 | 0 | p2 |

**Example input:** 11

**Expected result:** Accepted.

The NFA can maintain multiple active states while processing an input string.

## 9. Testing

The simulator should be tested using different input strings and automaton configurations.

Suggested test cases include:

| Test Case | Description | Expected Behavior |
|---|---|---|
| T01 | DFA input 1011 | Accepted |
| T02 | DFA input 1010 | Rejected |
| T03 | NFA input 11 | Accepted |
| T04 | Input containing a symbol outside the alphabet | Validation error |
| T05 | DFA with a missing transition | Validation error |
| T06 | Empty input string | Result based on whether the start state is final |
| T07 | NFA input with no reachable final state | Rejected |

Actual results should be recorded after running each test case.

## 10. Limitations

- The current implementation supports DFA and NFA without epsilon (ε) transitions.
- Epsilon-NFA conversion and DFA minimization are not implemented.
- The simulator focuses on interactive learning and visualization rather than large-scale automaton processing.
- DFA configurations must contain exactly one destination for every state-symbol pair.
- The NFA simulation handles multiple possible destination states.

## 11. Team Contributions

| Team Member | Contribution |
|---|---|
| TANVI CHAUHAN | DFA logic + transition-table generation |
| SUHANI SINGH | NFA logic + transition dictionary |
| SAMRIDDHI VISHNOI | Streamlit setup + simulation controls + execution trace + results |
| ANUSHKA PALLAVI | Validation + automaton configuration + editable table |
| SUJAL KUMAR | Graphviz visualization + diagram highlighting |

## 12. References

- Course material: CSET302 – Automata Theory and Computability.
- Python Documentation: https://docs.python.org/3/
- Streamlit Documentation: https://docs.streamlit.io/
- Pandas Documentation: https://pandas.pydata.org/docs/
- Graphviz Documentation: https://graphviz.org/documentation/

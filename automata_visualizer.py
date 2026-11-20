import streamlit as st
import pandas as pd
from graphviz import Digraph

st.set_page_config(page_title="Automata Lab", page_icon="🔁", layout="wide")

st.title("🔁 AUTOMATA LAB")
st.caption("Interactive DFA / NFA String Processing Visualizer")
st.write("Define a finite automaton, enter a string, and inspect its execution.")

def split_items(text):
    # Treat an empty Pandas cell as no destination.
    if pd.isna(text):
        return []
    return [x.strip() for x in str(text).split(",") if x.strip()]

def make_transitions(states, alphabet, machine):
    rows = []
    examples = {}
    if machine == "DFA":
        examples = {
            ("q0", "0"): "q0", ("q0", "1"): "q1",
            ("q1", "0"): "q0", ("q1", "1"): "q1"
        }
    else:
        examples = {
            ("p0", "0"): "p0", ("p0", "1"): "p0,p1",
            ("p1", "1"): "p2", ("p2", "0"): "p2"
        }
    for state in states:
        for symbol in alphabet:
            rows.append({
                "Current State": state,
                "Input Symbol": symbol,
                "Next State(s)": examples.get((state, symbol), "")
            })
    return pd.DataFrame(rows, columns=[
        "Current State", "Input Symbol", "Next State(s)"
    ])

def validate(machine, states, alphabet, start, finals, df):
    errors = []
    if not states: errors.append("Enter at least one state.")
    if not alphabet: errors.append("Enter at least one alphabet symbol.")
    if len(states) != len(set(states)): errors.append("State names must be unique.")
    if len(alphabet) != len(set(alphabet)): errors.append("Alphabet symbols must be unique.")
    if start not in states: errors.append("Start state must belong to the state set.")
    for f in finals:
        if f not in states: errors.append(f"Final state '{f}' is not defined.")

    seen = set()
    for _, row in df.iterrows():
        source = str(row["Current State"]).strip()
        symbol = str(row["Input Symbol"]).strip()
        dests = split_items(str(row["Next State(s)"]))
        if source not in states: errors.append(f"Unknown source state: {source}")
        if symbol not in alphabet: errors.append(f"Symbol '{symbol}' is not in the alphabet.")
        if (source, symbol) in seen: errors.append(f"Duplicate transition for {source} on {symbol}.")
        seen.add((source, symbol))
        for d in dests:
            if d not in states: errors.append(f"Unknown destination state: {d}")
        if machine == "DFA" and len(dests) > 1:
            errors.append(f"DFA transition from {source} on {symbol} has multiple destinations.")

    if machine == "DFA":
        for q in states:
            for a in alphabet:
                if (q, a) not in seen:
                    errors.append(f"Missing DFA transition: {q} on {a}.")
                else:
                    row = df[(df["Current State"].astype(str).str.strip() == q) &
                             (df["Input Symbol"].astype(str).str.strip() == a)]
                    if not row.empty and len(split_items(str(row.iloc[0]["Next State(s)"]))) != 1:
                        errors.append(f"DFA transition from {q} on {a} needs exactly one destination.")
    return list(dict.fromkeys(errors))

def transition_map(df):
    result = {}
    for _, row in df.iterrows():
        result[(str(row["Current State"]).strip(),
                str(row["Input Symbol"]).strip())] = set(
            split_items(str(row["Next State(s)"]))
        )
    return result

def run_dfa(start, finals, word, trans):
    state = start
    trace = [{"Step": 0, "Symbol": "START", "Active state(s)": state,
              "Explanation": "Begin at the start state."}]
    for i, symbol in enumerate(word, 1):
        destinations = trans.get((state, symbol), set())
        if not destinations:
            trace.append({"Step": i, "Symbol": symbol, "Active state(s)": "∅",
                          "Explanation": f"No transition from {state} on {symbol}."})
            return False, trace
        nxt = next(iter(destinations))
        trace.append({"Step": i, "Symbol": symbol, "Active state(s)": nxt,
                      "Explanation": f"Move from {state} to {nxt} on {symbol}."})
        state = nxt
    return state in finals, trace

def run_nfa(start, finals, word, trans):
    active = {start}
    trace = [{"Step": 0, "Symbol": "START",
              "Active state(s)": "{" + ", ".join(sorted(active)) + "}",
              "Explanation": "Begin with the start state active."}]
    for i, symbol in enumerate(word, 1):
        nxt = set()
        for state in active:
            nxt.update(trans.get((state, symbol), set()))
        active = nxt
        trace.append({"Step": i, "Symbol": symbol,
                      "Active state(s)": "{" + ", ".join(sorted(active)) + "}" if active else "∅",
                      "Explanation": f"Collect all destinations on input '{symbol}'."})
    return bool(active & finals), trace

def draw_graph(states, start, finals, df, highlighted=None):
    graph = Digraph()
    graph.attr(rankdir="LR")
    graph.attr("node", fontname="Arial", style="filled", fillcolor="white",
               color="#17365D")
    graph.node("__start__", label="", shape="point")
    for q in states:
        graph.node(q, shape="doublecircle" if q in finals else "circle",
                   fillcolor="#bfdbfe" if q in (highlighted or set()) else "white")
    if start in states:
        graph.edge("__start__", start)
    edges = {}
    for _, row in df.iterrows():
        source = str(row["Current State"]).strip()
        symbol = str(row["Input Symbol"]).strip()
        for dest in split_items(str(row["Next State(s)"])):
            edges.setdefault((source, dest), []).append(symbol)
    for (source, dest), symbols in edges.items():
        graph.edge(source, dest, label=", ".join(sorted(set(symbols))))
    return graph

# Sidebar: machine definition
st.sidebar.header("1. Automaton Configuration")
machine = st.sidebar.radio("Automaton type", ["DFA", "NFA"], horizontal=True)
states_text = st.sidebar.text_input(
    "States (comma-separated)", "q0,q1" if machine == "DFA" else "p0,p1,p2"
)
alphabet_text = st.sidebar.text_input("Alphabet (comma-separated)", "0,1")
start = st.sidebar.text_input("Start state", "q0" if machine == "DFA" else "p0")
finals_text = st.sidebar.text_input(
    "Final states (comma-separated)", "q1" if machine == "DFA" else "p2"
)
states, alphabet = split_items(states_text), split_items(alphabet_text)
finals = set(split_items(finals_text))
st.sidebar.caption("For NFA, separate multiple destinations with commas, e.g. p0,p1.")

# Transition table editor
left, right = st.columns([1.15, 1])
with left:
    st.subheader("2. Transition Table")
    st.caption("Edit the Next State(s) column. For NFA, use comma-separated destinations.")
    defaults = make_transitions(states, alphabet, machine)
    editor_key = f"editor_{machine}_{states_text}_{alphabet_text}"
    edited = st.data_editor(
        defaults, num_rows="dynamic", use_container_width=True,
        hide_index=True, key=editor_key
    )
with right:
    st.subheader("3. Automaton Diagram")
    try:
        st.graphviz_chart(draw_graph(states, start, finals, edited), use_container_width=True)
    except Exception as e:
        st.info(f"Diagram will appear when the automaton fields are valid. {e}")
    a, b = st.columns(2)
    a.metric("Number of states", len(states))
    b.metric("Number of final states", len(finals))

st.divider()
st.subheader("4. Test an Input String")
word = st.text_input("Input string", "1011" if machine == "DFA" else "11")
run_col, next_col, reset_col = st.columns(3)
run = run_col.button("▶ Run full simulation", type="primary", use_container_width=True)
next_step = next_col.button("⏭ Next step", use_container_width=True)
reset = reset_col.button("↺ Reset", use_container_width=True)

if "trace_result" not in st.session_state:
    st.session_state.trace_result = None
if "trace_step" not in st.session_state:
    st.session_state.trace_step = 0

if reset:
    st.session_state.trace_result = None
    st.session_state.trace_step = 0
    st.rerun()

if run or next_step:
    errors = validate(machine, states, alphabet, start, finals, edited)
    if errors:
        st.error("Please correct these issues:")
        for error in errors:
            st.write("• " + error)
        st.session_state.trace_result = None
    elif any(ch not in alphabet for ch in word):
        st.error("The input string contains a symbol that is not in the alphabet.")
        st.session_state.trace_result = None
    else:
        trans = transition_map(edited)
        accepted, trace = (run_dfa(start, finals, word, trans)
                           if machine == "DFA"
                           else run_nfa(start, finals, word, trans))
        st.session_state.trace_result = {
            "machine": machine, "word": word, "accepted": accepted, "trace": trace
        }
        if run:
            st.session_state.trace_step = len(trace) - 1
        else:
            st.session_state.trace_step = min(
                st.session_state.trace_step + 1, len(trace) - 1
            )

result = st.session_state.trace_result
if result:
    if result["machine"] != machine or result["word"] != word:
        st.info("Your machine or input has changed. Run the simulation again.")
    else:
        trace = result["trace"]
        step = min(st.session_state.trace_step, len(trace) - 1)
        st.subheader("5. Step-by-Step Execution")
        st.progress(step / max(len(trace) - 1, 1),
                    text=f"Step {step} of {len(trace) - 1}")
        trace_df = pd.DataFrame(trace[:step + 1])
        st.dataframe(trace_df, use_container_width=True, hide_index=True)
        current = trace[step]
        st.info(
            f"**Current step:** {current['Step']}  \n"
            f"**Symbol read:** {current['Symbol']}  \n"
            f"**Active state(s):** {current['Active state(s)']}  \n"
            f"**Explanation:** {current['Explanation']}"
        )
        if step == len(trace) - 1:
            if result["accepted"]:
                st.success("✓ STRING ACCEPTED")
            else:
                st.error("✗ STRING REJECTED")

        state_text = current["Active state(s)"]
        if machine == "DFA":
            highlighted = {state_text} if state_text in states else set()
        else:
            highlighted = set(state_text.strip("{}").replace(" ", "").split(",")) \
                if state_text not in ("∅", "") else set()
        st.subheader("6. Diagram at Current Step")
        st.graphviz_chart(
            draw_graph(states, start, finals, edited, highlighted),
            use_container_width=True
        )
else:
    st.info("Define the automaton, enter a string, and click Run or Next step.")

st.divider()
st.caption("Automata Lab • Educational prototype • DFA and NFA without ε-transitions")

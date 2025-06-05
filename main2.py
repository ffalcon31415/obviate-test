import random
import streamlit as st

# ─── LOAD ANY LIST FROM A TEXT FILE, CACHED ──────────────────────────────────
@st.cache_data
def load_list(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

obv_nouns  = load_list("obviate_nouns.txt")
verbs      = load_list("verbs.txt")
prox_nouns = load_list("proximate_nouns.txt")

# ─── PICK A NEW ROUND ─────────────────────────────────────────────────────────
def pick_new_round():
    # Clear old answers
    for k in ("form_left", "form_right", "left_answer", "right_answer", "submitted"):
        st.session_state.pop(k, None)

    # Choose one obviate noun, one proximate noun, one verb
    n_obv  = random.choice(obv_nouns)
    n_prox = random.choice(prox_nouns)
    v      = random.choice(verbs)

    # Randomize left/right
    if random.random() < 0.5:
        st.session_state.noun1, st.session_state.noun1_type = n_obv,  "Obviate"
        st.session_state.noun2, st.session_state.noun2_type = n_prox, "Proximate"
    else:
        st.session_state.noun1, st.session_state.noun1_type = n_prox, "Proximate"
        st.session_state.noun2, st.session_state.noun2_type = n_obv,  "Obviate"

    st.session_state.verb      = v
    st.session_state.submitted = False

def main():
    # ─── INITIALIZE SESSION STATE ─────────────────────────────────────────────────
    if "score"      not in st.session_state:
        st.session_state.score = 0
    if "milestones" not in st.session_state:
        st.session_state.milestones = []
    if "noun1"      not in st.session_state:
        pick_new_round()

    # ─── HEADER & SCORE ────────────────────────────────────────────────────────────
    st.title("Obviate Test  - Level 2")
    st.write(f"**Score:** {st.session_state.score}")

    st.write("##### Identify the nouns in the sentence below (obviate or proximate):")
    # ─── DISPLAY THE PHRASE WITH BIGGER NOUNS ─────────────────────────────────────
    col1, col2, col3 = st.columns([4, 4, 4])
    col1.markdown(f"### {st.session_state.noun1.title()}")
    col2.markdown(f"### {st.session_state.verb}")
    col3.markdown(f"### {st.session_state.noun2}.")

    # ─── QUIZ FORM: TWO RADIOS SIDE-BY-SIDE + SUBMIT ──────────────────────────────
    if not st.session_state.submitted:
        with st.form("quiz_form"):
            colA, colB = st.columns(2)
            left_choice = colA.radio(
                "First noun is:", ["Proximate","Obviate"],
                horizontal=True, key="form_left"
            )
            right_choice = colB.radio(
                "Second noun is:", ["Proximate","Obviate"],
                horizontal=True, key="form_right"
            )
            submitted = st.form_submit_button("Submit")

            if submitted:
                # store answers
                st.session_state.left_answer  = left_choice
                st.session_state.right_answer = right_choice
                st.session_state.submitted    = True

                # grade
                correct = (
                    left_choice  == st.session_state.noun1_type
                    and right_choice == st.session_state.noun2_type
                )
                st.session_state.score += 1 if correct else -1

                # balloons at new 10×
                ns = st.session_state.score
                if ns > 0 and ns % 10 == 0 and ns not in st.session_state.milestones:
                    st.session_state.milestones.append(ns)
                    st.balloons()

    # ─── FEEDBACK & NEXT BUTTON ───────────────────────────────────────────────────
    if st.session_state.submitted:
        correct = (
            st.session_state.left_answer  == st.session_state.noun1_type
            and st.session_state.right_answer == st.session_state.noun2_type
        )
        if correct:
            st.success("✅ Both correct!")
        else:
            st.error(
                f"❌ Wrong. First was **{st.session_state.noun1_type}**, "
                f"second was **{st.session_state.noun2_type}**."
            )

        st.button("Next", on_click=pick_new_round)
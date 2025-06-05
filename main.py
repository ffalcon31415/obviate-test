import random
import streamlit as st


# ─── LOAD WORDS ONCE ───────────────────────────────────────────────────────────
@st.cache_data
def load_words():
    words = []
    with open("words.txt") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                w, a = parts[0], parts[1]
                try:
                    a = int(a)
                    if 1 <= a <= 3:
                        words.append((w, a))
                except ValueError:
                    pass
    return words


# ─── SESSION‐STATE HELPERS ────────────────────────────────────────────────────
def pick_new_word():
    w, a = random.choice(load_words())
    st.session_state.word = w
    st.session_state.answer = a
    st.session_state.guess = None


def main():
    # initialize on first run
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "milestones" not in st.session_state:
        st.session_state.milestones = []
    if "word" not in st.session_state:
        pick_new_word()

    # ─── MAIN UI ──────────────────────────────────────────────────────────────────
    st.title("Obviate Test - Level 1")

    # move the score placeholder here, right under the title
    score_ph = st.empty()
    score_ph.markdown(f"**Score:** {st.session_state.score}")

    st.write(f"## {st.session_state.word}")

    # 1) The three choice‐buttons
    cols = st.columns(3)
    KEYS = ["Proximate", "Plural", "Obviate"]
    clicked = {i: cols[i].button(KEYS[i]) for i in range(3)}

    # 2) On first click, record guess, update score & placeholder, celebrate if needed
    if st.session_state.guess is None:
        for i in range(3):
            if clicked[i]:
                st.session_state.guess = i + 1

                # update score
                if st.session_state.guess == st.session_state.answer:
                    st.session_state.score += 1
                else:
                    st.session_state.score -= 1

                # update the placeholder right away
                score_ph.markdown(f"**Score:** {st.session_state.score}")

                # balloon on fresh multiples of 10
                ns = st.session_state.score
                if ns > 0 and ns % 10 == 0 and ns not in st.session_state.milestones:
                    st.session_state.milestones.append(ns)
                    st.balloons()

                break

    # 3) Feedback & Next button
    if st.session_state.guess is not None:
        if st.session_state.guess == st.session_state.answer:
            st.success("✅ Correct!")
        else:
            st.error(
                f"❌ Incorrect. You chose {KEYS[st.session_state.guess - 1]}, "
                f"but the right button was {KEYS[st.session_state.answer - 1]}."
            )

        # reset guess (and load a new word) when they hit Next
        st.button("Next", on_click=pick_new_word)

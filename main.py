import random
import streamlit as st

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

def pick_new_word():
    w, a = random.choice(load_words())
    st.session_state.word = w
    st.session_state.answer = a
    st.session_state.guess = None

# On first run, initialise
if "word" not in st.session_state:
    pick_new_word()

st.title("Obviate Test")
st.write(f"## {st.session_state.word}")

# 1) Show the three buttons and capture clicks
cols = st.columns(3)
KEY = ["Proximate", "Plural", "Obviate"]
clicked = {i: cols[i].button(KEY[i]) for i in range(3)}

# 2) If any was clicked, immediately record the guess
if st.session_state.guess is None:
    for i in range(3):
        if clicked[i]:
            st.session_state.guess = i + 1
            break

# 3) Feedback & Next
if st.session_state.guess is not None:
    if st.session_state.guess == st.session_state.answer:
        st.success("✅ Correct!")
    else:
        st.error(
            f"❌ Incorrect. You chose {KEY[st.session_state.guess]}, "
            f"but the right button was {KEY[st.session_state.answer]}."
        )

    # ← the only change: use on_click instead of an if‐wrapper
    st.button("Next", on_click=pick_new_word)
import streamlit as st

st.set_page_config(  # Alternate names: setup_page, page, layout
	layout="centered",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="expanded",  # Can be "auto", "expanded", "collapsed"
	page_title="COMO: Šibenice",  # String or None. Strings get appended with "• Streamlit". 
	page_icon=None,  # String, anything supported by st.image, or None.
)

if "guess_word" not in st.session_state:
    st.session_state.guess_word = ""

if "guess_word_set" not in st.session_state:
    st.session_state.guess_word_set=[]

if "guess_word_display" not in st.session_state:
    st.session_state.guess_word_display = ""

if "guess_word_left" not in st.session_state:
    st.session_state.guess_word_left = 0

if "ongoing_game" not in st.session_state:
    st.session_state.ongoing_game = False

with st.sidebar.form(key="update_guess_word",clear_on_submit=True):
    guess_word = st.text_input("Napiště jaké slovo chcete hádat",type = "password")
    if guess_word == "" and st.session_state.ongoing_game == False:
        st.warning("Napište slovo jaké slovo chcete hádat")
    elif guess_word != "" and st.session_state.ongoing_game == False:
        st.session_state.guess_word = guess_word
        st.session_state.guess_word_set = list(guess_word.upper())
        st.session_state.guess_word_display = ["-"] * len(guess_word)
        st.session_state.guess_word_left = len(guess_word)
    submit = st.form_submit_button(label = "Poslat slovo")
    if st.session_state.guess_word != "":
        st.success("Vložené slovo bylo přijato")
        st.session_state.ongoing_game = True

if "lives" not in st.session_state:
    st.session_state.lives = 6

if 'guess_letter' not in st.session_state:
    st.session_state.guess_letter = ""

if 'guessed_letter' not in st.session_state:
    st.session_state.guessed_letter = []

def replace_guess_letter_in_guess_word_set(guess_word_set, guess_letter, guess_word_display):
    for i in enumerate(guess_word_set):
        if guess_word_set[i[0]] == guess_letter:
            guess_word_display[i[0]] = guess_letter
            guess_word_set[i[0]] = "-"

if(st.session_state.lives > 0 and len(st.session_state.guess_word_set) > 0 and st.session_state.ongoing_game == True):
    with st.form(key = "update_guess_leter", clear_on_submit=True):
        st.session_state.guess_letter = st.text_input("Vložte hádané písmenko", max_chars=1).upper()
        if st.session_state.guess_letter != "":
            if st.session_state.guess_letter in st.session_state.guess_word_set and st.session_state.guess_letter not in st.session_state.guessed_letter:
                st.success(f"Gratuluji, hádané písmenko {st.session_state.guess_letter} je v skrytém slově")
                replace_guess_letter_in_guess_word_set(st.session_state.guess_word_set, st.session_state.guess_letter, st.session_state.guess_word_display)
                st.session_state.guessed_letter.append(st.session_state.guess_letter)
                st.session_state.guess_word_left = st.session_state.guess_word_display.count("-")
            elif st.session_state.guess_letter not in st.session_state.guess_word_set and st.session_state.guess_letter not in st.session_state.guessed_letter :
                st.warning(f"Bohužel, hádané písmenko {st.session_state.guess_letter} není v skrytém slově")
                st.session_state.guessed_letter.append(st.session_state.guess_letter)
                st.session_state.lives = st.session_state.lives - 1
            elif st.session_state.guess_letter in st.session_state.guessed_letter:
                st.write("Písmeno už bylo posláno")
        if st.session_state.guess_word_left == 0:
            st.success(f"Gratuluji, uhodl jsi slovo: {st.session_state.guess_word}")
        if st.session_state.lives == 0:
            st.warning(f"Bohužel, neuhodl jsi slovo: {st.session_state.guess_word}")
        st.write(f"Zatím uhodnutá písmena: {st.session_state.guess_word_display}")
        st.write(f"Zatím použité písmena: {st.session_state.guessed_letter}")
        st.write(f"Máte ještě {st.session_state.lives} pokusů")
        st.form_submit_button(label = "Poslat písmenko")
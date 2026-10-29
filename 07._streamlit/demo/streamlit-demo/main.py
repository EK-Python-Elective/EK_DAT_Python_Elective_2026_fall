import streamlit as st

st.title("Hello World!")
st.write("Velkommen til min første Streamlit-app.")

name = "Torben"
st.write(f"Hej, {name}!")

name  = " # Dette er en overskrift i markdown "
name


" --- "

x  = st.slider('Dette er en slider', 100, 10, 1)
x

alder = st.text_input('Hvad er din alder?')

f'## din alder er {alder}'




st.write('## Hello fra write')
st.markdown('## Hello fra markdown')
'## Hello fra tekststreng'


if st.button('Klik mig'):
    "I was cliked"

' --- '

if 'navne' not in st.session_state:
    st.session_state.navne = []

navn = st.text_input("Navn")
if st.button("Tilføj"):
    st.session_state.navne.append(navn)

st.write(st.session_state.navne)                              # viser kun det seneste navn


' --- '



col1, col2, col3, col4 = st.columns(4)

with col1:
    st.button('klik mig i col 1')

with col2:
    st.write('Hej fra col 2')

with col3:
    st.button('klik mig i col 3')

with col4:
    st.write('Hej fra col 4')









































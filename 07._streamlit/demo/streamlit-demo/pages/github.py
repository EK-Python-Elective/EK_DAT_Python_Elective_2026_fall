import httpx
import streamlit as st

st.title("GitHub-bruger")

username = st.text_input("Brugernavn", "EK-Python-Elective")

if st.button("Hent"):
    try:
        response = httpx.get(f"https://api.github.com/users/{username}", timeout=5)
        user = response.json()
        st.image(user["avatar_url"], width=120)
        st.metric("Public repos", user["public_repos"])
    
    except httpx.HTTPStatusError:
        st.error(f"Brugeren '{username}' blev ikke fundet")
    except httpx.RequestError as e:
        st.error(f"Kunne ikke kontakte API'et: {e}")

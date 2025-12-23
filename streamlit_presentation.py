import streamlit as st

#Styl stránky:
st.markdown(
    """
    <style>
        @font-face {
            font-family: 'Nunito';
            src: url('./Nunito-font/static/Nunito-Regular.ttf') format('truetype'); 
        }
        .stApp {
            background-color: Linen;  
        }
        .stMarkdown, .stTitle, .stHeader, .stSubheader, .stCode {
            font-family: 'Roboto', sans-serif; 
        }
        h1 {
            color: DarkGray; 
        }
        h2, h3 {
            color: Gray; 
        }
        .stMarkdown {
            color: Brown;  
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title="My Streamlit App", page_icon="📊")


st.title("Dopravní nehody v České republice")
st.write("""Vítejte v mém prvním projektu. 
         Pokud Vás zajímají údaje o dopravních nehodách, jste na správném místě.""")
st.write("Data o dopravních nehodách najdete zde: https://policie.gov.cz/clanek/statistika-nehodovosti.aspx")

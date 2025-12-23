import streamlit as st
from da import df_accidents_count
import plotly.express as px

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

if 'selected_year' not in st.session_state:
    st.session_state.selected_year = None
if st.session_state.selected_year is None:
    # Agregace pro roky
    df_years = df_accidents_count.groupby('Year')['Count'].sum().reset_index()
    
    fig = px.bar(df_years, x='Year', y='Count', color='Count', 
                 color_continuous_scale='Blues', title="Klikněte pro detail roku")
    selected_points = st.plotly_chart(fig, on_select="rerun")
    if selected_points and "selection" in selected_points and selected_points["selection"]["points"]:
        st.session_state.selected_year = selected_points["selection"]["points"][0]["x"]
        st.rerun()
else:
    year = st.session_state.selected_year
    st.subheader(f"Detail pro rok {year}")
    
    # Tlačítko zpět
    if st.button("← Zpět na roky"):
        st.session_state.selected_year = None
        st.rerun()
    
    # Filtrace dat pro daný rok
    df_detail = df_accidents_count[df_accidents_count['Year'] == year]
    
    fig_detail = px.bar(df_detail, x='Month', y='Count', color='Count',
                        color_continuous_scale='Reds', title=f"Měsíce v roce {year}")
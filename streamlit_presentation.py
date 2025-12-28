import streamlit as st
from da import execute_sql
import plotly.express as px
import pandas as pd
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import folium
from pyproj import Transformer
from pprint import pprint

st.set_page_config(page_title="Analýza nehod", page_icon="📊",layout='wide')


# funkce
# unifikace stylu grafů
def unify_graphs(graph):
    graph.update_xaxes(type='category')
    graph.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="brown")  
    return st.plotly_chart(graph, use_container_width=True)

# transformace dat z mapy ze sytému S-JTSK(5514) na systém WGS84(4326)
transformer = Transformer.from_crs("EPSG:5514", "EPSG:4326", always_xy=True)
@st.cache_data
def get_and_transform_data():
    query_gps = execute_sql("SELECT DISTINCT p1, d, e, k, p4a, p5a, p6, p9 FROM dopravni_nehody_cr.accidents_crash WHERE d < 0")
    if query_gps is not None and not query_gps.empty:
        val_e = query_gps['e'].values if (query_gps['e'].values < 0).all() else query_gps['e'].values * -1
        val_d = query_gps['d'].values if (query_gps['d'].values < 0).all() else query_gps['d'].values * -1

        lon, lat = transformer.transform(val_e, val_d)

        query_gps['lat'] = lat
        query_gps['lon'] = lon
        
        return query_gps[['p1', 'lat', 'lon', 'k', 'p4a', 'p6', 'p5a', 'p9']]
    return None

# Poměry v seskupených kategoriích
def ratio_in_categorii(data, groupbys, counted_cat_ratio):
    table_group = data.groupby(groupbys).size().reset_index(name='total')
    seskupení = data.groupby([groupbys, counted_cat_ratio])[counted_cat_ratio].size().reset_index(name='total_cat')
    table = pd.merge(seskupení, 
                     table_group, 
                     on=groupbys, 
                     how='left')
    table['ratio'] = table['total_cat']/table['total']*100
    return table

st.header('Analýza dopravních nehod v ČR')

if 'active_dashboard' not in st.session_state:
    st.session_state.active_dashboard = 'None'

but1, but2, but3, but4 =st.columns(4)

with but1:
    if st.button("Obecný přehled", use_container_width=True):
        st.session_state.active_dashboard = 'obecný_přehled'

with but2:
    if st.button("Kritické lokality", use_container_width=True):
        st.session_state.active_dashboard = 'kriticke_lokality'

with but3:
    if st.button("Příčiny", use_container_width=True):
        st.session_state.active_dashboard = "priciny"

with but4:
    if st.button("Okolnosti", use_container_width=True):
        st.session_state.active_dashboard = 'okolnosti'

st.divider()

if st.session_state.active_dashboard == 'None':
    st.text("""Vítejte. 
            Pokud vás zajímají informace o dopravních nehodách v ČR, jste tu správně.
            V této aplikaci se věnuji vizualizaci dat: https://policie.gov.cz/clanek/statistika-nehodovosti.aspx
            Kvůli velikosti dat se věnuji pouze posledním třem rokům.""")

elif st.session_state.active_dashboard == 'obecný_přehled':
    col1, col2, col3 = st.columns(3)
    df_but1 = execute_sql("SELECT p1, accident_year, accident_month, p13a as úmrtí, p14 as hmotná_škoda FROM dopravni_nehody_cr.accidents_in_time")
    years = sorted(df_but1['accident_year'].unique())
    if df_but1 is not None:
        with col1:
            st.title('Počet nehod')     
            st.metric(label="Celkem počet nehod", value=df_but1['p1'].nunique())

            accident_count = px.bar(df_but1.groupby('accident_year')['p1'].nunique().reset_index(),
                       x='accident_year',
                       y='p1',
                       title='Počet nehod v letech',
                       labels={'p1': 'Počet nehod', 'accident_year': 'Rok'},
                       color='p1',
                       color_continuous_scale='Reds',
                       text_auto=True)
            unify_graphs(accident_count)

            st.divider()

            selected_year = st.selectbox("Vyberte rok pro zobrazení počtu nehod:", options=['Měsíční průměr'] + list(years), key='total_count')
            if selected_year == 'Měsíční průměr':
                monthly_counts = df_but1.groupby(['accident_year', 'accident_month'])['p1'].nunique().reset_index()
                df_monthly_count = monthly_counts.groupby('accident_month')['p1'].mean().reset_index()
                title_suffix = 'průměr za všechny roky'               
            else:
                filtered_df = df_but1[df_but1['accident_year'] == selected_year]
                df_monthly_count = filtered_df.groupby('accident_month')['p1'].nunique().reset_index()
                title_suffix = f"rok {selected_year}"

            monthly_count_graph = px.bar(df_monthly_count,
                                         x='accident_month',
                                         y='p1',
                                         title=f'Počet nehod - {title_suffix}',
                                         labels={'p1': 'Počet nehod', 'accident_month': 'Měsíc'},
                                         color='p1',
                                         color_continuous_scale='Reds',
                                         text_auto='.1f')
            unify_graphs(monthly_count_graph)


        with col2:
            st.title('Úmrtnost')
            st.metric(label="Celkem počet úmrtí", value=df_but1['úmrtí'].sum())
            death_sum = px.bar(df_but1.groupby('accident_year')['úmrtí'].sum().reset_index(),
                       x='accident_year',
                       y='úmrtí',
                       title='Úmrtí v letech',
                       labels={'úmrtí': 'Počet úmrtí', 'accident_year': 'Rok'},
                       color='úmrtí',
                       color_continuous_scale='Reds',
                       text_auto=True)
            unify_graphs(death_sum)

            st.divider()

            selected_year2 = st.selectbox("Vyberte rok pro zobrazení počtu úmrtí:", options=['Měsíční průměr'] + list(years), key='deaths_filter')
            if selected_year2 == 'Měsíční průměr':
                monthly_deaths = df_but1.groupby(['accident_year', 'accident_month'])['úmrtí'].sum().reset_index()
                df_monthly_deaths = monthly_deaths.groupby('accident_month')['úmrtí'].mean().reset_index()
                title_suffix = 'průměr za všechny roky'               
            else:
                filtered_df = df_but1[df_but1['accident_year'] == selected_year2]
                df_monthly_deaths = filtered_df.groupby('accident_month')['úmrtí'].sum().reset_index()
                title_suffix = f"rok {selected_year2}"

            monthly_deaths_graph = px.bar(df_monthly_deaths,
                                         x='accident_month',
                                         y='úmrtí',
                                         title=f'Počet úmrtí - {title_suffix}',
                                         labels={'úmrtí': 'Počet úmrtí', 'accident_month': 'Měsíc'},
                                         color='úmrtí',
                                         color_continuous_scale='Reds',
                                         text_auto='.1f')
            unify_graphs(monthly_deaths_graph)

        with col3:
            st.title('Finanční škody')
            st.metric(label="Celkem finanční škody ve statisících", value=df_but1['hmotná_škoda'].sum())
            finan_loss_sum = px.bar(df_but1.groupby('accident_year')['hmotná_škoda'].sum().reset_index(),
                       x='accident_year',
                       y='hmotná_škoda',
                       title='Hmotná škoda v letech (ve statisících korunách)',
                       labels={'hmotná_škoda':'Hmnotná škoda (*100K) CZK', 'accident_year':'Rok'},
                       color='hmotná_škoda',
                       color_continuous_scale='Reds',
                       text_auto=True)
            unify_graphs(finan_loss_sum)

            st.divider()

            selected_year3 = st.selectbox("Vyberte rok pro zobrazení měsíční finanční škody:", options=['Měsíční průměr'] + list(years), key='monetary_loss_filter')
            if selected_year3 == 'Měsíční průměr':
                monthly_monetary_loss = df_but1.groupby(['accident_year', 'accident_month'])['hmotná_škoda'].sum().reset_index()
                df_monthly_monetary_loss = monthly_monetary_loss.groupby('accident_month')['hmotná_škoda'].mean().reset_index()
                title_suffix = 'průměr za všechny roky'               
            else:
                filtered_df = df_but1[df_but1['accident_year'] == selected_year2]
                df_monthly_monetary_loss = filtered_df.groupby('accident_month')['hmotná_škoda'].sum().reset_index()
                title_suffix = f"rok {selected_year3}"

            monthly_monetary_loss_graph = px.bar(df_monthly_monetary_loss,
                                         x='accident_month',
                                         y='hmotná_škoda',
                                         title=f"Hmotná škoda (*100K) CZK - {title_suffix}",
                                         labels={'hmotná_škoda': 'Hmotná škoda (*100K) CZK', 'accident_month': 'Měsíc'},
                                         color='hmotná_škoda',
                                         color_continuous_scale='Reds',
                                         text_auto='.1f')
            unify_graphs(monthly_monetary_loss_graph)
    else:
        st.error('Došlo k chybě v připojení')

elif st.session_state.active_dashboard == 'kriticke_lokality':
    st.subheader('Analýza kritických lokalit')    
    df_but2 = get_and_transform_data()
    road_types = sorted(df_but2['k'].unique())
    biggest_cat_val = df_but2.groupby('k')['p1'].nunique().max()
    col1graph, col2text = st.columns(2)
    with col1graph:
        col1_graph1 = px.bar(df_but2.groupby('k')['p1'].nunique().reset_index(),
                                x='k',
                                y='p1',
                                title='Počet nehod dle typu komunikace',
                                labels={'p1': 'Počet nehod', 'k': 'Typ komunikace'},
                                color='p1',
                                color_continuous_scale='Reds',
                                text_auto=True)
        unify_graphs(col1_graph1)
        col1_graph2 = df_but2.groupby(['k', 'p9']).size()

    with col2text:
        st.text(f"""Typy komunikací jsou vymezeny v zákoně č. 13/1997 Sb.
                Nejvice nehod se odehrává na Místních komunikacích: {biggest_cat_val}.
                Níže se můžete podívat na mapu ČR na níž je vykreslena hustota dopravních nehod.
                Dle očekávání se vetší koncentrace nehod objevuje kolem velkých měst a významných dopravních uzlů.
                Výberem komunikace ve filtru můžete intenzitu nehod sledovat na konrétním typu komunikace.""")
    st.divider()
    selected_road = st.selectbox("Vyberte typ komunikace:", options=['Všechny'] + list(road_types), key='road_type_filter')
    if df_but2 is not None and not df_but2.empty:
        m = folium.Map(location=[49.8175, 15.4730],
               min_zoom=7,
               zoom_start=7,
               tiles="cartodbpositron",
               max_bounds=True)
        #Kvůli chybným souřadnicím je třeba omezit data v heatmapě pouze na souřadnice v čr
        total_records = len(df_but2)
        MIN_LAT, MAX_LAT = 48.5, 51.1
        MIN_LON, MAX_LON = 12.0, 18.9

        df_gps_cleaned = df_but2[
            (df_but2['lat'] >= MIN_LAT) & (df_but2['lat'] <= MAX_LAT) &
            (df_but2['lon'] >= MIN_LON) & (df_but2['lon'] <= MAX_LON)
        ].copy()

        removed_records = total_records - len(df_gps_cleaned)
        removed_percentage = (removed_records / total_records) * 100

        if removed_records > 0:
            st.info(f"💡 Zobrazeno **{len(df_gps_cleaned):,}** nehod. "
                    f"Odstraněno **{removed_records}** záznamů ({removed_percentage:.2f} %) "
                    "Data byla očištěna o záznamy s chybně uvedenou lokací mimo ČR.")
            
        if selected_road == 'Všechny':
            heat_data = df_gps_cleaned[['lat', 'lon']].astype(float).values.tolist()
            HeatMap(heat_data, radius=8, blur=10).add_to(m)
            st_folium(m, width="100%", height=600)         
        else:
            filtered_df = df_gps_cleaned[df_gps_cleaned['k'] == selected_road]
            heat_data = filtered_df[['lat', 'lon']].astype(float).values.tolist()
            HeatMap(heat_data, radius=8, blur=10).add_to(m)
            st_folium(m, width="100%", height=600) 

    else:
        st.error("Nepodařilo se načíst/převést souřadnice z databáze.")



elif st.session_state.active_dashboard == 'priciny':
    st.subheader('Analýza nejběžnějších příčín')

else:
    st.subheader('Analýza externích podmínek při dopravních nehodách')


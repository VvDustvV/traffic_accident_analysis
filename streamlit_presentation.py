import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import folium
from pyproj import Transformer
import psycopg2

# funkce

st.set_page_config(
        page_title="Analýza dopravních nehod v ČR",
        layout="wide",
        page_icon="🚗"
    )

st.markdown(f"""
    <style>
    .stApp {{
        background-color: #041E2B;
    }}
    html, body, [class*="st-"] {{
        color: #E0D1D4 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    div.stButton > button {{
        background-color: #353743;
        color: #E0D1D4;            
        border-radius: 5px;
        border: 1px solid #E0D1D4;
        transition: all 0.3s;
    }}
    div.stButton > button:hover {{
        background-color: #43353E;
        color: #E0D1D4;
        border: 1px solid #3D2B1F;
    }}
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {{
        background-color: #353743 !important;
        color: #E0D1D4 !important;
        border: 1px solid #E0D1D4 !important;
    }}
    div[data-baseweb="popover"] {{
        background-color: ##550000 !important;
    }}
    </style>""", 
    unsafe_allow_html=True)
    

# Import z SQL databáze (postgre)
@st.cache_data
def execute_sql(sql_query: str):
    df_name = pd.DataFrame() 
    connection = None
    
    try:
        db_info = st.secrets["postgres"]
        connection = psycopg2.connect(
            host=db_info["host"],
            user=db_info["user"],
            password=db_info["password"],
            dbname=db_info["dbname"],
            port=db_info["port"],
            sslmode='require'
        )
        
        cursor = connection.cursor()
        cursor.execute("SET search_path TO dopravni_nehody_cr, public")
        cursor.execute(sql_query)
        data = cursor.fetchall()
        colnames = [cell[0] for cell in cursor.description]
        
        df_name = pd.DataFrame(data, columns=colnames)
        cursor.close()

    except Exception as e:
        st.error(f"Chyba databáze: {e}")
    
    finally:
        if connection is not None:
            connection.close()

    return df_name

# unifikace stylu grafů
def unify_graphs(graph):
    graph.update_xaxes(type='category')
    graph.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="brown")  
    return st.plotly_chart(graph, use_container_width=True)


# Poměry v seskupených kategoriích
def ratio_in_category(data, id_column, counted_cat_ratio):
    df_unique = data.drop_duplicates(subset=[id_column, counted_cat_ratio])
    df_grouped = df_unique.groupby(counted_cat_ratio).size().reset_index(name='Pocet_vyskytu')
    total = df_grouped['Pocet_vyskytu'].sum()
    df_grouped['total'] = total
    df_grouped['ratio'] = (df_grouped['Pocet_vyskytu']/df_grouped['total']*100).round(2)
    df_grouped = df_grouped.drop(columns=['total'])
    df_grouped['Pocet_vyskytu'] = pd.to_numeric(df_grouped['Pocet_vyskytu'])
    df_grouped = df_grouped.sort_values('ratio', ascending=False)
    return df_grouped

# Top výskyty v kategoriích (non-int sloupce)
def top_3_in_cat(table, id_column, category_column):
    df_unique = table.drop_duplicates(subset=[id_column, category_column])
    top_3 = df_unique.groupby(category_column).size().reset_index(name='Pocet_vyskytu')
    top_3 = top_3.sort_values(by='Pocet_vyskytu', ascending=False)
    return top_3.head(3).reset_index()
def top_1_in_cat(table, id_column, category_column):
    return top_3_in_cat(table, id_column, category_column).head(1).reset_index()

# Přeložený seznam jmen sloupců
def get_table_column_name(column):
    column_name = execute_sql(f"""SELECT descr FROM dopravni_nehody_cr.column_names
                              WHERE code = '{column}'""")
    return column_name.iloc[0, 0]

# Přeložený seznam jmen sloupců a jejich kategorií
def categories_translate(table, column):
    if table[column].isnull().all():
        return table
    cat_items = execute_sql(f"""SELECT id_detail, description_detail_2 FROM dopravni_nehody_cr.data_description
                                   WHERE column_code = '{column}'""")
    if cat_items is None or cat_items.empty:
        return table
    df = pd.merge(table,
                  cat_items,
                  left_on=column,
                  right_on='id_detail',
                  how='left')
    rename_column = get_table_column_name(column)
    df = df.rename(columns={'description_detail_2': rename_column})
    df = df.drop(columns=['id_detail', column])
    return df

def translate(table):
    to_translate = ['p5a',	'p6',	'p7',	'p8',	'p8a',	'p9',	'p10',
                'p11',	'p11a',	'p12',	'p13',	'p15',	'p16',	'p17',
                'p18',	'p19',	'p20',	'p21',	'p22',	'p23',	'p24',
                'p27',	'p28',	'p29',	'p29a',	'p29b',	'p30',	'p30a',
                'p30b',	'p31',	'p32',	'p33',	'p33c',	'p33d', 'p33e',
                'p33f',	'p33g',	'p35',	'p36',	'p37',	'p39',	'p44',
                'p45a',	'p45d',	'p45f',	'p47',	'p48a',	'p49',	'p50a',
                'p50b',	'p51',	'p52',	'p53',	'p55a',	'p57',	'p58',
                'p59a',	'p59b',	'p59c',	'p59e',	'p59f',	'p59g']	


    for column in to_translate:
        if column in table.column:
            table = categories_translate(table, column)
    return table

    
# Filtrování konkrétní kategorie v jednom ze sloupců, k tomu napárování dalších vlastností a zobrazení poměru/výskytu těchto vlastonstí v grafu
def category_conseq(table, filtered_value, category_col, consequences, graph_type):
    cause_conseqences = table.groupby(['p1',category_col,consequences]).size().reset_index()
    cause_conseqences = cause_conseqences.groupby([category_col,consequences])[consequences].size().reset_index(name='Pocet_vyskytu')
    filtered_cause_conseqences = cause_conseqences[cause_conseqences[category_col] == filtered_value].copy()
    filtered_cause_conseqences['total'] =  filtered_cause_conseqences['Pocet_vyskytu'].sum()
    filtered_cause_conseqences['ratio'] = (filtered_cause_conseqences['Pocet_vyskytu']/filtered_cause_conseqences['total']*100).round(2)
    filtered_cause_conseqences = filtered_cause_conseqences.drop(columns=['total'])
    filtered_cause_conseqences = filtered_cause_conseqences.sort_values('ratio', ascending=False)
    clean_label = consequences.replace('_', ' ')
    if graph_type == 'bar':
        filtered_cause_conseqences_graph = px.bar(filtered_cause_conseqences,
                                                  x=consequences,
                                                  y='Pocet_vyskytu',
                                                  color = 'Pocet_vyskytu',
                                                  color_continuous_scale='Reds',
                                                  text='Pocet_vyskytu',
                                                  title=f'{filtered_value} - {consequences}',
                                                  labels={'Pocet_vyskytu': 'Počet výskytů', consequences:clean_label})
    elif graph_type == 'pie': 
        filtered_cause_conseqences_graph = px.pie(filtered_cause_conseqences,
                                                  values='ratio',
                                                  names=consequences,
                                                  title=f'Poměr {consequences.replace("_", " ")} - {filtered_value}',
                                                  color_discrete_sequence=px.colors.sequential.Reds_r)
        filtered_cause_conseqences_graph.update_traces(marker=dict(line=dict(color='#000000', width=1)))
    unify_graphs(filtered_cause_conseqences_graph)
    return filtered_cause_conseqences_graph
### Skraté prvky

if 'active_dashboard' not in st.session_state:
    st.session_state.active_dashboard = 'None'


### STREAMLIT ###

st.header('Analýza dopravních nehod v ČR')



but1, but2, but3 =st.columns(3)

with but1:
    if st.button("Obecný přehled", use_container_width=True):
        st.session_state.active_dashboard = 'obecný_přehled'

with but2:
    if st.button("Kritické lokality", use_container_width=True):
        st.session_state.active_dashboard = 'kriticke_lokality'

with but3:
    if st.button("Příčiny", use_container_width=True):
        st.session_state.active_dashboard = "priciny"

st.divider()

if st.session_state.active_dashboard == 'None':
    current_layout = "centered" if st.session_state.active_dashboard == 'None' else "wide"

    st.set_page_config(
        page_title="O projektu",
        layout=current_layout,
        page_icon="⚙️"
    )
    

    st.header('Vítejte')
    st.subheader("""
            Pokud vás zajímají informace o dopravních nehodách v ČR, jste tu správně.
            V této aplikaci se věnuji vizualizaci dat: https://policie.gov.cz/clanek/statistika-nehodovosti.aspx
            Kvůli velikosti dat se věnuji pouze posledním třem rokům.
            """)
    st.subheader("Postup:")
    st.text("""
    1. Stažení dat z webu policie.cz z let 2023, 2024, 2025 (bez prosince) a jejich převod na formát xlsx kvůli snazšímu nahrání do databáze. 
            """)
    st.info('❗ V lednu 2026 je třeba doplnit prosincová data pro úplnost.')

    st.text("""
    2. Orientace v dokumentaci, hledání vztahů mezi tabulkami, čištění dat a explorativní analýza v Jupyter notebooku. 
            
    3. Vytvoření SQL databáze (PostgreSQL) s daty o nehodách.
            
    4. Vytvoření VIEWS (pohledů), které pomohou při vizualizaci zajímavých dat.

    5. Definování analytických otázek: 
            Jaký je trend četnosti dopravních nehod za poslední tři roky?👌
            V jakém měsíci je průměrně nejvíce nehod?👌
            Kolik životů vyhaslo na našich silnicích v posledních třech letech👌
            Jaký je trend úmrtnosti na našich silnicích?👌
            Jaký je nejkrizovější měsíc, co se průměrného počtu nehod týče?👌
            Co je nejčastější příčinou dopravní nehody?👌
            V jak velkém podílu dopravních nehod je v krvi viníka přítomen alkohol nebo drogy? ⚙️
            Jaký podíl chodců, kteří se stali účastníky nehody, byl vybaven reflexními prvky?👌
            Jaké je nejčastější pohlaví chodce, který se stal účastníkem dopravní nehody?👌
            Jaké je nejčastější pohlaví řidiče, který se stal účastníkem dopravní nehody? ⚙️ 
            Jaké jsou nejčastější okolnosti dopravní nehody (počasí/stav vozovky)? ⚙️
            Na jakém typu komunikace se nehody stávají nejčastěji?👌
            Jaké dny v týdnu jsou na silnicích nejrizikovější? ⚙️
            Co lze považovat za kritickou hodinu v silničním provozu? ⚙️      
    
    6. Rozvržení Streamlitu:
            - Rozdělení dashboardů na tři sekce pomocí navigace přes tlačítka.
            - Výběr knihovny pro zobrazení heatmapy intenzity dopravních nehod.
    
    7. Převodník souřadnic (S-JTSK na WGS84) pro účely zobrazení mapy.
    
    8. Implementace funkcí pro dekódování číselných hodnot na srozumitelné kategorie.
    
    9. Vizualizace výsledků a finalizace dashboardu.
    """)
    st.info('❗Body postupu nejsou seřazeny 100% chronologicky. Mnoho bodu jsem zpracovávala současně, nebo jsem mezi nimi přecházela.')
    st.divider()
    st.info('❌ Mezi některé problémy se kterými jsem se setkala patří neúplnost dokumentace, převod souřadnic, nejasnost pojmenování')
    st.info('❗Třeba dodělat vizualizace pro zbytek otázek a připojit data o počasí abych se mohla podívat zda je korelace mezi výší teploty/vlhkosti a počtem dopravních nehod.')

elif st.session_state.active_dashboard == 'obecný_přehled':
    col1, col2, col3 = st.columns(3, gap="medium")
    df_but1 = execute_sql("SELECT p1, accident_year, accident_month, p13a as úmrtí, p14 as hmotná_škoda FROM accidents_in_time")
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
    df_but2 = execute_sql("""SELECT gt.p1, gt.lat, gt.lon, g.k, n.p4a, n.p5a, n.p6, n.p9 
                             FROM dopravni_nehody_cr.gps_wgs84 as gt
                             LEFT JOIN dopravni_nehody_cr.gps as g ON g.p1 = gt.p1
                             LEFT JOIN dopravni_nehody_cr.nehody as n ON n.p1 = gt.p1""")
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

    with col2text:
        st.text(f"""
                Typy komunikací jsou vymezeny v zákoně č. 13/1997 Sb.

                Nejvice nehod se odehrává na Místních komunikacích: {biggest_cat_val}.

                Níže se můžete podívat na mapu ČR na níž je vykreslena hustota dopravních nehod.
                Dle očekávání se vetší koncentrace nehod objevuje kolem velkých měst a významných dopravních uzlů.
                Výberem komunikace ve filtru můžete intenzitu nehod sledovat na konrétním typu komunikace.
                """)
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
    df_but3 = translate(execute_sql("""SELECT p1, accident_year, accident_month, p5a, p6, p8, p8a, p9, p10, p11, p11a, 
                          p12, p13a, p13b, p13c, p29, p29a, p30a, p30b, p33c, p33g, p34, id_vozidla, p44, p45a
                          FROM dopravni_nehody_cr.accidents_crash"""))
    causes = sorted(df_but3['zavinění_nehody'].unique())
    crash_types = sorted(df_but3['druh_nehody'].unique())
    type_crash, determined_cause = st.columns(2, gap="large")
    with type_crash:
        st.subheader('Typy nehod')
        top_type_df = top_1_in_cat(df_but3, 'p1', 'druh_nehody')
        if not top_type_df.empty:
            nazev = top_type_df['druh_nehody'].iloc[0]
            pocet = top_type_df['Pocet_vyskytu'].iloc[0]
        st.metric(
            label=f"Nejčastější typ nehody: {nazev}", 
            value=f"{pocet} případů")
        df_crash_types = ratio_in_category(df_but3, 'p1', 'druh_nehody')
        crash_types_graph = px.bar(df_crash_types.tail(10),
                                   x='druh_nehody',
                                   y='Pocet_vyskytu',
                                   color='Pocet_vyskytu',
                                   color_continuous_scale='Reds',
                                   text='Pocet_vyskytu',
                                   labels={'Pocet_vyskytu': 'Počet výskytů', 'druh_nehody': ''})
        
        crash_types_graph.update_layout(yaxis=dict(
                                            type='linear',
                                            range=[0, 80000],       
                                            dtick=10000,            
                                            title='Počet nehod')
                                            )

        unify_graphs(crash_types_graph)

        st.divider()
        st.subheader('Následky u konkrétních typů nehod')
        selected_cause = st.selectbox("Vyberte typ nehody:", options=list(crash_types), key='crash_types')
        if selected_cause == 'srážka s domácím zvířetem':
            st.subheader('Srážky s domácím mazlíčkem')
            category_conseq(df_but3[df_but3['druh_nehody']=='srážka s domácím zvířetem'].reset_index(), 'srážka s domácím zvířetem', 'druh_nehody', 'charakter_nehody', 'pie')
            st.divider()
            st.subheader('Druhy domácích mazlíčků')
            category_conseq(df_but3[df_but3['druh_nehody']=='srážka s domácím zvířetem'].reset_index(), 'srážka s domácím zvířetem', 'druh_nehody', 'druh_zvěře/zvířete', 'bar')
        elif selected_cause == 'srážka s lesní zvěří':
            st.subheader('Srážky s divokou zvěří')
            category_conseq(df_but3[df_but3['druh_nehody']=='srážka s lesní zvěří'].reset_index(), 'srážka s lesní zvěří', 'druh_nehody', 'charakter_nehody', 'pie')
            st.divider()
            st.subheader('Druhy divoké zvěře')
            category_conseq(df_but3[df_but3['druh_nehody']=='srážka s lesní zvěří'].reset_index(), 'srážka s lesní zvěří', 'druh_nehody', 'druh_zvěře/zvířete', 'bar')
        else:
            category_conseq(df_but3, selected_cause, 'druh_nehody', 'charakter_nehody', 'pie')

    with determined_cause:
        st.subheader('Zavinění')
        top_type_df = top_1_in_cat(df_but3, 'p1', 'zavinění_nehody')
        if not top_type_df.empty:
            nazev = top_type_df['zavinění_nehody'].iloc[0]
            pocet = top_type_df['Pocet_vyskytu'].iloc[0]
        st.metric(
            label=f"Nejčastější zavinění: {nazev}", 
            value=f"{pocet} případů")
        df_crash_cause = ratio_in_category(df_but3, 'p1', 'zavinění_nehody')
        crash_cause_graph = px.bar(df_crash_cause.tail(10),
                                   x='zavinění_nehody',
                                   y='Pocet_vyskytu',
                                   color = 'Pocet_vyskytu',
                                   color_continuous_scale='Reds',
                                   text='Pocet_vyskytu',
                                   labels={'Pocet_vyskytu': 'Počet výskytů', 'zavinění_nehody': ''})
        unify_graphs(crash_cause_graph)
        st.divider()
        st.subheader('Následky u různých viníků')
        selected_cause = st.selectbox("Vyberte vyníka:", options=list(causes), key='causes_types')
        if selected_cause == 'chodcem':
            st.subheader("Následky nehod zaviněných chodci")
            category_conseq(df_but3, 'chodcem', 'zavinění_nehody', 'charakter_nehody', 'pie')
            st.divider()
            st.subheader("Pohlaví chodců zapletených do dopravních nehod")
            category_conseq(df_but3, 'chodcem', 'zavinění_nehody', 'kategorie_chodce', 'bar')
            st.text("Nejvíce s auty na silnicích střetávají muži. U žen je to výrazně nižší číslo.")
            st.divider()
            st.subheader("Poměr chodců s reflexním vybavením")
            category_conseq(df_but3, 'chodcem', 'zavinění_nehody', 'reflexní_prvky_u_chodce', 'pie')
            st.text("Z této informace je zřejmé, že je absence reflexních prvků u chodců zapetených do dopravní nehody takřka pravidlem")
        else:
            category_conseq(df_but3, selected_cause, 'zavinění_nehody', 'charakter_nehody', 'pie')
        

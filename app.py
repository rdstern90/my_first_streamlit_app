import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

driver_tags = {"leclerc":"LEC","sainz":"SAI","hamilton":"HAM",
               "russell":"RUS","kevin_magnussen":"MAG","bottas":"BOT",
               "ocon":"OCO","tsunoda":"TSU","alonso":"ALO",
               "zhou":"ZHO","mick_schumacher":"MSC","stroll":"STR",
               "albon":"ALB","ricciardo":"RIC","norris":"NOR",
               "latifi":"LAT","hulkenberg":"HUL","perez":"PER",
               "max_verstappen":"VER","gasly":"GAS","vettel":"VET",
               "de_vries":"DEV"}

tag_to_name = {
    "LEC": "Charles Leclerc",
    "SAI": "Carlos Sainz",
    "HAM": "Lewis Hamilton",
    "RUS": "George Russell",
    "MAG": "Kevin Magnussen",
    "BOT": "Valtteri Bottas",
    "OCO": "Esteban Ocon",
    "TSU": "Yuki Tsunoda",
    "ALO": "Fernando Alonso",
    "ZHO": "Guanyu Zhou",
    "MSC": "Mick Schumacher",
    "STR": "Lance Stroll",
    "ALB": "Alexander Albon",
    "RIC": "Daniel Ricciardo",
    "NOR": "Lando Norris",
    "LAT": "Nicholas Latifi",
    "HUL": "Nico Hulkenberg",
    "PER": "Sergio Perez",
    "VER": "Max Verstappen",
    "GAS": "Pierre Gasly",
    "VET": "Sebastian Vettel",
    "DEV": "Nyck de Vries"
}

def format_name(name):
    formatted_name = name.replace('_', ' ').title()
    return formatted_name
def get_age_from_birthdate(dt):
    birthdate = datetime.strptime(dt, '%Y-%m-%d').date()
    today = datetime.today().date()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


# Set app title and description
st.set_page_config(page_title="F1 2022 at a Glance", page_icon=":checkered_flag:", layout="wide")

# Define data loading function and cache it
@st.cache
def load_lap_data():
    df = pd.read_csv('data/F12022.csv')
    df = df.replace({'driverref':driver_tags})
    return df
df_laps = load_lap_data()

@st.cache
def load_results_data():
    df = pd.read_csv('data/F12022-Results.csv')
    df = df.replace({'driverref':driver_tags})
    return df
df_results = load_results_data()

@st.cache
def load_standings_data():
    df = pd.read_csv('data/F12022-Standings.csv')
    df = df.replace({'driverref':driver_tags})
    return df
df_standings = load_standings_data()


col1, col2, col3, col4 = st.columns([3,4,2,6])

with col1:
    st.image('logo.png')
    # round dropdown
    round_list = df_laps['roundNum'].unique()
    selected_round_num = st.selectbox('Select a race:', round_list)
    selected_df_laps = df_laps[df_laps['roundNum'] == selected_round_num]
    selected_df_results = df_results[df_results['roundNum'] == selected_round_num]
    selected_df_standings = df_standings[df_standings['roundNum'] == selected_round_num]

    # driver dropdown
    driver_refs = selected_df_laps['driverref'].unique()
    selected_driver_ref = st.selectbox('Select Driver', ['All Drivers'] + list(driver_refs))
    num_laps = int(selected_df_laps['lap'].max())
with col2:
    st.subheader("Point Scorers (This Race)")
    # Create bar chart
    chart = alt.Chart(selected_df_results.query('points != 0')).mark_bar().encode(
        y=alt.Y('points', title='Points'),
        x=alt.X('driverref', title='Driver', sort="-y"),
        tooltip=['driverref', 'points'],
        color=alt.condition(
            alt.FieldEqualPredicate(field='driverref', equal=selected_driver_ref),
            alt.value("yellow"),
            alt.value('steelblue')
        )
    )
    st.altair_chart(chart, use_container_width=True)
    
with col3:
    if selected_driver_ref != 'All Drivers':
        driver_info = df_standings[df_standings['driverref'] == selected_driver_ref].drop_duplicates('driverref')
        st.subheader("Driver Info")
        st.text(tag_to_name[selected_driver_ref])
        st.text(format_name(driver_info['constructorId'].values[0]))
        st.text(driver_info['nationality'].values[0])
        dob = driver_info['dob'].values[0]
        st.text(dob)
        st.text(get_age_from_birthdate(dob))
    else:
        st.subheader("Race DNFs")
        dnf_df = selected_df_results[['driverref','status']]
        dnf_df = dnf_df[dnf_df['status'] != "Finished"].rename(columns={"driverref":"Driver", "status":"Reason"})

        st.dataframe(dnf_df.reset_index().drop(columns={'index'}))
with col4:
    st.subheader("Accumulated Points")
    # Create bar chart
    chart = alt.Chart(selected_df_standings.query('points != 0')).mark_bar().encode(
        y=alt.Y('points', title='Points'),
        x=alt.X('driverref', title='Driver', sort="-y"),
        tooltip=['driverref', 'points'],
        color=alt.condition(
            alt.FieldEqualPredicate(field='driverref', equal=selected_driver_ref),
            alt.value("yellow"),
            alt.value('steelblue')
        )
    )
    st.altair_chart(chart, use_container_width=True)



col1, col2 = st.columns([2,1])

if selected_driver_ref != 'All Drivers':
    selected_df_laps = selected_df_laps[selected_df_laps['driverref'] == selected_driver_ref]
    selected_df_results = selected_df_results[selected_df_results['driverref'] == selected_driver_ref]
    selected_df_standings = selected_df_results[selected_df_results['driverref'] == selected_driver_ref]

with col1:
    # full lap/pos chart
    line = alt.Chart(selected_df_laps).mark_line().encode(
        alt.X('lap', scale=alt.Scale(domain=[0,num_laps]), title="Lap"),
        alt.Y('position', scale=alt.Scale(domain=[0,21]), title="Lap"),
        color=alt.Color('driverref', legend=None),
    ).properties(
        title='Driver Positions by Lap',
        height=500
    )
    # last lap df specifically for labels
    last_lap_df = selected_df_laps.groupby('driverref').tail(1)
    #label chart
    label = alt.Chart(last_lap_df).mark_text(align='left', dx=3, dy=5).encode(
        alt.X('lap'),
        alt.Y('position', scale=alt.Scale(domain=[0,21])),
        color='driverref',
        text='driverref'
    )
    st.altair_chart(line+label, use_container_width=True)

with col2:
    selected_df_results['grid_start'] = selected_df_results['grid_start'].replace(0, 20).copy()
    selected_df_results = pd.melt(selected_df_results, id_vars=['driverref'], value_vars=['grid_start','position'])

    # start end chart
    line = alt.Chart(selected_df_results).mark_line().encode(
        alt.X('variable', title=None, axis=alt.Axis(labelAngle=0)),
        alt.Y('value', scale=alt.Scale(domain=[0,21])),
        color=alt.Color('driverref', legend=None),
    ).properties(
        title='Driver Start vs Finish',
        height=500,
    )
    label = alt.Chart(selected_df_results[selected_df_results['variable'] == "position"]).mark_text(align='left', dx=3, dy=5).encode(
        alt.X('variable', title=None),
        alt.Y('value', scale=alt.Scale(domain=[0,21])),
        color='driverref',
        text='driverref'
    )
    st.altair_chart(line+label, use_container_width=True)

import streamlit as st
import pandas as pd
from utils.data_mangement import get_most_recent_file
import datetime
from utils.cycle_visualization import visualize_cycle


st.set_page_config(page_title = 'Ciclo Actual', page_icon = '🔛')
st.markdown('<h1 style="color: ; font-weigh: 400;"> Ciclo Actual <h/1>', unsafe_allow_html= True)
st.markdown('<hr style = "margin: 0;">', unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)


# load data
most_recent, number = get_most_recent_file('./data/', f'{st.session_state.name}_ciclo')

if most_recent != None:
    st.session_state.df = pd.read_excel(most_recent)
    st.session_state.df['Fecha'] = pd.to_datetime(st.session_state.df['Fecha']).dt.date
    if st.session_state.df.Fecha.iloc[-1] == datetime.date.today():
        st.warning("Recuerda cargar los datos de hoy")
    visualize_cycle(st.session_state.df)
else:
    st.warning("Ups! Parece que no has registrado ningún ciclo, por favor añade uno.")
    st.session_state.added_today_data = False
    st.stop()



import streamlit as st
from utils.data_mangement import get_available_files
from utils.cycle_visualization import visualize_cycle
import pandas as pd


st.set_page_config(page_title = 'Ciclos anteriores', page_icon = '🔙')
st.markdown('<h1 style="color: ; font-weigh: 400;"> Ciclos anteriores  <h/1>', unsafe_allow_html= True)
st.markdown('<hr style = "margin: 0;">', unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)

if 'authentication_status' not in st.session_state:
    st.warning('Por favor, introduce tu usuario y contraseña')
else:
    # list of cycles
    files_list = get_available_files('./data/', f'{st.session_state.name}_ciclo')
    files_list.sort()
    files_list = files_list[0:-1]
    files_dict = {file.split('_')[1].replace('.xlsx', ''): file for file in files_list}

    if len(files_list)==0:
        st.warning("Ups! Parece que no has registrado ningún ciclo, por favor añade uno en la página principal.")
        st.stop()

    # dropdown with cycle name
    file_chosen = st.selectbox('Elige un ciclo:', files_dict.keys())

    st.session_state.df = pd.read_excel(files_dict[file_chosen])
    st.session_state.df['Fecha'] = pd.to_datetime(st.session_state.df['Fecha']).dt.date

    visualize_cycle(st.session_state.df)
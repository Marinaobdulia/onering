import streamlit as st
from utils.data_mangement import get_available_files
from utils.cycle_visualization import visualize_cycle


st.set_page_config(page_title = 'Load previous cycles', page_icon = '🔙')
st.markdown('<h1 style="color: ; font-weigh: 400;"> Load previous cycles <h/1>', unsafe_allow_html= True)
st.markdown('<hr style = "margin: 0;">', unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)

# list of cycles
files_list = get_available_files('./data/', f'{st.session_state.name}_ciclo')
files_list = files_list[0:-1]
files_dict = {file.split('_')[1].replace('.xlsx', ''): file for file in files_list}

if len(files_list)==0:
    st.warning("Ups! Parece que no has registrado ningún ciclo, por favor añade uno en la página principal.")
    st.stop()

# dropdown with cycle name
file_chosen = st.selectbox('Elige un ciclo:', files_dict.keys())

visualize_cycle(files_dict[file_chosen])
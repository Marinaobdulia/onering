import streamlit as st
from utils.data_mangement import get_available_files
import pandas as pd
from utils.sinthotermic import find_sintho
from utils.plots import plot_sintho


st.set_page_config(page_title = 'Load previous cycles', page_icon = '🔙')
st.markdown('<h1 style="color: ; font-weigh: 400;"> Load previous cycles <h/1>', unsafe_allow_html= True)
st.markdown('<hr style = "margin: 0;">', unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)

# list of cycles
files_list = get_available_files('./data/', f'{st.session_state.name}_ciclo')
files_dict = {file.split('_')[1].replace('.xlsx', ''): file for file in files_list}

if len(files_list)==0:
    st.warning("Oops! It seems you haven't register any cycle, please add one on the main page")
    st.stop()

# dropdown with cycle name
file_chosen = st.selectbox('Choose one cycle:', files_dict.keys())
strict = st.checkbox('Strict Algorithm')

if strict:
    dec_above = 0.2
else:
    dec_above = 0.1

# show table and graph
df = pd.read_excel(files_dict[file_chosen])

df = find_sintho(df, dec_above)

# after loading today's data, show graph
chart = plot_sintho(df)

tab1, tab2 = st.tabs(["Graph", "Table"])

with tab1:
    st.altair_chart(chart, use_container_width=True)
with tab2:
    st.write(df)
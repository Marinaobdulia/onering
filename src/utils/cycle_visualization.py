import streamlit as st
from utils.plots import plot_sintho
from utils.sinthotermic import find_sintho
from utils.sinthotermic import dict_phases

def visualize_cycle(df):
    st.subheader('Your current cycle')

    strict = st.checkbox('Strict Algorithm')

    if strict:
        dec_above = 0.2
    else:
        dec_above = 0.1
    
    st.session_state.df = find_sintho(st.session_state.df, dec_above)

    # after loading today's data, show graph
    chart = plot_sintho(st.session_state.df)

    current_phase = st.session_state.df['phase'].iloc[-1]
    st.info(f'Actualmente estás {dict_phases[current_phase]}')


    tab1, tab2 = st.tabs(["Graph", "Table"])

    with tab1:
        st.altair_chart(chart, use_container_width=True)
    with tab2:
        st.write(st.session_state.df)
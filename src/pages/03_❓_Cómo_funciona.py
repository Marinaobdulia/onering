import streamlit as st

st.set_page_config(page_title = 'Cómo funciona', page_icon = '🔙')
st.markdown('<h1 style="color: ; font-weigh: 400;"> Cómo funciona <h/1>', unsafe_allow_html= True)
st.markdown('<hr style = "margin: 0;">', unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)

st.write('Explicando cosas')

tab1, tab2, tab3 = st.tabs(["Temperatura", "Flujo", "Cérvix"])

with tab1:
    st.write("Reglas para tomar la temperatura")
with tab2:
    st.write("Reglas para entender el flujo")
with tab3:
    st.write("Reglas para entender el cuello uterino")
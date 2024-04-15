import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd
from utils.data_mangement import get_most_recent_file
import datetime


def main():
    # initialise values
    if 'button_ok' not in st.session_state:
        st.session_state.button_ok = False
        st.session_state.added_today_data = False
       
    # load data
    most_recent, number = get_most_recent_file('./data/', f'{st.session_state.name}_ciclo')

    if most_recent != None:
        st.session_state.df = pd.read_excel(most_recent)
        st.session_state.df['Fecha'] = pd.to_datetime(st.session_state.df['Fecha']).dt.date
        if st.session_state.df.Fecha.iloc[-1] == datetime.date.today():
            st.session_state.added_today_data = True
    else:
        st.warning("Ups! Parece que no has registrado ningún ciclo. Por favor, añádelo.")
        st.session_state.added_today_data = False
        st.stop()

    if st.session_state.added_today_data == False:
        cola, colb, colc = st.columns(3)
        with colb.form('add info'):
            new_cycle = st.checkbox('Inicio de ciclo')
            date = st.date_input("Fecha del registro", datetime.date.today())
            temp = st.number_input('Temperatura', 35.5, 42.00, value = 36.00, step = 0.05)
            # col1, col2, col3 = st.columns(3)
            # with col1:
            #     st.checkbox('Alcohol')
            # with col2:
            #     st.checkbox('Enfermedad')
            # with col3:
            #     st.checkbox('Hora diferente')
            flux = st.selectbox('Flujo', ['','F', 'f', 'S'])
            # cuello1 = st.selectbox('Apertura del cuello', ['Abierto', 'Semi-abierto', 'Cerrado'])
            # cuello2 = st.selectbox('Altura del cuello', ['Alto', 'Medio', 'Bajo'])
            # cuello3 = st.selectbox('Tacto del cuello', ['Suave', 'Firme'])
            st.session_state.button_ok = st.form_submit_button("✅ Guardar")

    if st.session_state.button_ok:
        st.write(temp)
        if new_cycle:
            st.write('Creando un excel para un nuevo ciclo')
            st.session_state.df = pd.DataFrame(columns = ['Fecha', 'Temperatura'])
            number = int(number)+1

        one_more_row = len(st.session_state.df.index)
        st.session_state.df.loc[one_more_row, 'Fecha'] = date
        st.session_state.df.loc[one_more_row, 'Temperatura']= temp
        st.session_state.df.loc[one_more_row, 'Flujo']= flux
        st.session_state.df.to_excel(f'./data/{st.session_state.name}_ciclo'+str(number)+'.xlsx', index = None)


st.set_page_config(page_title = 'Inicio', page_icon = '🏠')


with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

col_1, col_2, col_3, col_4, col_5 = st.columns(5)
with col_5:
    new_user = st.button('🆕 Registrar nuevo usuario')

# register new user_option
if new_user:
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False)
        if email_of_registered_user:
            st.success('Usario registrado correctamente')

        with open('../config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
    except Exception as e:
        st.error(e)

# login
st.session_state.name, st.session_state.authentication_status, username = authenticator.login('main')



if st.session_state.authentication_status:
    # authenticator.logout('Logout', 'main')
    st.markdown('<h1 style="color: ; font-weigh: 400;"> Registra un nuevo día 🌅 <h/1>', unsafe_allow_html= True)
    st.markdown('<hr style = "margin: 0;">', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    main()
elif st.session_state.authentication_status == False:
    st.error('Usuario/contraseña incorrectos')
elif st.session_state.authentication_status == None:
    st.warning('Por favor, introduce tu usuario y contraseña')
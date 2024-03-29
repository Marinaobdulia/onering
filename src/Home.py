import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd
from utils.data_mangement import get_most_recent_file
from utils.sinthotermic import find_sintho, find_phase, dict_phases
from utils.plots import plot_sintho
import datetime

# st.set_page_config(page_title = 'Home', page_icon = '🏠')

def main():

    # initialise values
    if 'button_ok' not in st.session_state:
        st.session_state.button_ok = False

    with st.sidebar:
        # ask for today's info
        with st.form('add info'):
            new_cycle = st.checkbox('New cycle')
            date = st.date_input("Register date", datetime.date.today())
            temp = st.number_input('Temperature', 35.5, 42.00, value = 36.00, step = 0.05)
            # col1, col2, col3 = st.columns(3)
            # with col1:
            #     st.checkbox('Alcohol')
            # with col2:
            #     st.checkbox('Illness')
            # with col3:
            #     st.checkbox('Different time')
            flux = st.selectbox('Flux', ['','F', 'f', 'S'])
            # cuello1 = st.selectbox('Cervix opening', ['Open', 'Halfway', 'Closed'])
            # cuello2 = st.selectbox('Cervix height', ['Up', 'Halfway', 'Down'])
            # cuello3 = st.selectbox('Cervix touch', ['Soft', 'Hard'])
            st.session_state.button_ok = st.form_submit_button("Submit")
        
            # load data
    most_recent, number = get_most_recent_file('./data/', f'{st.session_state.name}_ciclo')

    if most_recent != None:
        st.session_state.df = pd.read_excel(most_recent)
    else:
        st.warning("Oops! It seems you haven't register any cycle, please add one with the menu on the left")
        st.stop()
        
    if st.session_state.button_ok:
        st.write(temp)
        if new_cycle:
            st.write('Creating excel for new cycle')
            st.session_state.df = pd.DataFrame(columns = ['Fecha', 'Temperatura'])
            number = int(number)+1

        one_more_row = len(st.session_state.df.index)
        st.session_state.df.loc[one_more_row, 'Fecha'] = date
        st.session_state.df.loc[one_more_row, 'Temperatura']= temp
        st.session_state.df.loc[one_more_row, 'Flujo']= flux
        st.session_state.df.to_excel(f'./data/{st.session_state.name}_ciclo'+str(number)+'.xlsx', index = None)

        
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
    st.info(f'You are currently {dict_phases[current_phase]}')

    if current_phase == 'luteal':
        st.success("Unprotected sex won't lead to a pregnancy")


    tab1, tab2 = st.tabs(["Graph", "Table"])

    with tab1:
        st.altair_chart(chart, use_container_width=True)
    with tab2:
        st.write(st.session_state.df)

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

# login
st.session_state.name, authentication_status, username = authenticator.login('main')

if authentication_status:
    # authenticator.logout('Logout', 'main')
    st.markdown('<h1 style="color: ; font-weigh: 400;"> Good morning, sunshine 🌅 <h/1>', unsafe_allow_html= True)
    st.markdown('<hr style = "margin: 0;">', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    main()
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
import pandas as pd
import numpy as np
import streamlit as st

def find_baseline(df):
    # Find the highest temperature over the last six available upon registry date
    df['Max_Last_Six'] = df['Temperatura'].rolling(window=6, min_periods=6).apply(lambda x: x[:-1].max())
    
    # Find the baseline temperature
    mask = (df['Temperatura'] >= df['Max_Last_Six']) & ~(df['Temperatura'].shift(1) >= df['Max_Last_Six'].shift(1))
    first_occurrence_index = mask.idxmax()
    df['First_Over_Max_Last_Six'] = False
    if first_occurrence_index>0:
        df.loc[first_occurrence_index, 'First_Over_Max_Last_Six'] = True
        # Get that temperature
        baseline = df[df.First_Over_Max_Last_Six == True].Max_Last_Six.iloc[0]
    else:
        baseline=40
    
    df['baseline'] = baseline

    return df

def confirm_ovulation_temp(df, dec_above):
    df = find_baseline(df)
    # Check the next three temperatures are higher than that value
    df['higher_baseline']=df.apply(lambda x: ((x.Temperatura >= x.baseline+dec_above)), axis=1)

    df['days_higher_than_baseline'] = df['higher_baseline'].rolling(window=4, min_periods = 1).sum()

    # confirm ovulation
    df['ovulation_confirmed_temp'] = False
    mask_ovulation = ((df.ovulation_confirmed_temp == False) & (df.days_higher_than_baseline==3))
    first_occurrence_ovulation = mask_ovulation.idxmax()
   
    if first_occurrence_ovulation>0:
        df.loc[first_occurrence_ovulation::, 'ovulation_confirmed_temp'] = True    
    return df

def confirm_ovulation_flux(df):# Find last 'F' index
    last_F_index = df[df['Flujo'] == 'F'].index.max()

    # Create 'last_F' column
    df['last_F'] = 0
    if last_F_index>0:
        df.loc[last_F_index::, 'last_F'] = 1

    # Fill forward the last 'F' value
    df['last_F'] = df['last_F'].ffill().astype(int)
    df['days_from_F'] = df['last_F'].rolling(window=3, min_periods = 1).sum()

    # confirm ovulation
    df['ovulation_confirmed_flux'] = False
    mask_ovulation = ((df.ovulation_confirmed_flux == False) & (df.days_from_F==3))
    first_occurrence_ovulation = mask_ovulation.idxmax()

    if first_occurrence_ovulation>0:
        df.loc[first_occurrence_ovulation::, 'ovulation_confirmed_flux'] = True
    return df

def find_phase(last_day):
    if last_day.Flujo == 'S':
        current_phase = 'periodo'
    elif last_day.higher_baseline == False and last_day.ovulation_confirmed == True:
        current_phase = 'periodo'
    elif last_day.Flujo == 'f' or last_day.Flujo == 'F' or last_day.higher_baseline == False:
        current_phase = 'folicular'
    elif last_day.higher_baseline == True and last_day.ovulation_confirmed == False:
        current_phase = 'ovulatoria'
    elif last_day.ovulation_confirmed == True:
        current_phase = 'lutea'
    else:
        current_phase = 'indefinida'
    return current_phase

def find_sintho(df, dec_above=0.1):
    df = confirm_ovulation_temp(df, dec_above)

    df = confirm_ovulation_flux(df)

    df['ovulation_confirmed'] = (df.ovulation_confirmed_temp & df.ovulation_confirmed_flux)

    df['phase'] = df.apply(find_phase, axis=1)

    return df

dict_phases = {'periodo': 'en tu periodo',
               'follicular': 'en la fase folicular',
               'ovulatoria': 'ovulando o acabas de ovular',
               'lutea': 'en la fase lútea',
               'indefinida': 'en una fase indefinida. Por favor, añade más datos.'}
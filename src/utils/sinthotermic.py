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

def confirm_ovulation(df, dec_above=0.2):
    # Check the next three temperatures are higher than that value
    df['higher_baseline']=df.apply(lambda x: ((x.Temperatura >= x.baseline+dec_above)), axis=1)

    df['days_higher_than_baseline'] = df['higher_baseline'].rolling(window=4, min_periods = 1).sum()

    # confirm ovulation
    df['ovulation_confirmed'] = False
    mask_ovulation = ((df.ovulation_confirmed == False) & (df.days_higher_than_baseline==3))
    first_occurrence_ovulation = mask_ovulation.idxmax()
   
    if first_occurrence_ovulation>0:
        df.loc[first_occurrence_ovulation::, 'ovulation_confirmed'] = True    
    return df

def find_sintho(df):
    df = find_baseline(df)

    df = confirm_ovulation(df)

    return df

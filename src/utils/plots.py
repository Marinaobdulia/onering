import altair as alt
import pandas as pd

def plot_sintho(df):

    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
    df['Fecha2'] = df['Fecha'].shift(1)


    # Calculate the start_date and end_date to include at least 28 days
    min_days = min(28, len(df))  # Ensure at least 28 days
    if min_days<28:
        num_days = 28-min_days
        start_date = df['Fecha'].min()
        end_date = df['Fecha'].max() + pd.DateOffset(days=num_days)
    else:
        start_date = df['Fecha'].min()
        end_date = df['Fecha'].max()
    domain = list(pd.to_datetime([start_date, end_date]).astype(int) / 10 ** 6)



    # Plot
    line = alt.Chart(df).mark_line().encode(
        x='Fecha:T',
        y=alt.Y('Temperatura:Q', scale=alt.Scale(domain=[36, 37]))
    )

    points = alt.Chart(df).mark_point().encode(
        x='Fecha:T',
        y='Temperatura:Q',
        tooltip=['Fecha:T', 'Temperatura:Q']
    )

    if df['baseline'].iloc[-1]!=40:
        baseline = alt.Chart(df).mark_line().encode(
            x='Fecha:T',
            y=alt.Y('baseline:Q', scale=alt.Scale(domain=[35.9, 37]))
        )
    else:
        baseline = alt.Chart(pd.DataFrame({'y':[36]})
                             ).mark_line().encode(y='y')

    points_ovulation = alt.Chart(df[df['ovulation_confirmed']]).mark_point(color='green', filled = True, size = 100).encode(
        x='Fecha:T',
        y='Temperatura:Q',
        tooltip=['Fecha:T', 'ovulation_confirmed']
    )

    light_blue_band = alt.Chart(df[df['Flujo'] == 'f']).mark_rect(color='lightblue', opacity = 0.3).encode(
        x='Fecha:T',
        x2='Fecha2:T'
    )

    dark_blue_band = alt.Chart(df[df['Flujo'] == 'F']).mark_rect(color='darkblue', opacity = 0.3).encode(
        x='Fecha:T',
        x2='Fecha2:T'
    )

    red_band = alt.Chart(df[df['Flujo'] == 'S']).mark_rect(color='red', opacity = 0.3).encode(
        x='Fecha:T',
        x2='Fecha2:T'
    )


    chart = (red_band + light_blue_band + dark_blue_band + line + points + baseline + points_ovulation ).properties(
        title='Temperatura vs Fecha',
        width=600,
        height=300
    ).encode(
    x=alt.X('Fecha:T', scale=alt.Scale(domain=domain))
    ).interactive()

    chart.configure_axis(
        labelAngle=45
    )

    return chart
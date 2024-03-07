import altair as alt
import pandas as pd

def plot_sintho(df):
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date

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
            y=alt.Y('baseline:Q', scale=alt.Scale(domain=[36, 37]))
        )
    else:
        baseline = alt.Chart(pd.DataFrame({'y':[36]})
                             ).mark_line().encode(y='y')

    points_ovulation = alt.Chart(df[df['ovulation_confirmed']]).mark_point(color='green').encode(
        x='Fecha:T',
        y='Temperatura:Q',
        tooltip=['Fecha:T', 'ovulation_confirmed']
    )

    chart = (line + points+baseline+points_ovulation).properties(
        title='Temperatura vs Fecha',
        width=600,
        height=300
    ).interactive()

    chart.configure_axis(
        labelAngle=45
    )

    return chart
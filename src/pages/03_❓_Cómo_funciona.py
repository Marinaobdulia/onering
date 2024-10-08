import streamlit as st

st.set_page_config(page_title = 'Cómo funciona', page_icon = '🔙')
st.markdown('<h1 style="color: ; font-weigh: 400;"> Cómo funciona <h/1>', unsafe_allow_html= True)
st.markdown('<hr style = "margin: 0;">', unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)

st.write("""Onering se basa en tres indicadores para estimar en qué fase del ciclo te encuentras: 
la temperatura basal, el flujo cervical y la posición del cuello del útero.
         
Estos tres elementos proporcionan información valiosa sobre el ciclo menstrual 
de una mujer y pueden ayudar a identificar los días más fértiles.
         
Te explicamos con mayor detalle cada uno de ellos:""")

tab1, tab2, tab3 = st.tabs(["Temperatura", "Flujo", "Cérvix"])

with tab1:
    st.write("""La temperatura basal es la temperatura del cuerpo en reposo, 
medida en el momento en que te despiertas por la mañana, 
antes de levantarte de la cama o de realizar cualquier actividad física. 
Se mide con un [termómetro capaz de indicar dos decimales](https://www.amazon.es/Domotherm-Rapid-Term%C3%B3metro-decimales-flexible/dp/B0014II7G6?th=1).

En el ciclo menstrual, la temperatura basal puede ayudar a detectar la ovulación. 
Antes de la ovulación, la temperatura basal suele ser más baja, y después de la ovulación,
tiende a subir ligeramente y permanecer elevada hasta el próximo periodo menstrual. 
Este aumento se debe a la liberación de la hormona **progesterona** después de la ovulación.

Es importante medir la temperatura basal a la **misma hora cada mañana** y bajo condiciones consistentes,
como **antes de levantarse de la cama o de hablar**, para obtener lecturas precisas. """)
with tab2:
    st.write("""El flujo cervical es una secreción vaginal natural que cambia en cantidad 
y consistencia a lo largo del ciclo menstrual de una mujer. 
Se puede observar en la ropa interior o al limpiarse después de ir al baño.

Durante la fase menstrual, el flujo cervical es escaso y puede ser más espeso. 
Después de la menstruación, se vuelve más abundante y fluido, similar a la clara 
de huevo cruda. Esta consistencia se asocia con la ovulación y suele indicar 
el momento más fértil del ciclo menstrual.

El flujo cervical actúa como un medio de transporte para los espermatozoides, 
ayudándolos a moverse hacia el óvulo. También puede proporcionar protección contra infecciones 
al mantener la vagina lubricada y limpia.""")
with tab3:
    st.write("""El cuello del útero, también conocido como cérvix, es la parte inferior y 
estrecha del útero que se conecta con la vagina. Tiene una abertura pequeña 
llamada orificio cervical, que se abre y cierra en diferentes 
momentos del ciclo menstrual y del embarazo.

Durante el ciclo menstrual, el cuello del útero cambia en respuesta a las 
fluctuaciones hormonales. En la fase menstrual y posmenstrual, el cérvix suele estar bajo,
firme y cerrado para proteger el útero de infecciones. Durante la ovulación, 
el cuello del útero se ablanda, se eleva y se abre ligeramente para permitir que los 
espermatozoides entren en el útero y se encuentren con un óvulo para la fertilización.

Observar los cambios en la posición, textura y apertura del cuello del útero puede
ser útil para determinar el momento más fértil del ciclo menstrual. Sin embargo, 
es importante tener en cuenta que esta técnica requiere práctica y puede no ser 
tan precisa como otras formas de seguimiento de la fertilidad.""")
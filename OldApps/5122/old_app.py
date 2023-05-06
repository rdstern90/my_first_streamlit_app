import streamlit as st
import random
import altair as alt
import numpy as np
import pandas as pd

st.header('Homework 1')

st.markdown(
"**QUESTION 1**: In previous homeworks you created dataframes from random numbers.\n"
"Create a datframe where the x axis limit is 100 and the y values are random values.\n"
"Print the dataframe you create and use the following code block to help get you started"
)

st.code(
''' 
x_limit = 

# List of values from 0 to 100 each value being 1 greater than the last
x_axis = np.arange()

# Create a random array of data that we will use for our y values
y_data = []

df = pd.DataFrame({'x': x_axis,
                     'y': y_data})
st.write(df)''',language='python')

x_limit = 100

# List of values from 0 to 100 each value being 1 greater than the last
x_axis = np.arange(0, x_limit, step=1)

# Create a random array of data that we will use for our y values
y_data = np.random.rand(x_limit)

df = pd.DataFrame({'x': x_axis,
                     'y': y_data})

st.dataframe(df)


st.markdown(
"**QUESTION 2**: Using the dataframe you just created, create a basic scatterplot and Print it.\n"
"Use the following code block to help get you started."
)

st.code(
''' 
scatter = alt.Chart().mark_point().encode()

st.altair_chart(scatter, use_container_width=True)''',language='python')

scatter = alt.Chart(df).mark_point().encode(
    x='x',
    y='y'
)
st.altair_chart(scatter, use_container_width=True)

st.markdown(
"**QUESTION 3**: Lets make some edits to the chart by reading the documentation on Altair.\n"
"https://docs.streamlit.io/library/api-reference/charts/st.altair_chart.  "
"Make 5 changes to the graph, document the 5 changes you made using st.markdown(), and print the new scatterplot.  \n"
"To make the bullet points and learn more about st.markdown() refer to the following discussion.\n"
"https://discuss.streamlit.io/t/how-to-indent-bullet-point-list-items/28594/3"
)

scatter = alt.Chart(df, title="X and Y Values").mark_point(size=1000, color="Green").encode(
    x=alt.X('x', title="X Values"),
    y=alt.Y('y', title="Y Values")
)

st.altair_chart(scatter, use_container_width=True)

st.markdown("The five changes I made were.....")
st.markdown("""
The 5 changes I made were:
- Added a chart title
- Added a label to the x axis
- Added a label to the y axis
- Changed the point colors
- Changed the point sizes
""")



st.markdown(
"**QUESTION 4**: Explore on your own!  Go visit https://altair-viz.github.io/gallery/index.html.\n "
"Pick a random visual, make two visual changes to it, document those changes, and plot the visual.  \n"
"You may need to pip install in our terminal for example pip install vega_datasets "
)

import altair as alt
from vega_datasets import data

source = data.wheat()

line_chart = alt.Chart(source).mark_trail(color="Green").encode(
    x='year:T',
    y='wheat:Q',
    size='wheat:Q'
).properties(
    width=700,
    height=340
)

st.altair_chart(line_chart)

st.markdown("""
The 2 changes I made were:
- Changing the line color to green
- Changed the width and height
"""
)


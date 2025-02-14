import pandas as pd 
import numpy as np 
import streamlit as st 
import plotly.express as px

df = pd.read_csv('vehicles_us.csv')

df['odometer'] = df['odometer'].fillna(df['odometer'].mean())
df['days_listed'] = df['days_listed'].fillna(df['days_listed'].mean())
df['price'] = df['price'].fillna(df['price'].mean())
df['model_year'] = df['model_year'].fillna(df['model_year'].mean())

st.header('Market of used cars. Original data')
st.write('Filter the data below to gain insight on the market of used cars')

model_choice = df['model'].unique()
selected_model = st.selectbox('Select a model', model_choice)

min_year, max_year = int(df['model_year'].min()), int(df['model_year'].max())
year_range = st.slider("Choose years", value=(min_year, max_year), min_value=min_year, max_value=max_year)
actual_range = list(range(year_range[0], year_range[1] + 1))

df_filtered = df[ (df['model'] == selected_model) & (df['model_year'].isin(actual_range)) ]

st.header('Price Analysis')
st.write('The price distribution of the selected model')

list_for_hist = ['condition', 'model_year', 'days_listed']  
selected_type = st.selectbox('Select a category to color by', list_for_hist)

fig1 = px.histogram(df_filtered, x='price', color=selected_type)
fig1.update_layout(title="<b> Split of price by {} <b>".format(selected_type))
st.plotly_chart(fig1)

df['age'] = 2025 - df['model_year']

def age_category(age):
    if age <= 5:
        return '0-5 years'
    elif age <= 10:
        return '6-10 years'
    elif age <= 15:
        return '11-15 years'
    else:
        return '16+ years'

df['age_category'] = df['age'].apply(age_category)


list_for_scatter = ['odometer', 'days_listed']  


choice_for_scatter = st.selectbox('Price dependency on', list_for_scatter)


fig2 = px.scatter(df, x='price', y=choice_for_scatter, color='age_category')
fig2.update_layout(title="<b> Price vs {} <b>".format(choice_for_scatter))
st.plotly_chart(fig2)
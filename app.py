import pandas as pd
import streamlit as st
import plotly.express as pt
import plotly.graph_objects as go
import numpy as np

df = pd.read_csv('vehicles_us.csv')
df.is_4wd = df.is_4wd.fillna(0)
df.is_4wd = df.is_4wd.astype(bool)
df.paint_color = df.paint_color.fillna('unknown')
df.cylinders = df.cylinders.fillna(0)
df[['manufacturer', 'model']] = df.model.str.split(' ', n = 1, expand = True)
df_manufacturer = df.groupby(['manufacturer', 'type'])['type'].count().unstack(fill_value=0)


st.title('Car analysis')


with st.expander("Data"):
        showData=st.multiselect('Filter: ',df.columns,default=list(df.columns))
        st.dataframe(df[showData],use_container_width=True)
model_year_df = df.groupby(by= 'model_year')['price'].agg(['mean', 'count'])

st.subheader('Vehicle :green[type] by :green[manufacturer]')
fig_1 = pt.bar(df_manufacturer)
fig_1.update_layout(
    yaxis_title = 'count'
)
st.plotly_chart(fig_1)

st.subheader('Histogram of :green[condition] vs :green[model year]')
fig2 = pt.histogram(df, x = 'model_year', color = 'condition')
st.plotly_chart(fig2)


st.subheader('Compare distribution between manufacturers')
manufacturer_1 = st.selectbox('Select manufacturer 1', df['manufacturer'].unique(), key='1')
manufacturer_2 = st.selectbox('Select manufacturer 2', df['manufacturer'].unique(), key= '2')
normalize = st.checkbox('Normalize histogram')
fig_3 = go.Figure()
if normalize:
    fig_3.add_trace(go.Histogram(x = df[df['manufacturer'] == manufacturer_1]['price'], histnorm= 'percent', name = manufacturer_1))
    fig_3.add_trace(go.Histogram(x = df[df['manufacturer'] == manufacturer_2]['price'], histnorm= 'percent', name = manufacturer_2))
else:
    fig_3.add_trace(go.Histogram(x = df[df['manufacturer'] == manufacturer_1]['price'], name = manufacturer_1))
    fig_3.add_trace(go.Histogram(x = df[df['manufacturer'] == manufacturer_2]['price'], name = manufacturer_2))
fig_3.update_layout(barmode='overlay')
fig_3.update_traces(opacity=0.75)
st.plotly_chart(fig_3)

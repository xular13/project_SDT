import pandas as pd
import streamlit as st
import plotly.express as pt

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

st.subheader('Vehicle type by manufacturer')
fig_1 = pt.bar(df_manufacturer)
fig_1.update_layout(
    yaxis_title = 'count'
)
st.plotly_chart(fig_1)
# fig = pt.scatter(model_year_df, y = 'mean', trendline = 'lowess')
# fig.update_layout(
#     xaxis_title = 'model year',
#     yaxis_title = 'price'
# )
# st.plotly_chart(fig)

# price_range = st.slider(
#      "What is your price range?",
#      value=(4, 3200))

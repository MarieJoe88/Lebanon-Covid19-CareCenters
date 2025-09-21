# Home.py
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title="Welcome")
st.title("Below you may find some summary data and the raw dataset used to create the visualizations.")
st.header("You can use the sidebar to navigate between pages.")

health_sts = pd.read_csv("health status.csv")
health_resources = pd.read_csv("health resources.csv")
edu_resources = pd.read_csv("Educational Resources.csv")

#Merge all 3 datasets using the common column Town
merged_df = pd.merge(health_sts, health_resources, on='Town', how='outer')
merged_df = pd.merge(merged_df, edu_resources, on='Town', how='outer')

st.divider()
grouped_df = merged_df.groupby("Governorate")["Town"].count().reset_index()
st.metric(label="Total number of towns",value=sum(grouped_df["Town"]))
st.subheader("Total number of towns per governorate: ")
st.dataframe(grouped_df,hide_index=True)


def load_data(data,nrows):
    return data.head(nrows)
data = load_data(merged_df,30)
st.divider()
if st.checkbox('Show raw data (first 30 rows)'):
    st.dataframe(data)


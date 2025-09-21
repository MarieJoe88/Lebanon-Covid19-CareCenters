import plotly.express as px
import pandas as pd
import streamlit as st


st.set_page_config(page_title="Towns and access to Care Centers (Special Needs)")
st.title("Care Centers in Lebanon")


health_sts = pd.read_csv("health status.csv")
health_resources = pd.read_csv("health resources.csv")
edu_resources = pd.read_csv("Educational Resources.csv")

#Merge all 3 datasets using the common column Town
merged_df = pd.merge(health_sts, health_resources, on='Town', how='outer')
merged_df = pd.merge(merged_df, edu_resources, on='Town', how='outer')

filtered_df = merged_df.copy()

#get all governorates names to use in filter
governorates = merged_df['Governorate'].unique().tolist()

#create new dataframe which is grouped per governorate
summary = filtered_df.groupby('Governorate').agg(
    total_cases_Covid19 = ('Nb of Covid-19 cases','sum'),
    total_towns=('Town','count'),
    total_care_centers = ('Total number of care centers','sum'),
    towns_with_sn = ('Percentage of towns with special needs indiciduals - With special needs','sum'),
    towns_with_care_centers=('Existence of nearby care centers - exists', 'sum'),
    towns_with_sn_care_centers=('Existence of special needs care centers - exists', 'sum')
).reset_index()

#add following columns to dataframe summary
summary['sn_centers_coverage_from_sn_towns']=((summary['towns_with_sn_care_centers']/summary['towns_with_sn'])*100).round(1)
summary['sn_centers_coverage_from_total_towns']=((summary['towns_with_sn_care_centers']/summary['total_towns'])*100).round(1)
summary['regular_centers_coverage']=((summary['towns_with_care_centers']/summary['total_towns'])*100).round(1)
summary['%_of_towns_with_sn']=((summary['towns_with_sn']/summary['total_towns'])*100).round(1)

#add checkbox for showing the summarized data
if st.checkbox("Show table with summarized data:"):
    st.dataframe(summary,hide_index=True)

#add filter for governorate
filtered_gov = st.selectbox(
    "Select Governorate",
    options=["All"] + sorted(governorates)
)

if filtered_gov != "All":
    summary = summary[summary['Governorate'] == filtered_gov]


summary = summary.sort_values(by='total_cases_Covid19',ascending=False)
#bar plot to show the total nbr of care centers per governorate
fig_5 = px.bar(
    summary,
    x='Governorate',
    y='total_cases_Covid19',
    text='total_care_centers',
    title='Total # of Covid-19 cases and care centers per governorate')

fig_5.update_traces(textposition='inside',insidetextfont=dict(size=15))
st.plotly_chart(fig_5)


#add slider to show governorates based on % of towns with special needs individuals
minimum = summary['%_of_towns_with_sn'].min()
maximum = summary['%_of_towns_with_sn'].max()
cases = st.slider('Use below slider: ',minimum,maximum,70.0)
st.write(f"Only show governorates where at least {cases}% of towns have special needs individuals")

summary =  summary[summary['%_of_towns_with_sn'] >= cases]

#bar plot to show diff per governorate between % of towns with regular care centers and special needs care centers (both from total nbr of towns) and special needs care centers (from total nbr of towns with special needs individuals)
fig_4 = px.bar(
    summary,
    x='Governorate',
    y=['regular_centers_coverage', 'sn_centers_coverage_from_total_towns','sn_centers_coverage_from_sn_towns'],
    barmode='group',
    title="Care Centers vs Special Needs Care Centers per Governorate",
    hover_data='total_cases_Covid19'
)

st.plotly_chart(fig_4)

st.subheader("Interpretation:")
st.write("We can see a huge gap between the percentage of towns per each governorate that have access to regular care centers versus the ones that have access to special needs care center. Even though most governorates have a high percentage of towns with special needs individuals, they do not have care centers that are specifically tailored to suit their needs.")

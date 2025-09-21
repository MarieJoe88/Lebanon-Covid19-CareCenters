import plotly.express as px
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Covid-19 cases")
st.title("Covid-19 cases in Lebanon")


health_sts = pd.read_csv("health status.csv")
health_resources = pd.read_csv("health resources.csv")
edu_resources = pd.read_csv("Educational Resources.csv")

#Merge all 3 datasets using the common column Town
merged_df = pd.merge(health_sts, health_resources, on='Town', how='outer')
merged_df = pd.merge(merged_df, edu_resources, on='Town', how='outer')

#create an additional column (boolean) showing 1 if any below 3 variables are 1 (presense of chronic disease), and 0 otherwise (absence of chronic disease)
chronic = ["Existence of chronic diseases - Hypertension",
           "Existence of chronic diseases - Cardiovascular disease ",
           "Existence of chronic diseases - Diabetes "
           ]
merged_df['has_chronic_disease']=merged_df[chronic].any(axis=1)

#get all governorates and towns to use in filter
governorates = merged_df['Governorate'].unique().tolist()
towns = merged_df['Town'].unique().tolist()

#governorate filter
selected_governorate = st.selectbox(
    "Select Governorate",
    options=["All"] + sorted(governorates)
)

#show towns in filter based on governorate chosen
filtered_towns = merged_df[merged_df["Governorate"] == selected_governorate]['Town'].unique()
selected_towns = st.selectbox(
    "Select Town",
    options = ["All"] + sorted(filtered_towns)
)

#chronic illness filter
chronic_filter = st.selectbox("Filter by Chronic Disease",["All","Yes","No"])


filtered_df = merged_df.copy()

#create an additional column (boolean) showing 1 if any below 4 variables are 1, and 0 otherwise (presence/absence of medical facilities))
facilities = ["Type and size of medical resources - Pharmacies","Type and size of medical resources - Medical Centers",
              "Type and size of medical resources - Hospitals","Type and size of medical resources - Clinics"]
filtered_df['medical_resources']=filtered_df[facilities].any(axis=1)

#medical resources filter
medical_resources = st.selectbox("Medical resources available",["All","Yes","No"])


if selected_governorate != "All":
    filtered_df = filtered_df[filtered_df['Governorate'] == selected_governorate]

if selected_towns != "All":
    filtered_df = filtered_df[filtered_df['Town'] == selected_towns]


if chronic_filter == "Yes":
    filtered_df = filtered_df[filtered_df['has_chronic_disease'] == True]
elif chronic_filter == "No":
    filtered_df = filtered_df[filtered_df['has_chronic_disease'] == False]

if medical_resources == "Yes":
    filtered_df = filtered_df[filtered_df['medical_resources'] == True]
elif medical_resources == "No":
    filtered_df = filtered_df[filtered_df['medical_resources'] == False]

if not filtered_df.empty:
    median_cases = filtered_df['Nb of Covid-19 cases'].median()
    q1 = filtered_df['Nb of Covid-19 cases'].quantile(0.25)
    q3 = filtered_df['Nb of Covid-19 cases'].quantile(0.75)
    st.write("For the selected filters: ",filtered_df.shape[0],"towns")
    st.write(f"Median Covid-19 cases: {median_cases}")
    st.write(f"Q1 = {q1} ; Q2 = {q3} ; IQR = {q3 - q1}")


#make sure when selections are made, color of each governorate stays the same for better readibility
color_map = {
    'South_Governorate':'blue',
    'Akkar_Governorate':'purple',
    'North_Governorate' : 'red',
    'Mount_Lebanon_Governorate' : 'green',
    'Nabatieh_Governorate' : 'orange',
    'Beqaa_Governorate' : 'brown',
    'Baalbek-Hermel_Governorate' : 'gray'
}

#side by side box plots to show the total nbr of covid-19 cases per governorate
fig_2 = px.box(filtered_df,
               x='Governorate',
               y='Nb of Covid-19 cases',
               color="Governorate",
               hover_data = ['Town'],
               color_discrete_map=color_map,
               title='Distribution of COVID-19 Cases by Governorate')
fig_2.update_yaxes(range=[0, 30000])

st.plotly_chart(fig_2)

st.subheader("Interpretation:")
st.write("1- When we play around with the filters, we can see that the median of Covid-19 cases when Chronic Diseases are present is less than when they are absent, which is a little bit surprising. Though this might mean that these people have maybe taken better precautions during Covid-19, unlike the younger generation with no chronic diseases.")
st.write("2- We can also see that the median and IQR are lower when Medical Resources are not available. This might be because, in that case, Covid-19 patients went undocumented due the lack of medical resources available nearby.")


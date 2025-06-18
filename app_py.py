import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Diabetes Dashboard", layout="wide")

# Load data
df = pd.read_csv("diabetes_clean.csv")

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.title("🔎 Filter Data")

age_filter = st.sidebar.multiselect("Age Group:", df["age_group"].unique(), default=df["age_group"].unique())
gender_filter = st.sidebar.multiselect("Gender:", df["gender"].unique(), default=df["gender"].unique())
smoke_filter = st.sidebar.multiselect("Smoking History:", df["smoking_history"].unique(), default=df["smoking_history"].unique())

# Optional comorbidity filters
show_hypertension = st.sidebar.checkbox("Include Hypertension Only", value=False)
show_heart_disease = st.sidebar.checkbox("Include Heart Disease Only", value=False)

# Apply filters
filtered_df = df[
    (df["age_group"].isin(age_filter)) &
    (df["gender"].isin(gender_filter)) &
    (df["smoking_history"].isin(smoke_filter))
]

if show_hypertension:
    filtered_df = filtered_df[filtered_df["hypertension"] == 1]
if show_heart_disease:
    filtered_df = filtered_df[filtered_df["heart_disease"] == 1]

# -------------------------------
# Title and Metrics
# -------------------------------
st.title("🩺 Diabetes Analytics Dashboard")
st.markdown("Analyze diabetes prevalence based on demographic, lifestyle, and health indicators.")

col1, col2, col3 = st.columns(3)
col1.metric("Total Records", len(filtered_df))
col2.metric("Diabetes Cases", int(filtered_df["diabetes"].sum()))
col3.metric("Average HbA1c", round(filtered_df["HbA1c_level"].mean(), 2))

st.markdown("---")

# -------------------------------
# 1. Diabetes by Age Group
# -------------------------------
st.subheader("📊 Diabetes by Age Group")
age_chart = filtered_df.groupby("age_group")["diabetes"].mean().reset_index()
fig1 = px.bar(age_chart, x="age_group", y="diabetes", title="Diabetes Rate (%) by Age Group", labels={"diabetes": "Rate"})
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# 2. Diabetes by Gender
# -------------------------------
st.subheader("👤 Diabetes by Gender")
gender_chart = filtered_df.groupby("gender")["diabetes"].mean().reset_index()
fig2 = px.bar(gender_chart, x="gender", y="diabetes", color="gender", title="Diabetes Rate by Gender", labels={"diabetes": "Rate"})
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# 3. Diabetes by Smoking History
# -------------------------------
st.subheader("🚬 Diabetes by Smoking History")
smoke_chart = filtered_df.groupby("smoking_history")["diabetes"].mean().reset_index()
fig3 = px.bar(smoke_chart, x="smoking_history", y="diabetes", color="smoking_history", title="Diabetes Rate by Smoking History")
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# 4. HbA1c vs Diabetes (Box Plot)
# -------------------------------
st.subheader("🧪 HbA1c Level vs Diabetes")
fig4 = px.box(filtered_df, x="diabetes", y="HbA1c_level", color="diabetes",
              title="HbA1c Levels in Diabetic vs Non-Diabetic",
              labels={"diabetes": "Diabetes (0 = No, 1 = Yes)", "HbA1c_level": "HbA1c Level"})
st.plotly_chart(fig4, use_container_width=True)

# -------------------------------
# 5. Diabetes by Hypertension + Heart Disease
# -------------------------------
st.subheader("❤️ Comorbidity Analysis")
comorbidity = filtered_df.groupby(["hypertension", "heart_disease"])["diabetes"].mean().reset_index()
comorbidity["hypertension"] = comorbidity["hypertension"].replace({0: "No HTN", 1: "HTN"})
comorbidity["heart_disease"] = comorbidity["heart_disease"].replace({0: "No HD", 1: "HD"})
fig5 = px.bar(comorbidity, x="hypertension", y="diabetes", color="heart_disease", barmode="group",
              title="Diabetes Rate by Hypertension & Heart Disease",
              labels={"diabetes": "Diabetes Rate", "hypertension": "Hypertension", "heart_disease": "Heart Disease"})
st.plotly_chart(fig5, use_container_width=True)

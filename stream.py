import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import json

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="PhonePe Case Study Dashboard", layout="wide")

# ------------------ DB CONNECTION ------------------
engine = create_engine(
    "mysql+pymysql://root:Sql25@127.0.0.1:3306/phone_pe",
    pool_pre_ping=True
)

# ------------------ CACHE ------------------
@st.cache_data
def load_data(query):
    return pd.read_sql(query, con=engine)

Agg_Trans = load_data("SELECT * FROM agg_trans")
agg_insurance = load_data("SELECT * FROM agg_insurance")
agg_user = load_data("SELECT * FROM agg_user")

# ------------------ SIDEBAR ------------------
st.sidebar.title("📊 Case Studies")

case_study = st.sidebar.selectbox(
    "Select Case Study",
    [
        "Dashboard",
        "Transaction Dynamics",
        "Device Analysis",
        "Insurance Growth",
        "Market Expansion",
        "User Engagement"
    ]
)

# Filters
states = sorted(Agg_Trans["State"].unique())
years = sorted(Agg_Trans["Year"].unique())

selected_state = st.sidebar.selectbox("State", ["All"] + states)
selected_year = st.sidebar.selectbox("Year", ["All"] + years)

# Apply filters
filtered_trans = Agg_Trans.copy()

if selected_state != "All":
    filtered_trans = filtered_trans[filtered_trans["State"] == selected_state]

if selected_year != "All":
    filtered_trans = filtered_trans[filtered_trans["Year"] == selected_year]

# ------------------ MAP FUNCTION ------------------
def show_map():
    with open("india_states.geojson.json") as f:
        geojson = json.load(f)

    map_data = Agg_Trans.groupby("State")["Transacion_amount"].sum().reset_index()

    state_mapping = {
        "andaman-&-nicobar-islands": "Andaman and Nicobar",
        "andhra-pradesh": "Andhra Pradesh",
        "arunachal-pradesh": "Arunachal Pradesh",
        "assam": "Assam",
        "bihar": "Bihar",
        "chandigarh": "Chandigarh",
        "chhattisgarh": "Chhattisgarh",
        "dadra-&-nagar-haveli-&-daman-&-diu": "Dadra and Nagar Haveli",
        "delhi": "Delhi",
        "goa": "Goa",
        "gujarat": "Gujarat",
        "haryana": "Haryana",
        "himachal-pradesh": "Himachal Pradesh",
        "jammu-&-kashmir": "Jammu and Kashmir",
        "jharkhand": "Jharkhand",
        "karnataka": "Karnataka",
        "kerala": "Kerala",
        "ladakh": "Ladakh",
        "madhya-pradesh": "Madhya Pradesh",
        "maharashtra": "Maharashtra",
        "manipur": "Manipur",
        "meghalaya": "Meghalaya",
        "mizoram": "Mizoram",
        "nagaland": "Nagaland",
        "odisha": "Orissa",
        "puducherry": "Puducherry",
        "punjab": "Punjab",
        "rajasthan": "Rajasthan",
        "sikkim": "Sikkim",
        "tamil-nadu": "Tamil Nadu",
        "telangana": "Telangana",
        "tripura": "Tripura",
        "uttar-pradesh": "Uttar Pradesh",
        "uttarakhand": "Uttaranchal",
        "west-bengal": "West Bengal"
    }

    map_data["State"] = map_data["State"].map(state_mapping)
    map_data = map_data.dropna()

    fig = px.choropleth(
        map_data,
        geojson=geojson,
        locations="State",
        featureidkey="properties.NAME_1",
        color="Transacion_amount",
        title="India Transaction Map"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)
# ------------------ DASHBOARD ------------------
if case_study == "Dashboard":

    st.title("📱 PhonePe Insights Dashboard")
    st.markdown("### Real-time Analytics of Transactions, Insurance & Users")

    # KPI Metrics
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Total Transactions",
        f"₹ {int(Agg_Trans['Transacion_amount'].sum()):,}"
    )

    col2.metric(
        "🛡️ Total Insurance",
        f"₹ {int(agg_insurance['Insurance_amount'].sum()):,}"
    )

    col3.metric(
        "👥 Total Users",
        f"{int(agg_user['User_count'].sum()):,}"
    )

    st.markdown("---")

# ------------------ CASE STUDY 1 ------------------
elif case_study == "Transaction Dynamics":
    st.title("📊 Case Study 1: Transaction Dynamics")

    df = filtered_trans.groupby("State")["Transacion_amount"].sum().reset_index()

    st.metric("Total Transactions", int(df["Transacion_amount"].sum()))

    fig = px.bar(df, x="State", y="Transacion_amount")
    st.plotly_chart(fig, use_container_width=True)

    show_map()

    st.subheader("🔍 Insights")
    st.write("""
    - Transactions are concentrated in a few major states
    - Digital adoption varies across regions
    """)

    st.subheader("💡 Recommendations")
    st.write("""
    - Expand services in low-performing states
    - Promote digital awareness campaigns
    """)

# ------------------ CASE STUDY 2 ------------------
elif case_study == "Device Analysis":
    st.title("📱 Case Study 2: Device Analysis")

    df = agg_user.groupby("User_brand")["User_count"].sum().reset_index()

    st.metric("Total Users", int(df["User_count"].sum()))

    fig = px.pie(df, names="User_brand", values="User_count")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔍 Insights")
    st.write("""
    - Few brands dominate user base
    - Engagement differs across devices
    """)

    st.subheader("💡 Recommendations")
    st.write("""
    - Optimize app for all devices
    - Focus on high-engagement brands
    """)

# ------------------ CASE STUDY 3 ------------------
elif case_study == "Insurance Growth":
    st.title("🛡️ Case Study 3: Insurance Growth")

    df = agg_insurance.groupby("State")["Insurance_amount"].sum().reset_index()

    st.metric("Total Insurance", int(df["Insurance_amount"].sum()))

    fig = px.bar(df, x="State", y="Insurance_amount")
    st.plotly_chart(fig, use_container_width=True)

    show_map()

    st.subheader("🔍 Insights")
    st.write("""
    - Insurance adoption is limited
    - Few states drive most transactions
    """)

    st.subheader("💡 Recommendations")
    st.write("""
    - Increase awareness programs
    - Partner with insurance providers
    """)

# ------------------ CASE STUDY 4 ------------------
elif case_study == "Market Expansion":
    st.title("🌍 Case Study 4: Market Expansion")

    df = filtered_trans.groupby("State")["Transacion_amount"].sum().reset_index()
    df = df.sort_values(by="Transacion_amount", ascending=False).head(10)

    fig = px.bar(df, x="State", y="Transacion_amount")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔍 Insights")
    st.write("""
    - Revenue is concentrated in top states
    - Mid-tier states show growth potential
    """)

    st.subheader("💡 Recommendations")
    st.write("""
    - Expand into emerging states
    - Strengthen merchant ecosystem
    """)

# ------------------ CASE STUDY 5 ------------------
elif case_study == "User Engagement":
    st.title("👥 Case Study 5: User Engagement")

    df = agg_user.groupby("State")["User_count"].sum().reset_index()

    st.metric("Total Users", int(df["User_count"].sum()))

    fig = px.bar(df, x="State", y="User_count")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔍 Insights")
    st.write("""
    - User growth varies across states
    - High population states dominate
    """)

    st.subheader("💡 Recommendations")
    st.write("""
    - Improve onboarding experience
    - Focus on user retention strategies
    """)

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("📌PhonePe Case Study Dashboard")
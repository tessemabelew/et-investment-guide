import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse

# PostgreSQL Connection Function
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="investment_guide",
        user="postgres",
        password="Saba123@"
    )

# Load Opportunities from DB
def load_opportunities():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT o.title, r.name AS region, s.name AS sector, o.investment_value_usd, o.expected_roi_percent, o.status
        FROM opportunity o
        JOIN region r ON o.region_id = r.region_id
        JOIN sector s ON o.sector_id = s.sector_id
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return pd.DataFrame(data)

# Insert New Opportunity
def add_opportunity(title, region_id, sector_id, type_id, value, roi, status, person, email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO opportunity (title, region_id, sector_id, type_id, investment_value_usd, expected_roi_percent, status, contact_person, contact_email)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (title, region_id, sector_id, type_id, value, roi, status, person, email))
    conn.commit()
    cur.close()
    conn.close()

# UI Layout
st.title("Investment Guide - XYZ Region")

st.subheader("Available Investment Opportunities")

# Load and display opportunities
df = load_opportunities()
st.dataframe(df)

st.subheader("➕ Add New Investment Opportunity")

# Form to add new opportunity
with st.form("add_opportunity_form"):
    title = st.text_input("Opportunity Title")
    region_id = st.text_input("Region ID")
    sector_id = st.text_input("Sector ID")
    type_id = st.text_input("Type ID")
    value = st.number_input("Investment Value (USD)", min_value=0.0)
    roi = st.number_input("Expected ROI (%)", min_value=0.0)
    status = st.selectbox("Status", ["Available", "In Progress", "Completed"])
    person = st.text_input("Contact Person")
    email = st.text_input("Contact Email")
    
    submitted = st.form_submit_button("Add Opportunity")
    if submitted:
        add_opportunity(title, region_id, sector_id, type_id, value, roi, status, person, email)
        st.success("✅ Opportunity added successfully!")



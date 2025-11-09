import streamlit as st
import requests
from datetime import datetime
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def analytics_tab():
    col1, col2 = st.columns(2)
    with col1:
        start = st.date_input("Start date:", value=datetime(2024, 8, 1))
    with col2:
        end = st.date_input("End date:", value=datetime(2024, 8, 5))

    if st.button("Get Analytics"):

        payload = {
            "start_date": str(start),
            "end_date": str(end)
        }

        response = requests.post(f"{API_URL}/analytics", json=payload)

        if response.status_code == 200:
            summary = response.json()
        else:
            st.error("Failed to retrieve summary.")

        df = pd.DataFrame(summary)
        df = df.T.reset_index()
        df.columns = ["Category", "Total", "Percentage"]
        df_sorted = df.sort_values("Percentage", ascending=False, ignore_index=True)

        st.title("Expense Breakdown By Category")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.bar_chart(data=df_sorted, x="Category", y="Percentage")

        df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
        df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)
        st.table(df_sorted)
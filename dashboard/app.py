import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="IntelliStream Dashboard",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 IntelliStream Dashboard")

API_URL = "http://api:8000"

# --------------------
# Stats
# --------------------

try:
    stats = requests.get(
        f"{API_URL}/stats",
        timeout=5
    ).json()

    st.subheader("System Statistics")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Events",
        stats["total_events"]
    )

    col2.metric(
        "High Risk",
        stats["high_risk_events"]
    )

    col3.metric(
        "Normal",
        stats["normal_events"]
    )

except Exception as e:
    st.error(f"Cannot connect to API: {e}")
    st.stop()

# --------------------
# Latest Events
# --------------------

st.subheader("Latest Events")

try:
    events = requests.get(
        f"{API_URL}/latest",
        timeout=5
    ).json()

    df = pd.DataFrame(events)

    if not df.empty:

        st.dataframe(
            df,
            use_container_width=True
        )

        st.subheader("Risk Distribution")

        st.bar_chart(
            df["risk_level"].value_counts()
        )

        st.subheader("Temperature Trend")

        st.line_chart(
            df["temperature"]
        )

        st.subheader("Heart Rate Trend")

        st.line_chart(
            df["heart_rate"]
        )

    else:
        st.warning("No events found.")

except Exception as e:
    st.error(f"Failed to fetch events: {e}")

# --------------------
# Animal History
# --------------------

st.subheader("Animal History")

animal_id = st.number_input(
    "Enter Animal ID",
    min_value=1,
    step=1
)

if st.button("Search"):

    try:

        history = requests.get(
            f"{API_URL}/animal/{animal_id}",
            timeout=5
        ).json()

        if history:
            st.dataframe(
                pd.DataFrame(history),
                use_container_width=True
            )
        else:
            st.warning("No records found.")

    except Exception as e:
        st.error(f"Failed to fetch animal history: {e}")

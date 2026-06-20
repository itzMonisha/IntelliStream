from streamlit_autorefresh import st_autorefresh
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

count = st_autorefresh(interval=5000, key="refresh")

st.write("Refresh Count:", count)

st_autorefresh(
    interval=5000,
    key="refresh"
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="IntelliStream Dashboard",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 IntelliStream Dashboard")

API_URL = "http://localhost:8000"

# --------------------------------------------------
# ANALYTICS
# --------------------------------------------------

try:

    response = requests.get(
        f"{API_URL}/analytics",
        timeout=5
    )

    if response.status_code != 200:
        st.error("Analytics endpoint failed")
        st.stop()

    analytics = response.json()

    st.subheader("📊 System Analytics")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "📦 Total Events",
        analytics.get("total_events", 0)
    )

    col2.metric(
        "🐄 Total Animals",
        analytics.get("total_animals", 0)
    )

    col3.metric(
        "🌡 Avg Temperature",
        analytics.get("avg_temperature", 0)
    )

    col4.metric(
        "❤️ Avg Heart Rate",
        analytics.get("avg_heart_rate", 0)
    )

    col5.metric(
        "⚠ High Risk %",
        f"{analytics.get('high_risk_percent', 0)}%"
    )

except Exception as e:

    st.error(
        f"Analytics API Error: {e}"
    )

    st.stop()
# --------------------------------------------------
# LATEST EVENTS
# --------------------------------------------------

st.subheader("📋 Latest Events")

try:

    events = requests.get(
        f"{API_URL}/latest",
        timeout=5
    ).json()

    df = pd.DataFrame(events)

    st.dataframe(
        df,
        use_container_width=True
    )

except Exception as e:

    st.error(
        f"Failed to fetch latest events: {e}"
    )

    st.stop()

# --------------------------------------------------
# CHARTS
# --------------------------------------------------

col_left, col_right = st.columns(2)

# --------------------------------------------------
# PIE CHART
# --------------------------------------------------

with col_left:

    st.subheader("🥧 Risk Distribution")

    risk_counts = (
        df["risk_level"]
        .value_counts()
        .reset_index()
    )

    risk_counts.columns = [
        "risk_level",
        "count"
    ]

    fig_pie = px.pie(
        risk_counts,
        names="risk_level",
        values="count",
        hole=0.4,
        title="Risk Level Distribution"
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

# --------------------------------------------------
# BAR CHART
# --------------------------------------------------

with col_right:

    st.subheader("📊 Risk Count")

    fig_bar = px.bar(
        risk_counts,
        x="risk_level",
        y="count",
        title="Risk Categories"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

# --------------------------------------------------
# TEMPERATURE TREND
# --------------------------------------------------

st.subheader("🌡 Temperature Trend")

fig_temp = px.line(
    df,
    x="id",
    y="temperature",
    markers=True,
    title="Temperature Trend"
)

st.plotly_chart(
    fig_temp,
    use_container_width=True
)

# --------------------------------------------------
# HEART RATE TREND
# --------------------------------------------------

st.subheader("❤️ Heart Rate Trend")

fig_hr = px.line(
    df,
    x="id",
    y="heart_rate",
    markers=True,
    title="Heart Rate Trend"
)

st.plotly_chart(
    fig_hr,
    use_container_width=True
)

# --------------------------------------------------
# HIGH RISK ANIMALS
# --------------------------------------------------

st.subheader("🚨 High Risk Animals")

high_df = df[
    df["risk_level"] == "HIGH"
]

if len(high_df) > 0:

    st.dataframe(
        high_df,
        use_container_width=True
    )

else:

    st.success(
        "No high-risk animals found."
    )

# --------------------------------------------------
# ANIMAL SEARCH
# --------------------------------------------------

st.subheader("🔍 Animal History")

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

        history_df = pd.DataFrame(
            history
        )

        if len(history_df) > 0:

            st.dataframe(
                history_df,
                use_container_width=True
            )

        else:

            st.warning(
                "No records found."
            )

    except Exception as e:

        st.error(
            f"Search failed: {e}"
        )

# --------------------------------------------------
# DOWNLOAD CSV
# --------------------------------------------------

st.subheader("⬇ Export Data")

csv = df.to_csv(
    index=False
)

st.download_button(
    label="Download Events CSV",
    data=csv,
    file_name="events.csv",
    mime="text/csv"
)

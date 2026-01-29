import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Bundle Dashboard", layout="wide")
st.title("📊 Bundle Performance Dashboard")
st.markdown("Upload the Excel file shared via OneDrive to view interactive charts")

uploaded_file = st.file_uploader(
    "Upload Book1_20260129.xlsx",
    type=['xlsx', 'xls'],
    help="Download the file from the OneDrive link shared with you, then upload here"
)

if uploaded_file is None:
    st.info("👆 Upload the Excel file to see charts")
    st.stop()

try:
    df = pd.read_excel(uploaded_file, na_values=['#N/A', 'NA', '#VALUE!', '#DIV/0!'])
except Exception as e:
    st.error(f"Error reading file: {e}")
    st.stop()

# Clean data
df = df.dropna(subset=['Bundle Name', 'MSISDN']).copy()
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
df['Data_MBs'] = pd.to_numeric(df['Data_MBs'], errors='coerce')

# CHART 1: Revenue vs Subscribers
st.subheader("Chart 1: Revenue vs Subscriber Count")
df1 = df.dropna(subset=['Revenue']).copy()
if len(df1) > 0:
    chart1 = df1.groupby('Bundle Name').agg(
        msisdn_count=('MSISDN', 'count'),
        total_revenue=('Revenue', 'sum'),
        avg_revenue=('Revenue', 'mean')
    ).reset_index()
    chart1 = chart1.sort_values('total_revenue', ascending=False)
    
    fig1 = px.scatter(
        chart1,
        x='Bundle Name',
        y='total_revenue',
        size='msisdn_count',
        color='avg_revenue',
        hover_data={'msisdn_count': True, 'total_revenue': ':,.0f', 'avg_revenue': ':,.2f'},
        title='Revenue vs Subscriber Count',
        labels={'total_revenue': 'Total Revenue', 'msisdn_count': 'Subscriber Count'},
        size_max=70,
        color_continuous_scale='Viridis'
    )
    fig1.update_layout(height=600, template='plotly_white')
    fig1.update_xaxes(tickangle=45)
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("No valid revenue data found")

# CHART 2: Revenue vs Data Volume (EXCLUDES NA Data Volume)
st.subheader("Chart 2: Revenue vs Data Volume (NA Data Volume Excluded)")
df2 = df.dropna(subset=['Revenue', 'Data_MBs']).copy()  # CRITICAL: Excludes NA Data Volume
if len(df2) > 0:
    chart2 = df2.groupby('Bundle Name').agg(
        msisdn_count=('MSISDN', 'count'),
        total_revenue=('Revenue', 'sum'),
        avg_revenue=('Revenue', 'mean'),
        total_data_mb=('Data_MBs', 'sum')
    ).reset_index()
    chart2 = chart2.sort_values('total_revenue', ascending=False)
    
    fig2 = px.scatter(
        chart2,
        x='Bundle Name',
        y='total_revenue',
        size='total_data_mb',
        color='avg_revenue',
        hover_data={'msisdn_count': True, 'total_revenue': ':,.0f', 'avg_revenue': ':,.2f', 'total_data_mb': ':,.0f'},
        title='Revenue vs Data Volume',
        labels={'total_revenue': 'Total Revenue', 'total_data_mb': 'Total Data Volume (MB)'},
        size_max=70,
        color_continuous_scale='Plasma'
    )
    fig2.update_layout(height=600, template='plotly_white')
    fig2.update_xaxes(tickangle=45)
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("No valid data volume records found (all NA?)")

st.markdown("---")
st.caption("✅ Hover over bubbles to see details | Data processed in-browser (not stored)")

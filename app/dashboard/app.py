import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page config
st.set_page_config(page_title="Invoice Extractor", layout="wide")

# Title
st.title("AI Invoice & Receipt Extractor")
st.markdown("Upload invoices and receipts to extract structured data")

# API endpoint
API_BASE = "http://localhost:8000"

# Sidebar for upload
with st.sidebar:
    st.header("Upload Invoice")
    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # Display file details
        st.write("File details:", uploaded_file.name, uploaded_file.type)
        
        # Upload to API
        if st.button("Process Invoice"):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            response = requests.post(f"{API_BASE}/upload-invoice", files=files)
            
            if response.status_code == 200:
                result = response.json()
                st.success("Invoice processed successfully!")
                
                # Display extracted data
                st.subheader("Extracted Data")
                data = result['data']
                st.json(data)
            else:
                st.error(f"Error processing invoice: {response.text}")

# Main content area
tab1, tab2, tab3 = st.tabs(["Dashboard", "Invoices", "Analytics"])

with tab1:
    st.header("Recent Invoices")
    
    try:
        # Fetch invoices from API
        response = requests.get(f"{API_BASE}/invoices?limit=10")
        if response.status_code == 200:
            invoices = response.json()
            
            if invoices:
                df = pd.DataFrame(invoices)
                st.dataframe(df[['id', 'vendor', 'amount', 'category', 'invoice_date', 'processed_at']])
            else:
                st.info("No invoices processed yet. Upload one to get started!")
        else:
            st.error("Could not fetch invoices from server")
    except:
        st.error("Could not connect to the API server. Make sure it's running on localhost:8000")

with tab2:
    st.header("All Invoices")
    
    try:
        # Fetch all invoices from API
        response = requests.get(f"{API_BASE}/invoices?limit=100")
        if response.status_code == 200:
            invoices = response.json()
            
            if invoices:
                df = pd.DataFrame(invoices)
                
                # Filters
                col1, col2 = st.columns(2)
                with col1:
                    vendors = ['All'] + list(df['vendor'].unique())
                    selected_vendor = st.selectbox("Filter by Vendor", vendors)
                
                with col2:
                    categories = ['All'] + list(df['category'].unique())
                    selected_category = st.selectbox("Filter by Category", categories)
                
                # Apply filters
                if selected_vendor != 'All':
                    df = df[df['vendor'] == selected_vendor]
                if selected_category != 'All':
                    df = df[df['category'] == selected_category]
                
                st.dataframe(df)
            else:
                st.info("No invoices found")
        else:
            st.error("Could not fetch invoices from server")
    except:
        st.error("Could not connect to the API server")

with tab3:
    st.header("Spending Analytics")
    
    try:
        # Fetch invoices for analytics
        response = requests.get(f"{API_BASE}/invoices?limit=1000")
        if response.status_code == 200:
            invoices = response.json()
            
            if invoices:
                df = pd.DataFrame(invoices)
                
                # Convert date column
                df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
                df = df.dropna(subset=['invoice_date', 'amount'])
                
                # Monthly spending trend
                st.subheader("Monthly Spending Trend")
                df_monthly = df.set_index('invoice_date').resample('M').sum(numeric_only=True).reset_index()
                fig = px.line(df_monthly, x='invoice_date', y='amount', title='Monthly Spending')
                st.plotly_chart(fig, use_container_width=True)
                
                # Category distribution
                st.subheader("Spending by Category")
                category_totals = df.groupby('category')['amount'].sum().reset_index()
                fig2 = px.pie(category_totals, values='amount', names='category', title='Spending by Category')
                st.plotly_chart(fig2, use_container_width=True)
                
            else:
                st.info("Not enough data for analytics yet")
        else:
            st.error("Could not fetch invoices for analytics")
    except Exception as e:
        st.error(f"Error generating analytics: {str(e)}")
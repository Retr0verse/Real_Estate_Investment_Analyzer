import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Real Estate Investment Tool", layout="centered")

st.title("🏡 Real Estate Investment Analyzer")
st.subheader("Calculate ROI and Cap Rate on Investment Properties")

# Sidebar Inputs
st.sidebar.header("Enter Property Details")

property_name = st.sidebar.text_input("Property Name", "Example Property")
purchase_price = st.sidebar.number_input("Purchase Price ($)", value=250000)
monthly_rent = st.sidebar.number_input("Monthly Rent ($)", value=1800)
monthly_expenses = st.sidebar.number_input("Monthly Expenses ($)", value=600)

if st.sidebar.button("Add Property"):
    if "properties" not in st.session_state:
        st.session_state.properties = []

    st.session_state.properties.append({
        "Property Name": property_name,
        "Purchase Price": purchase_price,
        "Monthly Rent": monthly_rent,
        "Monthly Expenses": monthly_expenses
    })

# Show Table if Properties Exist
if "properties" in st.session_state and st.session_state.properties:
    df = pd.DataFrame(st.session_state.properties)
    df['Annual Rent'] = df['Monthly Rent'] * 12
    df['Annual Expenses'] = df['Monthly Expenses'] * 12
    df['Net Income'] = df['Annual Rent'] - df['Annual Expenses']
    df['Cap Rate (%)'] = round((df['Net Income'] / df['Purchase Price']) * 100, 2)
    df['ROI (%)'] = round((df['Net Income'] / (0.2 * df['Purchase Price'])) * 100, 2)

    st.write("### 📊 Property Investment Summary")
    st.dataframe(df)

    # Plot ROI vs Cap Rate
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['Property Name'],
        y=df['Cap Rate (%)'],
        name='Cap Rate (%)',
        marker_color='mediumseagreen'
    ))
    fig.add_trace(go.Bar(
        x=df['Property Name'],
        y=df['ROI (%)'],
        name='ROI (%)',
        marker_color='steelblue'
    ))
    fig.update_layout(
        title='Cap Rate vs ROI',
        xaxis_title='Property',
        yaxis_title='Percentage',
        barmode='group',
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)

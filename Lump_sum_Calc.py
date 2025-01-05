import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def sip_calculator_with_lump_sum(lump_sum, monthly_contribution, annual_rate, total_years, stop_contribution_years):
    r = annual_rate / 100
    n = 12
    total_months = total_years * 12
    sip_stop_months = stop_contribution_years * 12
    current_value = lump_sum
    total_invested = lump_sum
    growth = []

    for month in range(1, total_months + 1):
        if month <= sip_stop_months:
            current_value = current_value * (1 + r / n) + monthly_contribution
            total_invested += monthly_contribution
        else:
            current_value *= (1 + r / n)
        if month % 12 == 0 or month == total_months:
            growth.append((month / 12, current_value))
    
    profit = current_value - total_invested
    return current_value, total_invested, profit, pd.DataFrame(growth, columns=["Year", "Investment Value"])

# Streamlit App
st.set_page_config(page_title="Enhanced SIP & Lump Sum Calculator", layout="wide")
st.title("📈 Enhanced SIP & Lump Sum Investment Calculator")

# Sidebar Inputs
with st.sidebar:
    st.header("Input Parameters")
    lump_sum = st.number_input("💵 Lump Sum Investment", value=10000.0, min_value=0.0, max_value=1_000_000_000.0, step=1000.0)
    monthly_contribution = st.number_input("📅 Monthly Contribution", value=500.0, min_value=0.0, max_value=10_000_000.0, step=100.0)
    annual_rate = st.slider("📊 Annual Interest Rate (%)", min_value=0.0, max_value=50.0, value=10.0, step=0.1)
    total_years = st.slider("⏳ Total Investment Period (Years)", min_value=1, max_value=100, value=10)
    stop_contribution_years = st.slider("🛑 SIP Stops After (Years)", min_value=0, max_value=total_years, value=5)
    currency_code = st.selectbox("💱 Select Currency", options=["USD", "INR", "EUR", "GBP", "JPY"], index=0)

# Currency Symbols
currency_symbols = {'USD': '$', 'INR': '₹', 'EUR': '€', 'GBP': '£', 'JPY': '¥'}
currency_symbol = currency_symbols.get(currency_code, '$')

# Run Calculation
if st.button("Calculate"):
    # Combined SIP and Lump Sum Calculation
    final_value, total_invested, profit, sip_growth = sip_calculator_with_lump_sum(
        lump_sum, monthly_contribution, annual_rate, total_years, stop_contribution_years
    )

    # Results
    st.subheader("Results")
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Value", f"{currency_symbol}{final_value:,.2f}")
    col2.metric("📈 Total Invested", f"{currency_symbol}{total_invested:,.2f}")
    col3.metric("💸 Profit", f"{currency_symbol}{profit:,.2f}")

    # Pie Chart for Summary
    st.subheader("Investment Summary")
    pie_labels = ["Invested Amount", "Profit"]
    pie_values = [total_invested, profit]
    fig_pie, ax_pie = plt.subplots(figsize=(2, 2))  # Reduced size
    ax_pie.pie(pie_values, labels=pie_labels, autopct='%1.1f%%', startangle=90)
    ax_pie.set_title("Investment Distribution")
    st.pyplot(fig_pie)

    # Growth Chart
    st.subheader("Growth Over Time")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(sip_growth["Year"], sip_growth["Investment Value"], label="SIP + Lump Sum Growth", marker='x')
    ax.set_xlabel("Years")
    ax.set_ylabel(f"Value ({currency_code})")
    ax.set_title("Investment Growth")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Data Tables
    st.subheader("Yearly Investment Details")
    st.dataframe(sip_growth)

# Footer
st.markdown("---")
st.markdown("Developed with ❤️ using [Streamlit](https://streamlit.io)")

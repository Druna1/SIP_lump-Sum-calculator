import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# SIP Calculator Function
def sip_calculator(lump_sum, monthly_contribution, annual_rate, total_years, stop_contribution_years):
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

# Streamlit App UI
st.set_page_config(page_title="SIP & Lump Sum Calculator", layout="wide")
st.title("📈 SIP & Lump Sum Investment Calculator")

# Sidebar Inputs
with st.sidebar:
    st.header("Input Parameters")
    lump_sum = st.number_input("💵 Lump Sum Investment", value=10000.0, min_value=0.0)
    monthly_contribution = st.number_input("📅 Monthly Contribution", value=500.0, min_value=0.0)
    annual_rate = st.slider("📊 Annual Interest Rate (%)", min_value=0.0, max_value=20.0, value=10.0, step=0.1)
    total_years = st.slider("⏳ Total Investment Period (Years)", min_value=1, max_value=30, value=10)
    stop_contribution_years = st.slider("🛑 SIP Stops After (Years)", min_value=0, max_value=total_years, value=5)
    currency_code = st.selectbox("💱 Select Currency", options=["USD", "INR", "EUR", "GBP", "JPY"], index=0)

# Currency Symbols
currency_symbols = {'USD': '$', 'INR': '₹', 'EUR': '€', 'GBP': '£', 'JPY': '¥'}
currency_symbol = currency_symbols.get(currency_code, '$')

# Run Calculation
if st.button("Calculate"):
    final_value, total_invested, profit, growth_df = sip_calculator(
        lump_sum, monthly_contribution, annual_rate, total_years, stop_contribution_years
    )

    # Results
    st.subheader("Results")
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Value", f"{currency_symbol}{final_value:,.2f}")
    col2.metric("📈 Total Invested", f"{currency_symbol}{total_invested:,.2f}")
    col3.metric("💸 Profit", f"{currency_symbol}{profit:,.2f}")

    # Graph
    st.subheader("Investment Growth Over Time")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(growth_df["Year"], growth_df["Investment Value"], label="Investment Value", marker='o')
    ax.set_xlabel("Years")
    ax.set_ylabel(f"Investment Value ({currency_code})")
    ax.set_title("Growth of Investment Over Time")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Data Table
    st.subheader("Yearly Investment Details")
    st.dataframe(growth_df)

# Footer
st.markdown("---")
st.markdown("Developed with ❤️ using [Streamlit](https://streamlit.io)")

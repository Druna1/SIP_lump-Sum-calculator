import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

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
st.title("📊 SIP & Lump Sum Investment Calculator")

# Sidebar Inputs
with st.sidebar:
    st.header("🎯 Input Parameters")
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
if st.button("📈 Calculate Investment"):
    # Combined SIP and Lump Sum Calculation
    final_value, total_invested, profit, sip_growth = sip_calculator_with_lump_sum(
        lump_sum, monthly_contribution, annual_rate, total_years, stop_contribution_years
    )

    # Results
    st.subheader("📋 Results Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Value", f"{currency_symbol}{final_value:,.2f}")
    col2.metric("📈 Total Invested", f"{currency_symbol}{total_invested:,.2f}")
    col3.metric("💸 Profit", f"{currency_symbol}{profit:,.2f}")

    # Visualizations
    st.subheader("📊 Visualizations")

    # Pie Chart
    st.markdown("### 💡 Investment Distribution")
    pie_labels = ["Invested Amount", "Profit"]
    pie_values = [total_invested, profit]
    colors = ['#4CAF50', '#FF9800']  # Professional colors

    fig_pie, ax_pie = plt.subplots(figsize=(2.5, 2.5))  # Further reduced size
    wedges, texts, autotexts = ax_pie.pie(
        pie_values, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=colors, 
        textprops={'fontsize': 8}
    )
    ax_pie.legend(
        wedges, 
        pie_labels, 
        title="Legend", 
        loc="center left", 
        bbox_to_anchor=(1, 0, 0.5, 1), 
        fontsize=8
    )
    ax_pie.set_title("Investment Breakdown", fontsize=10, pad=20)
    st.pyplot(fig_pie)

    # Growth Chart
    st.markdown("### 📈 Growth Over Time")
    fig, ax = plt.subplots(figsize=(4, 2.5))  # Further reduced graph size

    # Plot the investment growth
    ax.plot(sip_growth["Year"], sip_growth["Investment Value"], label="Investment Value", marker='o', color="#2ca02c")

    # Format Y-axis with currency symbols
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{currency_symbol}{x:,.0f}"))

    ax.set_xlabel("Years", fontsize=8)
    ax.set_ylabel(f"Value ({currency_code})", fontsize=8)
    ax.set_title("Investment Growth", fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=8)
    st.pyplot(fig)

    # Add Columns for Invested Amount, Profit, Total Value, and Profit %
    sip_growth["Invested Amount"] = sip_growth["Year"] * monthly_contribution * 12 + lump_sum
    sip_growth["Profit"] = sip_growth["Investment Value"] - sip_growth["Invested Amount"]
    sip_growth["Total Value"] = sip_growth["Investment Value"]
    sip_growth["Profit %"] = (sip_growth["Profit"] / sip_growth["Invested Amount"]) * 100

    # Display the table
    st.subheader("📅 Yearly Investment Details")
    st.dataframe(
        sip_growth[["Year", "Invested Amount", "Profit", "Total Value", "Profit %"]].style.format(
            {
                "Year": "{:.0f}",
                "Invested Amount": lambda x: f"{currency_symbol}{x:,.2f}",
                "Profit": lambda x: f"{currency_symbol}{x:,.2f}",
                "Total Value": lambda x: f"{currency_symbol}{x:,.2f}",
                "Profit %": "{:.2f}%",
            }
        )
    )

# Footer
st.markdown("---")
st.markdown("Developed with ❤️ using [Streamlit](https://streamlit.io)")

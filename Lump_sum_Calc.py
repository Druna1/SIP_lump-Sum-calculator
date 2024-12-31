import matplotlib.pyplot as plt

def sip_calculator_with_graph(
    lump_sum,
    monthly_contribution,
    annual_rate,
    total_years,
    stop_contribution_years,
    currency_code='USD'
):
    currency_symbols = {
        'USD': '$',
        'INR': '₹',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
    }
    currency_symbol = currency_symbols.get(currency_code.upper(), '$')
    r = annual_rate / 100
    n = 12
    total_months = total_years * 12
    sip_stop_months = stop_contribution_years * 12

    # Precompute common factor
    monthly_rate = 1 + r / n
    months = []
    values = []

    # Initialize values
    current_value = lump_sum
    total_invested = lump_sum
    months.append(0)
    values.append(current_value)

    # Efficient compounding using formula
    for month in range(1, total_months + 1):
        if month <= sip_stop_months:
            current_value = current_value * monthly_rate + monthly_contribution
            total_invested += monthly_contribution
        else:
            current_value *= monthly_rate

        if month % 12 == 0 or month == total_months:
            months.append(month)
            values.append(current_value)

    final_value = current_value
    profit = final_value - total_invested

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.plot(months, values, label='Investment Value', marker='o')
    plt.xlabel('Months')
    plt.ylabel('Investment Value')
    plt.title('Growth of Investment Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

    print(f"Total Amount  = {currency_symbol}{final_value:,.2f}")
    print(f"Invested      = {currency_symbol}{total_invested:,.2f}")
    print(f"Profit        = {currency_symbol}{profit:,.2f}")

    return final_value

# Example Usage
lump_sum = float(input("Enter Lump Sum Investment (e.g., 10000): "))
monthly_contribution = float(input("Enter Monthly Contribution (e.g., 500): "))
annual_rate = float(input("Enter Annual Interest Rate in % (e.g., 10): "))
total_years = int(input("Enter Total Investment Period in Years (e.g., 10): "))
stop_contribution_years = int(input("Enter Years after which SIP stops (e.g., 5): "))
currency_code = input("Enter Currency Code (default is USD): ")

future_value = sip_calculator_with_graph(
    lump_sum,
    monthly_contribution,
    annual_rate,
    total_years,
    stop_contribution_years,
    currency_code=currency_code
)
print(f"\nReturned Future Value: {future_value:,.2f}")

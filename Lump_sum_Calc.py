import matplotlib.pyplot as plt
def sip_calculator_with_graph(
    lump_sum,
    monthly_contribution,
    annual_rate,
    total_years,
    stop_contribution_years,
    currency_code='USD'
):
    """
    Calculates the future value of an investment with:
    - An initial lump sum
    - Monthly contributions (SIP) that stop after a defined number of years
    - Displays a plot of the investment value over time
    and prints:
      * Total Amount (final value)
      * Invested (total contributions)
      * Profit (final value - total contributions)
      * All amounts are displayed with the selected currency symbol.
    Parameters:
    lump_sum (float)                : Initial lump sum investment
    monthly_contribution (float)    : Monthly SIP contribution
    annual_rate (float)             : Annual interest rate (as a percentage)
    total_years (int)               : Total investment period in years
    stop_contribution_years (int)   : Number of years after which monthly contributions stop
    currency_code (str)             : Currency code for display (e.g., 'USD', 'INR', 'EUR')
    Returns:
    float : The final investment value
    """
    # Map currency codes to symbols.
    # Add or modify as needed for your use case.
    currency_symbols = {
        'USD': '$',
        'INR': '₹',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        # Add more codes/symbols if needed
    }
    
    # Use the matching symbol if it exists; default to '$' if not found
    currency_symbol = currency_symbols.get(currency_code.upper(), '$')
    
    # Convert annual percentage rate to a decimal
    r = annual_rate / 100
    # Compounding frequency (monthly)
    n = 12
    # Total months in the investment period
    total_months = total_years * 12
    # Lists to store values for plotting
    months = []
    total_investment_values = []
    # Initial investment value
    current_value = lump_sum
    months.append(0)
    total_investment_values.append(current_value)
    # Track total amount invested (lump sum + monthly contributions)
    total_invested = lump_sum
    # Calculate the value for each month
    for month in range(1, total_months + 1):
        if month <= stop_contribution_years * 12:
            # Add monthly contribution within the SIP period
            current_value = current_value * (1 + r / n) + monthly_contribution
            total_invested += monthly_contribution
        else:
            # No monthly contribution after stop_contribution_years
            current_value = current_value * (1 + r / n)
        
        # Store data for plotting
        months.append(month)
        total_investment_values.append(current_value)
    # Final value of the investment
    final_value = total_investment_values[-1]
    # Profit calculation
    profit = final_value - total_invested
    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.plot(months, total_investment_values, label='Total Investment Value')
    plt.xlabel('Months')
    plt.ylabel('Investment Value')
    plt.title('Growth of Investment Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()
    # Print the results with currency formatting
    print(f"Total Amount  = {currency_symbol}{final_value:,.2f}")
    print(f"Invested      = {currency_symbol}{total_invested:,.2f}")
    print(f"Profit        = {currency_symbol}{profit:,.2f}")
    return final_value

# -------------------------------------
# Example usage (In Google Colab or Replit)
# -------------------------------------
# 1. Prompt for parameters
lump_sum = float(input("Enter Lump Sum Investment (e.g., 10000): "))
monthly_contribution = float(input("Enter Monthly Contribution (e.g., 500): "))
annual_rate = float(input("Enter Annual Interest Rate in % (e.g., 10): "))
total_years = int(input("Enter Total Investment Period in Years (e.g., 10): "))
stop_contribution_years = int(input("Enter Years after which SIP stops (e.g., 5): "))
# 2. Prompt for currency choice
print("\nSupported currency codes: USD, INR, EUR, GBP, JPY")
currency_code = input("Enter Currency Code (default is USD if not recognized): ")
# 3. Run the calculator
future_value = sip_calculator_with_graph(
    lump_sum,
    monthly_contribution,
    annual_rate,
    total_years,
    stop_contribution_years,
    currency_code=currency_code
)
print(f"\nReturned Future Value: {future_value:,.2f}")

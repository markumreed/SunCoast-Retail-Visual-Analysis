
# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Welcome message
print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Create a seed for reproducibility
np.random.seed(42)

# Generate dates for 8 quarters (Q1 2022 - Q4 2023)
quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022',
                 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

# Store locations
locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']

# Product categories
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

# Generate quarterly sales data for each location and category
quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            # Base sales with seasonal pattern (Q4 higher, Q1 lower)
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.0
            if quarter.quarter == 4:  # Q4 (holiday boost)
                seasonal_factor = 1.3
            elif quarter.quarter == 1:  # Q1 (post-holiday dip)
                seasonal_factor = 0.8

            # Location effect
            location_factor = {
                'Tampa': 1.0,
                'Miami': 1.2,
                'Orlando': 0.9,
                'Jacksonville': 0.8
            }[location]

            # Category effect
            category_factor = {
                'Electronics': 1.5,
                'Clothing': 1.0,
                'Home Goods': 0.8,
                'Sporting Goods': 0.7,
                'Beauty': 0.9
            }[category]

            # Growth trend over time (5% per year, quarterly compounded)
            growth_factor = (1 + 0.05/4) ** quarter_idx

            # Calculate sales with some randomness
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)  # Add noise

            # Advertising spend (correlated with sales but with diminishing returns)
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)

            # Record
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

# Create customer data
customer_data = []
total_customers = 2000

# Age distribution parameters for each location
age_params = {
    'Tampa': (45, 15),      # Older demographic
    'Miami': (35, 12),      # Younger demographic
    'Orlando': (38, 14),    # Mixed demographic
    'Jacksonville': (42, 13)  # Middle-aged demographic
}

for location in locations:
    # Generate ages based on location demographics
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {
        'Tampa': 0.3,
        'Miami': 0.35,
        'Orlando': 0.2,
        'Jacksonville': 0.15
    }[location])

    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)  # Ensure ages are between 18-80

    # Generate purchase amounts
    for age in ages:
        # Younger and older customers spend differently across categories
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])

        # Purchase amount based on age and category
        base_amount = np.random.gamma(shape=5, scale=20)

        # Product tier (budget, mid-range, premium)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'],
                                     p=[0.3, 0.5, 0.2])

        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]

        purchase_amount = base_amount * tier_factor

        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

# Create DataFrames
sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

# Add some calculated columns
sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

# Print data info
print("\nSales Data Sample:")
print(sales_df.head())
print("\nCustomer Data Sample:")
print(customer_df.head())
print("\nDataFrames created successfully. Ready for visualization!")
# ----- END OF DATA CREATION -----


# TODO 1: Time Series Visualization - Sales Trends
def plot_quarterly_sales_trend():
    """
    Create a line chart showing total sales for each quarter.
    REQUIRED: Return the figure object
    """
    totals = sales_df.groupby('QuarterLabel')['Sales'].sum().reindex(quarter_labels)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(totals.index, totals.values, marker='o')
    ax.set_title("Overall Quarterly Sales Trend")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Total Sales ($)")
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_location_sales_comparison():
    """
    Create a multi-line chart comparing quarterly sales across different locations.
    REQUIRED: Return the figure object
    """
    pivot = sales_df.groupby(['QuarterLabel', 'Location'])['Sales'].sum().unstack()
    pivot = pivot.reindex(quarter_labels)

    fig, ax = plt.subplots(figsize=(10, 5))
    for loc in pivot.columns:
        ax.plot(pivot.index, pivot[loc].values, marker='o', label=loc)
    ax.set_title("Quarterly Sales Trends by Location")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales ($)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


# TODO 2: Categorical Comparison - Product Performance by Location
def plot_category_performance_by_location():
    """
    Create a grouped bar chart showing how each product category performs in different locations.
    REQUIRED: Return the figure object
    """
    grouped = sales_df.groupby(['Location', 'Category'])['Sales'].sum().unstack()
    grouped = grouped.reindex(index=locations, columns=categories)

    fig, ax = plt.subplots(figsize=(11, 6))
    grouped.plot(kind='bar', ax=ax)
    ax.set_title("Category Sales Performance by Location (Grouped)")
    ax.set_xlabel("Location")
    ax.set_ylabel("Total Sales ($)")
    ax.grid(axis='y', alpha=0.3)
    ax.legend(title="Category", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    return fig


def plot_sales_composition_by_location():
    """
    Create a stacked bar chart showing the composition of sales across categories for each location.
    REQUIRED: Return the figure object
    """
    grouped = sales_df.groupby(['Location', 'Category'])['Sales'].sum().unstack()
    grouped = grouped.reindex(index=locations, columns=categories)

    fig, ax = plt.subplots(figsize=(11, 6))
    grouped.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title("Sales Composition by Location (Stacked)")
    ax.set_xlabel("Location")
    ax.set_ylabel("Total Sales ($)")
    ax.grid(axis='y', alpha=0.3)
    ax.legend(title="Category", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    return fig


# TODO 3: Relationship Analysis - Advertising and Sales
def plot_ad_spend_vs_sales():
    """
    Create a scatter plot to visualize the relationship between advertising spend and sales.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(sales_df['AdSpend'], sales_df['Sales'], alpha=0.6)
    ax.set_title("Advertising Spend vs Sales")
    ax.set_xlabel("Ad Spend ($)")
    ax.set_ylabel("Sales ($)")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def plot_ad_efficiency_over_time():
    """
    Create a line chart showing how efficient advertising spend has been over time.
    REQUIRED: Return the figure object
    """
    # Avoid plotting infinite values if AdSpend is zero or extremely small
    efficiency = sales_df.copy()
    efficiency['SafeAdSpend'] = efficiency['AdSpend'].replace(0, np.nan)
    efficiency['SafeEfficiency'] = efficiency['Sales'] / efficiency['SafeAdSpend']

    avg_eff = efficiency.groupby('QuarterLabel')['SafeEfficiency'].mean().reindex(quarter_labels)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(avg_eff.index, avg_eff.values, marker='o')
    ax.set_title("Advertising Efficiency Over Time (Sales per $ Ad Spend)")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales per Dollar Spent")
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


# TODO 4: Distribution Analysis - Customer Demographics
def plot_customer_age_distribution():
    """
    Create histograms showing the age distribution of customers, both overall and by location.
    REQUIRED: Return the figure object
    """
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # Overall
    axs[0].hist(customer_df['Age'], bins=20)
    axs[0].set_title("Overall Customer Age Distribution")
    axs[0].set_xlabel("Age")
    axs[0].set_ylabel("Count")
    axs[0].grid(True, alpha=0.2)

    # By location overlay
    for loc in locations:
        subset = customer_df[customer_df['Location'] == loc]['Age']
        axs[1].hist(subset, bins=20, alpha=0.5, label=loc)

    axs[1].set_title("Age Distribution by Location")
    axs[1].set_xlabel("Age")
    axs[1].set_ylabel("Count")
    axs[1].legend()
    axs[1].grid(True, alpha=0.2)

    plt.tight_layout()
    return fig


def plot_purchase_by_age_group():
    """
    Create box plots showing purchase amounts across different age groups.
    REQUIRED: Return the figure object
    """
    bins = [18, 30, 45, 60, 81]
    labels = ['18-29', '30-44', '45-59', '60-80']
    temp = customer_df.copy()
    temp['AgeGroup'] = pd.cut(temp['Age'], bins=bins, labels=labels, right=False)

    data = [temp[temp['AgeGroup'] == lab]['PurchaseAmount'].values for lab in labels]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.boxplot(data, labels=labels)
    ax.set_title("Purchase Amount by Age Group")
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Purchase Amount ($)")
    ax.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    return fig


# TODO 5: Sales Distribution - Pricing Tiers
def plot_purchase_amount_distribution():
    """
    Create a histogram showing the distribution of purchase amounts.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(customer_df['PurchaseAmount'], bins=30)
    ax.set_title("Purchase Amount Distribution")
    ax.set_xlabel("Purchase Amount ($)")
    ax.set_ylabel("Frequency")
    ax.grid(True, alpha=0.2)
    plt.tight_layout()
    return fig


def plot_sales_by_price_tier():
    """
    Create a pie chart showing the breakdown of sales by price tier.
    REQUIRED: Return the figure object
    """
    tier_totals = customer_df.groupby('PriceTier')['PurchaseAmount'].sum()
    tier_totals = tier_totals.reindex(['Budget', 'Mid-range', 'Premium'])

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(tier_totals.values, labels=tier_totals.index, autopct='%1.1f%%', startangle=90)
    ax.set_title("Sales Breakdown by Price Tier")
    plt.tight_layout()
    return fig


# TODO 6: Market Share Analysis
def plot_category_market_share():
    """
    Create a pie chart showing the market share of each product category.
    REQUIRED: Return the figure object
    """
    totals = sales_df.groupby('Category')['Sales'].sum().reindex(categories)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(totals.values, labels=totals.index, autopct='%1.1f%%', startangle=90)
    ax.set_title("Market Share by Product Category (Sales)")
    plt.tight_layout()
    return fig


def plot_location_sales_distribution():
    """
    Create a pie chart showing the distribution of sales across different store locations.
    REQUIRED: Return the figure object
    """
    totals = sales_df.groupby('Location')['Sales'].sum().reindex(locations)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(totals.values, labels=totals.index, autopct='%1.1f%%', startangle=90)
    ax.set_title("Sales Distribution by Location")
    plt.tight_layout()
    return fig


# TODO 7: Comprehensive Dashboard
def create_business_dashboard():
    """
    Create a comprehensive dashboard with multiple subplots highlighting key business insights.
    REQUIRED: Return the figure object with at least 4 subplots
    """
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    # (1) Quarterly sales trend
    totals = sales_df.groupby('QuarterLabel')['Sales'].sum().reindex(quarter_labels)
    axs[0, 0].plot(totals.index, totals.values, marker='o')
    axs[0, 0].set_title("Total Sales Trend")
    axs[0, 0].tick_params(axis='x', rotation=45)
    axs[0, 0].grid(True, alpha=0.3)

    # (2) Sales by location
    loc_totals = sales_df.groupby('Location')['Sales'].sum().reindex(locations)
    axs[0, 1].bar(loc_totals.index, loc_totals.values)
    axs[0, 1].set_title("Total Sales by Location")
    axs[0, 1].grid(True, axis='y', alpha=0.3)

    # (3) Category market share
    cat_totals = sales_df.groupby('Category')['Sales'].sum().reindex(categories)
    axs[1, 0].pie(cat_totals.values, labels=cat_totals.index, autopct='%1.1f%%', startangle=90)
    axs[1, 0].set_title("Category Market Share")

    # (4) Ad spend vs sales scatter
    axs[1, 1].scatter(sales_df['AdSpend'], sales_df['Sales'], alpha=0.6)
    axs[1, 1].set_title("Ad Spend vs Sales")
    axs[1, 1].set_xlabel("Ad Spend ($)")
    axs[1, 1].set_ylabel("Sales ($)")
    axs[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


# Main function to execute all visualizations
# REQUIRED: Do not modify this function name
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)

    # Time Series Analysis
    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()

    # Categorical Comparison
    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()

    # Relationship Analysis
    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()

    # Distribution Analysis
    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()

    # Sales Distribution
    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()

    # Market Share Analysis
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()

    # Comprehensive Dashboard
    fig13 = create_business_dashboard()

    # REQUIRED: Add business insights summary
    print("\nKEY BUSINESS INSIGHTS:")

    # Insight 1: Best quarter overall
    quarter_totals = sales_df.groupby('QuarterLabel')['Sales'].sum().reindex(quarter_labels)
    best_quarter = quarter_totals.idxmax()
    print(f"- Highest total sales occurred in {best_quarter} (${quarter_totals.max():,.2f}).")

    # Insight 2: Best-performing location overall
    location_totals = sales_df.groupby('Location')['Sales'].sum().reindex(locations)
    best_location = location_totals.idxmax()
    print(f"- Top location by total sales: {best_location} (${location_totals.max():,.2f}).")

    # Insight 3: Best-performing category overall
    category_totals = sales_df.groupby('Category')['Sales'].sum().reindex(categories)
    best_category = category_totals.idxmax()
    print(f"- Top category by total sales: {best_category} (${category_totals.max():,.2f}).")

    # Insight 4: Relationship between AdSpend and Sales (correlation)
    corr = sales_df[['AdSpend', 'Sales']].corr().iloc[0, 1]
    print(f"- Correlation between Ad spend and Sales: {corr:.3f} (positive indicates higher ad spend generally aligns with higher sales).")

    # Insight 5: Customer tier contribution
    tier_sales = customer_df.groupby('PriceTier')['PurchaseAmount'].sum().reindex(['Budget', 'Mid-range', 'Premium'])
    top_tier = tier_sales.idxmax()
    print(f"- Price tier contributing most to customer purchase totals: {top_tier} (${tier_sales.max():,.2f}).")

    # Display all figures
    plt.show()


# Run the main function
if __name__ == "__main__":
    main()

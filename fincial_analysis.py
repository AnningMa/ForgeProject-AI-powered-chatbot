import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_data(filepath):
    """Load financial data from a CSV file."""
    return pd.read_excel(filepath)

def clean_data(df):
    """Clean the financial data by handling missing values and duplicates."""
    df.columns = df.columns.str.strip()
    if "Year" in df.columns:
        df["Year"] = df["Year"].astype(int)
        
    key_cols = ['Company', 'Year']
    duplicate_rows = df.duplicated(subset=key_cols).sum()
    if duplicate_rows > 0:
        df = df.drop_duplicates(subset=key_cols,keep='first')
        
    raw_financial_columns = [
        'Total Revenue', 'Net Income', 'Total Liabilities', 'Total Assets',
        'Cash Flow from Operating Activities', 'Total Current Assets', 
        'Total Current Liabilities'
    ]
    cols_to_fill = [col for col in raw_financial_columns if col in df.columns]
    df[cols_to_fill] = df[cols_to_fill].fillna(0)
    
    return df

def calculate_financial_ratios(df):
    """Calculate key financial ratios."""
    def safe_divide(numerator, denominator):
        denominator = denominator.replace(0, np.nan)
        return numerator / denominator
    
    # Profitability
    df["Net Profit Margin (%)"] = safe_divide(df["Net Income"], df["Total Revenue"]) * 100

    # Leverage
    df["Debt Ratio (%)"] = safe_divide(df["Total Liabilities"], df["Total Assets"]) * 100
    
    # Cash Flow Quality
    df["CFO / Net Income"] = safe_divide(df["Cash Flow from Operating Activities"], df["Net Income"])
    
    
    df["ROA (%)"] = safe_divide(df["Net Income"], df["Total Assets"]) * 100
   
    print("Financial ratios calculation complete.")
    return df

def plot_trends(df, metric, ylabel, title):
    """Plot trends of a given financial metric over years for each company."""
    plt.figure(figsize=(10, 6))
    df_sorted = df.sort_values(by=["Company", "Year"])
    for company, subset in df_sorted.groupby("Company"):
        plt.plot(subset["Year"], subset[metric], marker="o", label=company)
        
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()
 
if __name__ == "__main__":
    
    INPUT_FILE = 'financial_data.xlsx'
    OUTPUT_FILE = 'financials_with_ratios.xlsx'
    
    df = load_data(INPUT_FILE)
    if df is not None:
        df = clean_data(df)
        df = calculate_financial_ratios(df)
        
        try:
            df.to_excel(OUTPUT_FILE, index=False)
            print(f"Enhanced financial data saved to {OUTPUT_FILE}")
        except Exception as e:
            print(f"Error saving to Excel: {e}")
        
        plot_trends(df, 
                    metric="Total Revenue", 
                    ylabel="Revenue (USD, millions)", 
                    title="Total Revenue Trend")
        
        plot_trends(df, 
                    metric="Net Profit Margin (%)", 
                    ylabel="Net Profit Margin (%)", 
                    title="Net Profit Margin Trend")
        
        plot_trends(df, 
                    metric="Debt Ratio (%)", 
                    ylabel="Debt Ratio (%)", 
                    title="Debt Ratio (Leverage) Trend")
        
    
    
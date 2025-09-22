import streamlit as st
import pandas as pd

st.set_page_config(page_title="Promotion Analysis", layout="wide")
st.title("Promotion Performance Dashboard")

# --- Load data from file path ---
file_path = "Promotion Report newwwww.Xlsx"  # <-- Replace with your file path
df = pd.read_excel(file_path)

# Strip any accidental whitespace from column names
df.columns = df.columns.str.strip()

# Required columns based on your dataset
required_cols = ["Item Code", "Item Name", "Cost Price", "Sales Qty", "Promo Price1"]
missing_cols = [c for c in required_cols if c not in df.columns]

if missing_cols:
    st.error(f"Missing columns: {missing_cols}")
else:
    # Use Promo Price1 as effective price if available, else fallback to Sales Price
    df["Effective Price"] = df["Promo Price1"].fillna(df["Sales Price"])
    
    # Calculate Gross Profit and Margin %
    df["Gross Profit"] = (df["Effective Price"] - df["Cost Price"]) * df["Sales Qty"]
    df["Margin %"] = (df["Gross Profit"] / (df["Effective Price"] * df["Sales Qty"])) * 100
    
    # Top 10 items by Gross Profit
    top_items = df.sort_values(by="Gross Profit", ascending=False).head(10)
    st.subheader("Top 10 Items by Gross Profit")
    st.dataframe(top_items[["Item Code", "Item Name", "Sales Qty", "Effective Price", "Cost Price", "Gross Profit", "Margin %"]])
    
    # Top 10 items by Margin %
    top_margin = df.sort_values(by="Margin %", ascending=False).head(10)
    st.subheader("Top 10 Items by Margin %")
    st.dataframe(top_margin[["Item Code", "Item Name", "Sales Qty", "Effective Price", "Cost Price", "Gross Profit", "Margin %"]])
    
    # Suggestions
    st.subheader("Promotion Suggestions")
    suggestions = []
    
    high_gp_items = top_items["Item Name"].tolist()
    suggestions.append(f"Focus next promotion on high GP items: {', '.join(high_gp_items)}")
    
    low_gp_items = df.sort_values(by="Gross Profit").head(10)["Item Name"].tolist()
    suggestions.append(f"Consider reviewing low GP items: {', '.join(low_gp_items)}")
    
    for s in suggestions:
        st.write("- " + s)
    
    # --- Show Raw Data at the end ---
    st.subheader("Raw Data")
    st.dataframe(df)

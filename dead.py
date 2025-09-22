import streamlit as st
import pandas as pd

st.set_page_config(page_title="Promotion Analysis", layout="wide")
st.title("Promotion Performance Dashboard")

# --- Load data directly from file path ---
file_path = "Promotion Report newwwww.Xlsx"  # <-- Replace with your file path
df = pd.read_excel(file_path)

st.subheader("Raw Data")
st.dataframe(df)

# Ensure required columns are present
required_cols = ["Item Code", "Item Name", "Cost Price", "Sales Qty", "Promo Price1"]
missing_cols = [c for c in required_cols if c not in df.columns]

if missing_cols:
    st.error(f"Missing columns: {missing_cols}")
else:
    # Use Promo Price if available, else use Sales Price
    df["Effective Price"] = df["Promo Price1"].fillna(df["Sales Price"])
    
    # Calculate Gross Profit (GP) and Margin %
    df["Gross Profit"] = (df["Effective Price"] - df["Cost Price"]) * df["Sales Qty"]
    df["Margin %"] = (df["Gross Profit"] / (df["Effective Price"] * df["Sales Qty"])) * 100
    
    # Top 10 Items by GP
    top_items = df.sort_values(by="Gross Profit", ascending=False).head(10)
    st.subheader("Top 10 Items by Gross Profit")
    st.dataframe(top_items[["Item Code", "Item Name", "Sales Qty", "Effective Price", "Cost Price", "Gross Profit", "Margin %"]])
    
    # Top 10 Items by Margin %
    top_margin = df.sort_values(by="Margin %", ascending=False).head(10)
    st.subheader("Top 10 Items by Margin %")
    st.dataframe(top_margin[["Item Code", "Item Name", "Sales Qty", "Effective Price", "Cost Price", "Gross Profit", "Margin %"]])
    
    # If Category exists
    if "Category" in df.columns:
        category_gp = df.groupby("Category")["Gross Profit"].sum().sort_values(ascending=False)
        st.subheader("Top Categories by Gross Profit")
        st.dataframe(category_gp.reset_index())
    
    # Suggestions
    st.subheader("Promotion Suggestions")
    suggestions = []
    
    high_gp_items = top_items["Item Name"].tolist()
    suggestions.append(f"Focus next promotion on high GP items: {', '.join(high_gp_items)}")
    
    low_gp_items = df.sort_values(by="Gross Profit").head(10)["Item Name"].tolist()
    suggestions.append(f"Consider reviewing low GP items: {', '.join(low_gp_items)}")
    
    if "Category" in df.columns:
        top_categories = category_gp.head(3).index.tolist()
        suggestions.append(f"Prioritize promotions on top categories: {', '.join(top_categories)}")
    
    for s in suggestions:
        st.write("- " + s)

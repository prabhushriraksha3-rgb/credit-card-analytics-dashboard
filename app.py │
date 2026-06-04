import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# Page Configuration
# ----------------------------------

st.set_page_config(
    page_title="Credit Card Analytics Dashboard",
    page_icon="💳",
    layout="wide"
)

# ----------------------------------
# Custom Styling
# ----------------------------------

st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
h1 {
    color: #1f4e79;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# Load Dataset
# ----------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("credit_card_transactions.csv")

df = load_data()

# ----------------------------------
# Header
# ----------------------------------

st.title("💳 Credit Card Analytics Dashboard")
st.markdown("### Analyze Credit Card Transactions and Fraud Trends")

# ----------------------------------
# Sidebar Filters
# ----------------------------------

st.sidebar.header("Filters")

card_filter = st.sidebar.multiselect(
    "Select Card Type",
    options=df["Card_Type"].unique(),
    default=df["Card_Type"].unique()
)

status_filter = st.sidebar.multiselect(
    "Select Transaction Status",
    options=df["Transaction_Status"].unique(),
    default=df["Transaction_Status"].unique()
)

filtered_df = df[
    (df["Card_Type"].isin(card_filter)) &
    (df["Transaction_Status"].isin(status_filter))
]

# ----------------------------------
# KPI Section
# ----------------------------------

total_transactions = len(filtered_df)
total_amount = filtered_df["Amount"].sum()
fraud_count = filtered_df["Is_Fraud"].sum()

success_rate = (
    len(filtered_df[filtered_df["Transaction_Status"] == "Success"])
    / len(filtered_df)
) * 100 if len(filtered_df) > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Transactions", total_transactions)
col2.metric("Total Amount", f"₹{total_amount:,.0f}")
col3.metric("Fraud Cases", fraud_count)
col4.metric("Success Rate", f"{success_rate:.1f}%")

st.divider()

# ----------------------------------
# Row 1 Charts
# ----------------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("Card Type Usage")

    fig = px.pie(
        filtered_df,
        names="Card_Type",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Fraud Distribution")

    fraud_data = filtered_df["Is_Fraud"].value_counts()

    fig = px.pie(
        values=fraud_data.values,
        names=["Genuine", "Fraud"]
    )

    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# Spending Analysis
# ----------------------------------

st.subheader("Spending by Merchant Category")

category_data = (
    filtered_df.groupby("Merchant_Category")["Amount"]
    .sum()
    .reset_index()
)

fig = px.bar(
    category_data,
    x="Merchant_Category",
    y="Amount",
    text_auto=True,
    title="Total Spending by Category"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# Transaction Amount Distribution
# ----------------------------------

st.subheader("Transaction Amount Distribution")

fig = px.histogram(
    filtered_df,
    x="Amount",
    nbins=15,
    title="Transaction Amount Histogram"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# Top Customers
# ----------------------------------

st.subheader("Top Customers by Spending")

top_customers = (
    filtered_df.groupby("Customer_ID")["Amount"]
    .sum()
    .reset_index()
    .sort_values(by="Amount", ascending=False)
    .head(10)
)

fig = px.bar(
    top_customers,
    x="Customer_ID",
    y="Amount",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# Data Preview
# ----------------------------------

st.subheader("Transaction Data")

st.dataframe(filtered_df, use_container_width=True)

# ----------------------------------
# Business Insights
# ----------------------------------

st.subheader("📈 Business Insights")

most_used_card = filtered_df["Card_Type"].mode()[0]

highest_category = (
    filtered_df.groupby("Merchant_Category")["Amount"]
    .sum()
    .idxmax()
)

avg_transaction = filtered_df["Amount"].mean()

st.success(f"""
✅ Total Transaction Value: ₹{total_amount:,.0f}

✅ Most Used Card Type: {most_used_card}

✅ Highest Spending Category: {highest_category}

✅ Average Transaction Amount: ₹{avg_transaction:,.0f}

✅ Fraud Transactions Detected: {fraud_count}

✅ Transaction Success Rate: {success_rate:.1f}%
""")

# ----------------------------------
# Footer
# ----------------------------------

st.markdown("---")
st.caption("Credit Card Analytics Dashboard | Streamlit Project")

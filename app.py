import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------
# Page Configuration
# ---------------------------------------
st.set_page_config(
    page_title="Credit Card Analytics Dashboard",
    page_icon="💳",
    layout="wide"
)

# ---------------------------------------
# Title
# ---------------------------------------
st.title("💳 Credit Card Analytics Dashboard")
st.markdown("Analyze transactions, spending patterns, and fraud cases.")

# ---------------------------------------
# Load Data
# ---------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("credit_card_transactions.csv")

df = load_data()

# ---------------------------------------
# Sidebar Filters
# ---------------------------------------
st.sidebar.header("Filters")

card_types = st.sidebar.multiselect(
    "Card Type",
    options=df["Card_Type"].unique(),
    default=df["Card_Type"].unique()
)

statuses = st.sidebar.multiselect(
    "Transaction Status",
    options=df["Transaction_Status"].unique(),
    default=df["Transaction_Status"].unique()
)

filtered_df = df[
    (df["Card_Type"].isin(card_types)) &
    (df["Transaction_Status"].isin(statuses))
]

# ---------------------------------------
# KPI Metrics
# ---------------------------------------
total_transactions = len(filtered_df)
total_amount = filtered_df["Amount"].sum()
fraud_cases = filtered_df["Is_Fraud"].sum()

if total_transactions > 0:
    success_rate = (
        (filtered_df["Transaction_Status"] == "Success").sum()
        / total_transactions
    ) * 100
else:
    success_rate = 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Transactions", total_transactions)
col2.metric("Total Amount", f"₹{total_amount:,.0f}")
col3.metric("Fraud Cases", fraud_cases)
col4.metric("Success Rate", f"{success_rate:.1f}%")

st.divider()

# ---------------------------------------
# Card Usage Chart
# ---------------------------------------
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

    fraud_counts = filtered_df["Is_Fraud"].value_counts()

    fraud_df = pd.DataFrame({
        "Type": ["Genuine", "Fraud"],
        "Count": [
            fraud_counts.get(0, 0),
            fraud_counts.get(1, 0)
        ]
    })

    fig = px.pie(
        fraud_df,
        names="Type",
        values="Count",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------
# Spending by Category
# ---------------------------------------
st.subheader("Spending by Merchant Category")

category_df = (
    filtered_df.groupby("Merchant_Category")["Amount"]
    .sum()
    .reset_index()
)

fig = px.bar(
    category_df,
    x="Merchant_Category",
    y="Amount",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------
# Transaction Amount Distribution
# ---------------------------------------
st.subheader("Transaction Amount Distribution")

fig = px.histogram(
    filtered_df,
    x="Amount",
    nbins=20
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------
# Top Customers
# ---------------------------------------
st.subheader("Top 10 Customers by Spending")

customer_df = (
    filtered_df.groupby("Customer_ID")["Amount"]
    .sum()
    .reset_index()
    .sort_values("Amount", ascending=False)
    .head(10)
)

fig = px.bar(
    customer_df,
    x="Customer_ID",
    y="Amount",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------
# Data Table
# ---------------------------------------
st.subheader("Transaction Records")

st.dataframe(filtered_df, use_container_width=True)

# ---------------------------------------
# Business Insights
# ---------------------------------------
st.subheader("📈 Business Insights")

if len(filtered_df) > 0:

    most_used_card = filtered_df["Card_Type"].mode()[0]

    highest_category = (
        filtered_df.groupby("Merchant_Category")["Amount"]
        .sum()
        .idxmax()
    )

    avg_transaction = filtered_df["Amount"].mean()

    st.success(
        f"""
• Total Transaction Value: ₹{total_amount:,.0f}

• Most Used Card Type: {most_used_card}

• Highest Spending Category: {highest_category}

• Average Transaction Amount: ₹{avg_transaction:,.0f}

• Fraud Transactions: {fraud_cases}

• Success Rate: {success_rate:.1f}%
"""
    )

else:
    st.warning("No data available for the selected filters.")

# ---------------------------------------
# Footer
# ---------------------------------------
st.markdown("---")
st.caption("Built with Streamlit | Credit Card Analytics Dashboard")

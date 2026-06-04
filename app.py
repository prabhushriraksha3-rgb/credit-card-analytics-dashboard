import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Credit Card Fraud Analytics",
    page_icon="💳",
    layout="wide"
)

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("credit_card_transactions.csv")
    return df

df = load_data()

# -------------------------------------------------
# Load ML Model
# -------------------------------------------------
try:
    model = joblib.load("fraud_model.pkl")
    encoders = joblib.load("encoders.pkl")
    model_loaded = True
except:
    model_loaded = False

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("💳 Credit Card Fraud Analytics Dashboard")
st.markdown("Analyze transactions and predict fraudulent activity.")

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------
st.sidebar.header("Filters")

selected_cards = st.sidebar.multiselect(
    "Card Type",
    df["Card_Type"].unique(),
    default=df["Card_Type"].unique()
)

selected_status = st.sidebar.multiselect(
    "Transaction Status",
    df["Transaction_Status"].unique(),
    default=df["Transaction_Status"].unique()
)

filtered_df = df[
    (df["Card_Type"].isin(selected_cards)) &
    (df["Transaction_Status"].isin(selected_status))
]

# -------------------------------------------------
# KPI Metrics
# -------------------------------------------------
total_transactions = len(filtered_df)
total_amount = filtered_df["Amount"].sum()
fraud_cases = filtered_df["Is_Fraud"].sum()

success_rate = (
    (filtered_df["Transaction_Status"] == "Success").sum()
    / total_transactions * 100
) if total_transactions > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Transactions", total_transactions)
col2.metric("Total Amount", f"₹{total_amount:,.0f}")
col3.metric("Fraud Cases", int(fraud_cases))
col4.metric("Success Rate", f"{success_rate:.1f}%")

st.divider()

# -------------------------------------------------
# Charts
# -------------------------------------------------
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

    fraud_df = pd.DataFrame({
        "Category": ["Genuine", "Fraud"],
        "Count": [
            fraud_data.get(0, 0),
            fraud_data.get(1, 0)
        ]
    })

    fig = px.pie(
        fraud_df,
        names="Category",
        values="Count",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Spending Analysis
# -------------------------------------------------
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
    title="Category Wise Spending"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Amount Distribution
# -------------------------------------------------
st.subheader("Transaction Amount Distribution")

fig = px.histogram(
    filtered_df,
    x="Amount",
    nbins=15
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Top Customers
# -------------------------------------------------
st.subheader("Top Customers")

customer_df = (
    filtered_df.groupby("Customer_ID")["Amount"]
    .sum()
    .reset_index()
    .sort_values(
        by="Amount",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    customer_df,
    x="Customer_ID",
    y="Amount"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Dataset Preview
# -------------------------------------------------
st.subheader("Transaction Records")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# -------------------------------------------------
# Insights
# -------------------------------------------------
st.subheader("📈 Business Insights")

if not filtered_df.empty:

    most_used_card = filtered_df["Card_Type"].mode()[0]

    highest_category = (
        filtered_df.groupby("Merchant_Category")["Amount"]
        .sum()
        .idxmax()
    )

    avg_transaction = filtered_df["Amount"].mean()

    st.success(f"""
    • Total Transaction Value: ₹{total_amount:,.0f}

    • Most Used Card Type: {most_used_card}

    • Highest Spending Category: {highest_category}

    • Average Transaction Amount: ₹{avg_transaction:,.0f}

    • Fraud Transactions: {fraud_cases}

    • Success Rate: {success_rate:.1f}%
    """)

# -------------------------------------------------
# ML Fraud Prediction
# -------------------------------------------------
st.markdown("---")
st.header("🤖 Fraud Prediction")

if model_loaded:

    amount = st.number_input(
        "Transaction Amount",
        min_value=0,
        value=1000
    )

    card_type = st.selectbox(
        "Card Type",
        ["Visa", "MasterCard", "RuPay"]
    )

    merchant = st.selectbox(
        "Merchant Category",
        ["Shopping", "Food", "Travel", "Electronics"]
    )

    status = st.selectbox(
        "Transaction Status",
        ["Success", "Failed"]
    )

    if st.button("Predict Fraud"):

        card_encoded = (
            encoders["Card_Type"]
            .transform([card_type])[0]
        )

        merchant_encoded = (
            encoders["Merchant_Category"]
            .transform([merchant])[0]
        )

        status_encoded = (
            encoders["Transaction_Status"]
            .transform([status])[0]
        )

        input_df = pd.DataFrame({
            "Amount": [amount],
            "Card_Type": [card_encoded],
            "Merchant_Category": [merchant_encoded],
            "Transaction_Status": [status_encoded]
        })

        prediction = model.predict(input_df)[0]

        if prediction == 1:
            st.error("⚠ Fraud Transaction Detected")
        else:
            st.success("✅ Genuine Transaction")

else:
    st.warning(
        "Model files not found. Run train_model.py first."
    )

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.caption("Credit Card Fraud Analytics Dashboard | Streamlit + Machine Learning")

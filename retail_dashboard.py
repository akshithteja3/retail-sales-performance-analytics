
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------
# 1. Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Retail Sales Analytics",
    page_icon="📊",
    layout="wide"
)

# Dashboard Title
st.title("📊 Retail Sales Performance Analytics")
st.caption(
    "Explore sales trends, product performance, "
    "and customer insights."
)

# Consistent chart styling
sns.set_theme(style="whitegrid")

# --------------------------------------------------
# 2. Load Dataset
# --------------------------------------------------
df = pd.read_csv("retail_sales_dataset.csv")

df["Date"] = pd.to_datetime(df["Date"])

# Create Age Groups
bins = [17, 25, 35, 45, 55, 100]
labels = ["18-25", "26-35", "36-45", "46-55", "56+"]

df["Age Group"] = pd.cut(
    df["Age"],
    bins=bins,
    labels=labels
)

# --------------------------------------------------
# 3. Sidebar Filter
# --------------------------------------------------
st.sidebar.header("Dashboard Filters")

category = st.sidebar.selectbox(
    "Select Product Category",
    ["All", "Beauty", "Clothing", "Electronics"]
)

if category != "All":
    filtered_df = df[df["Product Category"] == category].copy()
else:
    filtered_df = df.copy()

# --------------------------------------------------
# 4. KPI Cards
# --------------------------------------------------
total_sales = filtered_df["Total Amount"].sum()
total_quantity = filtered_df["Quantity"].sum()
average_transaction = filtered_df["Total Amount"].mean()
total_transactions = len(filtered_df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Total Sales", f"₹{total_sales:,.0f}")

with col2:
    st.metric("📦 Total Quantity", f"{total_quantity:,}")

with col3:
    st.metric(
        "🧾 Average Transaction",
        f"₹{average_transaction:,.2f}"
    )

with col4:
    st.metric("🛍️ Total Transactions", f"{total_transactions:,}")

st.divider()

# --------------------------------------------------
# 5. Helper Function for Bar Charts
# --------------------------------------------------
def create_bar_chart(data, color, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(7, 4))

    bars = ax.bar(
        data.index.astype(str),
        data.values,
        color=color,
        edgecolor="white",
        linewidth=0.8
    )

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)

    # Add values above bars
    ax.bar_label(bars, fmt="%.0f", padding=3, fontsize=9)

    fig.tight_layout()
    return fig

# --------------------------------------------------
# 6. Monthly Sales Trend
# --------------------------------------------------
st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_df.groupby(filtered_df["Date"].dt.month)["Total Amount"]
    .sum()
    .reindex(range(1, 13), fill_value=0)
)

month_names = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

monthly_sales.index = month_names

fig = create_bar_chart(
    monthly_sales,
    "#4285F4",
    "Month",
    "Sales Amount (₹)"
)
st.pyplot(fig)
plt.close(fig)

# --------------------------------------------------
# 7. Sales by Category and Gender
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🛒 Sales by Product Category")

    category_sales = filtered_df.groupby(
        "Product Category"
    )["Total Amount"].sum().sort_values(ascending=False)

    fig = create_bar_chart(
        category_sales,
        "#34A853",
        "Product Category",
        "Sales Amount (₹)"
    )
    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.subheader("👥 Sales by Gender")

    gender_sales = filtered_df.groupby(
        "Gender"
    )["Total Amount"].sum()

    gender_colors = {
        "Female": "#A142F4",
        "Male": "#F9AB00"
    }

    fig, ax = plt.subplots(figsize=(7, 4))

    bars = ax.bar(
        gender_sales.index.astype(str),
        gender_sales.values,
        color=[
            gender_colors.get(gender, "#4285F4")
            for gender in gender_sales.index
        ],
        edgecolor="white"
    )

    ax.set_xlabel("Gender")
    ax.set_ylabel("Sales Amount (₹)")
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    ax.bar_label(bars, fmt="%.0f", padding=3, fontsize=9)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# --------------------------------------------------
# 8. Sales by Age Group and Quantity by Category
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Sales by Age Group")

    age_sales = filtered_df.groupby(
        "Age Group",
        observed=True
    )["Total Amount"].sum()

    fig = create_bar_chart(
        age_sales,
        "#F9AB00",
        "Age Group",
        "Sales Amount (₹)"
    )
    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.subheader("📦 Quantity Sold by Product Category")

    quantity_by_category = filtered_df.groupby(
        "Product Category"
    )["Quantity"].sum().sort_values(ascending=False)

    fig = create_bar_chart(
        quantity_by_category,
        "#00A6A6",
        "Product Category",
        "Quantity Sold"
    )
    st.pyplot(fig)
    plt.close(fig)

# --------------------------------------------------
# 9. Price per Unit vs Total Amount
# --------------------------------------------------
st.subheader("🔍 Price per Unit vs Total Amount")

fig, ax = plt.subplots(figsize=(9, 4))

sns.scatterplot(
    data=filtered_df,
    x="Price per Unit",
    y="Total Amount",
    hue="Product Category" if category == "All" else None,
    palette={
        "Beauty": "#A142F4",
        "Clothing": "#34A853",
        "Electronics": "#4285F4"
    } if category == "All" else None,
    alpha=0.75,
    s=65,
    ax=ax
)

ax.set_xlabel("Price per Unit (₹)")
ax.set_ylabel("Total Amount (₹)")
ax.grid(alpha=0.25)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# --------------------------------------------------
# 10. Correlation Heatmap
# --------------------------------------------------
st.subheader("🌡️ Correlation Heatmap")

correlation = filtered_df[
    ["Quantity", "Price per Unit", "Total Amount"]
].corr()

fig, ax = plt.subplots(figsize=(7, 4))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    vmin=-1,
    vmax=1,
    linewidths=0.5,
    ax=ax
)

ax.set_title("Correlation Between Sales Variables")
fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

# --------------------------------------------------
# 11. Dataset Preview
# --------------------------------------------------
with st.expander("🔎 View Filtered Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )

st.caption(
    "Retail Sales Performance Analytics | "
    "Built with Python, Pandas, Streamlit, Matplotlib and Seaborn"
)

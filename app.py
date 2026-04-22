import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
from PIL import Image

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="OmniChannel Consumer Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== DARK UI ====================
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: #ffffff;
}

.kpi-container {
    display: flex;
    gap: 20px;
}

.kpi-box {
    flex: 1;
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-radius: 20px;
}

.kpi-value {
    font-size: 2rem;
    font-weight: 800;
    color: #3b82f6;
}

.kpi-label {
    font-size: 0.8rem;
    color: #94a3b8;
}
</style>
""", unsafe_allow_html=True)

# ==================== DATA LOADING ====================
@st.cache_data
def load_data():
    paths = [
        "dataset/Consumer_Shopping_Behavior_dataset.csv",
        "Consumer_Shopping_Behavior_dataset.csv"
    ]

    for path in paths:
        if os.path.exists(path):
            return pd.read_csv(path)

    st.warning("⚠️ Using demo dataset")
    return pd.DataFrame({
        'Customer ID': range(100),
        'Purchase Amount (USD)': np.random.randint(20, 500, 100),
        'Category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Beauty'], 100),
        'Gender': np.random.choice(['Male', 'Female'], 100),
        'Age': np.random.randint(18, 70, 100),
        'Location': np.random.choice(['NY', 'London', 'Tokyo', 'Paris'], 100),
        'Season': np.random.choice(['Summer', 'Winter', 'Spring', 'Autumn'], 100),
        'Review Rating': np.random.uniform(1, 5, 100)
    })

df = load_data()

# ==================== SIDEBAR UPLOAD ====================
with st.sidebar:
    st.header("📂 Data Upload")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

# ==================== VALIDATION ====================
if df.empty:
    st.error("Dataset is empty")
    st.stop()

# ==================== FILTERS ====================
with st.sidebar:
    st.header("🔍 Filters")

    selected_cat = st.multiselect("Category", df['Category'].unique(), default=df['Category'].unique())
    selected_gen = st.multiselect("Gender", df['Gender'].unique(), default=df['Gender'].unique())
    selected_sea = st.multiselect("Season", df['Season'].unique(), default=df['Season'].unique())

    age_range = st.slider(
        "Age",
        int(df['Age'].min()),
        int(df['Age'].max()),
        (int(df['Age'].min()), int(df['Age'].max()))
    )

filtered_df = df[
    (df['Category'].isin(selected_cat)) &
    (df['Gender'].isin(selected_gen)) &
    (df['Season'].isin(selected_sea)) &
    (df['Age'] >= age_range[0]) &
    (df['Age'] <= age_range[1])
]

# ==================== KPIs ====================
total_rev = filtered_df['Purchase Amount (USD)'].sum()
total_cust = filtered_df['Customer ID'].nunique()
avg_val = filtered_df['Purchase Amount (USD)'].mean()
avg_rating = filtered_df['Review Rating'].mean()

st.title("💎 Consumer Intelligence Hub")

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-box">
        <div class="kpi-label">Revenue</div>
        <div class="kpi-value">${total_rev:,.0f}</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-label">Customers</div>
        <div class="kpi-value">{total_cust}</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-label">Avg Order</div>
        <div class="kpi-value">${avg_val:.2f}</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-label">Rating</div>
        <div class="kpi-value">{avg_rating:.2f}★</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== ML MODELS ====================
@st.cache_data
def train_model(df):
    df_model = df.copy()

    encoders = {}
    for col in ['Category', 'Gender', 'Season']:
        enc = LabelEncoder()
        df_model[col] = enc.fit_transform(df_model[col])
        encoders[col] = enc

    X = df_model[['Age', 'Category', 'Gender', 'Season']]
    y = df_model['Purchase Amount (USD)']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = LinearRegression()
    model.fit(X_train, y_train)

    return model, encoders


@st.cache_data
def customer_segmentation(df):
    data = df[['Age', 'Purchase Amount (USD)']].copy()

    scaler = StandardScaler()
    scaled = scaler.fit_transform(data)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)

    df = df.copy()
    df['Segment'] = kmeans.fit_predict(scaled)

    return df

# ==================== INSIGHTS ====================
def generate_insight(df):
    if df.empty:
        return "No data available."

    top_cat = df.groupby('Category')['Purchase Amount (USD)'].sum().idxmax()
    total = df['Purchase Amount (USD)'].sum()
    avg = df['Purchase Amount (USD)'].mean()
    rating = df['Review Rating'].mean()

    return f"""
📊 BUSINESS INSIGHT

💰 Revenue: ${total:,.0f}
📦 Top Category: {top_cat}
💳 Avg Order: ${avg:.2f}
⭐ Rating: {rating:.2f}

📌 Recommendation:
Focus marketing on {top_cat} customers and target high-spending users above ${avg:.2f}.
"""

# ==================== TABS ====================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Revenue",
    "👤 Behavior",
    "📦 Products",
    "🖼️ Screenshots",
    "🤖 AI"
])

# -------- TAB 1 --------
with tab1:
    fig = px.area(
        filtered_df.groupby(['Season', 'Category'])['Purchase Amount (USD)'].sum().reset_index(),
        x="Season", y="Purchase Amount (USD)", color="Category",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

# -------- TAB 2 --------
with tab2:
    seg_df = customer_segmentation(filtered_df)

    fig = px.scatter(
        seg_df,
        x='Age',
        y='Purchase Amount (USD)',
        color='Segment',
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

# -------- TAB 3 --------
with tab3:
    prod = filtered_df.groupby('Category').agg({
        'Purchase Amount (USD)': 'mean',
        'Review Rating': 'mean',
        'Customer ID': 'count'
    }).reset_index()

    fig = px.scatter(
        prod,
        x='Review Rating',
        y='Purchase Amount (USD)',
        size='Customer ID',
        color='Category',
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

# -------- TAB 4 --------
with tab4:
    st.subheader("Screenshots")
    st.info("Add /screenshots folder for images")

# -------- TAB 5 (AI) --------
with tab5:
    st.subheader("🤖 AI Prediction Engine")

    model, encoders = train_model(df)

    age = st.slider("Age", 18, 70, 30)
    category = st.selectbox("Category", df['Category'].unique())
    gender = st.selectbox("Gender", df['Gender'].unique())
    season = st.selectbox("Season", df['Season'].unique())

    input_data = np.array([[
        age,
        encoders['Category'].transform([category])[0],
        encoders['Gender'].transform([gender])[0],
        encoders['Season'].transform([season])[0]
    ]])

    prediction = model.predict(input_data)[0]

    st.metric("💰 Predicted Spend", f"${prediction:.2f}")

    st.markdown("### 🧠 AI Insight")
    st.info(generate_insight(filtered_df))

# ==================== DATA PREVIEW ====================
with st.expander("🔍 Data Preview"):
    st.dataframe(df.head(50))

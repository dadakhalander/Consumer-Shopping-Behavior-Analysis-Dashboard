import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
from PIL import Image

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
.stApp { background-color: #0e1117; color: #ffffff; }

.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 25px;
    margin-bottom: 20px;
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
            try:
                df = pd.read_csv(path)
                df.columns = df.columns.str.strip()
                return df
            except Exception as e:
                st.warning(f"Error reading dataset: {e}")

    # fallback dummy data
    st.warning("⚠️ Using demo dataset")
    return pd.DataFrame({
        'Customer ID': range(100),
        'Purchase Amount (USD)': np.random.randint(20, 500, 100),
        'Category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Beauty'], 100),
        'Gender': np.random.choice(['Male', 'Female'], 100),
        'Age': np.random.randint(18, 70, 100),
        'Location': np.random.choice(['NY', 'London', 'Tokyo', 'Paris'], 100),
        'Season': np.random.choice(['Summer', 'Winter', 'Spring', 'Autumn'], 100),
        'Payment Method': np.random.choice(['Card', 'PayPal', 'Cash'], 100),
        'Review Rating': np.random.uniform(1, 5, 100),
        'Subscription Status': np.random.choice(['Yes', 'No'], 100)
    })

df = load_data()

# ==================== FILE UPLOAD ====================
with st.sidebar:
    st.header("📂 Data Upload")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            df.columns = df.columns.str.strip()
            st.success("File uploaded successfully")
        except Exception as e:
            st.error(f"Error: {e}")

# ==================== VALIDATION ====================
if df.empty:
    st.error("Dataset is empty")
    st.stop()

# ==================== SIDEBAR FILTERS ====================
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

# ==================== FILTERING ====================
filtered_df = df[
    (df['Category'].isin(selected_cat)) &
    (df['Gender'].isin(selected_gen)) &
    (df['Season'].isin(selected_sea)) &
    (df['Age'] >= age_range[0]) &
    (df['Age'] <= age_range[1])
]

if filtered_df.empty:
    st.warning("No data matches filters")

# ==================== HEADER ====================
st.title("💎 Consumer Intelligence Hub")
st.caption("Advanced behavioral analytics dashboard")

# ==================== KPI ====================
total_rev = filtered_df['Purchase Amount (USD)'].sum()
total_cust = filtered_df['Customer ID'].nunique()
avg_val = filtered_df['Purchase Amount (USD)'].mean()
avg_rating = filtered_df['Review Rating'].mean()

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

# ==================== SCREENSHOT LOADER ====================
def load_screenshots(folder="screenshots"):
    images = []
    if os.path.exists(folder):
        for file in os.listdir(folder):
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                try:
                    img = Image.open(os.path.join(folder, file))
                    images.append((file, img))
                except:
                    pass
    return images

# ==================== TABS ====================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Revenue",
    "👤 Behavior",
    "📦 Products",
    "🖼️ Screenshots"
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
    fig = px.scatter(
        filtered_df,
        x='Age',
        y='Purchase Amount (USD)',
        color='Gender',
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

# -------- TAB 3 --------
with tab3:
    prod_data = filtered_df.groupby('Category').agg({
        'Purchase Amount (USD)': 'mean',
        'Review Rating': 'mean',
        'Customer ID': 'count'
    }).reset_index()

    fig = px.scatter(
        prod_data,
        x='Review Rating',
        y='Purchase Amount (USD)',
        size='Customer ID',
        color='Category',
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

# -------- TAB 4 (SCREENSHOTS) --------
with tab4:
    st.subheader("📸 Screenshots Gallery")

    screenshots = load_screenshots()

    if screenshots:
        cols = st.columns(3)
        for i, (name, img) in enumerate(screenshots):
            with cols[i % 3]:
                st.image(img, caption=name, use_container_width=True)
    else:
        st.info("No screenshots found in /screenshots folder")

# ==================== DATA PREVIEW ====================
with st.expander("🔍 Preview Data"):
    st.dataframe(df.head(50))

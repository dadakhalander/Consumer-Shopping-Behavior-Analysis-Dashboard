import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="OmniChannel Consumer Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== PREMIUM DARK UI CSS ====================
st.markdown("""
<style>
    /* Global Theme */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Glassmorphism Card Effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(0, 191, 255, 0.5);
    }
    
    /* KPI Styling */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
    }
    .kpi-box {
        flex: 1;
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 20px;
        border-bottom: 4px solid #3b82f6;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #3b82f6;
        margin: 0;
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0a0c10 !important;
        border-right: 1px solid #1e293b;
    }
    
    /* Header Styling */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(to right, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-title {
        text-align: center;
        color: #64748b;
        margin-bottom: 3rem;
        font-size: 1.2rem;
    }

    /* Custom Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b !important;
        color: white !important;
        border-radius: 10px 10px 0 0 !important;
        padding: 10px 30px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        box-shadow: 0px 0px 15px rgba(59, 130, 246, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA ENGINE ====================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("dataset/Consumer_Shopping_Behavior_dataset.csv")
        df.columns = df.columns.str.strip()
        return df
    except:
        # Create dummy data if file not found for demonstration
        return pd.DataFrame({
            'Customer ID': range(100),
            'Purchase Amount (USD)': np.random.randint(20, 500, 100),
            'Category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Beauty'], 100),
            'Gender': np.random.choice(['Male', 'Female'], 100),
            'Age': np.random.randint(18, 70, 100),
            'Location': np.random.choice(['New York', 'London', 'Tokyo', 'Paris'], 100),
            'Season': np.random.choice(['Summer', 'Winter', 'Spring', 'Autumn'], 100),
            'Payment Method': np.random.choice(['Credit Card', 'PayPal', 'Cash'], 100),
            'Review Rating': np.random.uniform(1, 5, 100),
            'Subscription Status': np.random.choice(['Yes', 'No'], 100)
        })

df = load_data()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #3b82f6;'>💎 Filters</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Professional Multiselects
    selected_cat = st.multiselect("Product Category", options=df['Category'].unique(), default=df['Category'].unique())
    selected_gen = st.multiselect("Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
    selected_sea = st.multiselect("Season", options=df['Season'].unique(), default=df['Season'].unique())
    age_range = st.slider("Customer Age", int(df['Age'].min()), int(df['Age'].max()), (int(df['Age'].min()), int(df['Age'].max())))

# Filtering Logic
filtered_df = df[
    (df['Category'].isin(selected_cat)) & 
    (df['Gender'].isin(selected_gen)) & 
    (df['Season'].isin(selected_sea)) & 
    (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])
]

# ==================== HEADER ====================
st.markdown('<h1 class="main-title">Consumer Intelligence Hub</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">High-fidelity behavioral analytics for strategic decision making</p>', unsafe_allow_html=True)

# ==================== EXECUTIVE KPI ROW ====================
# Custom HTML for the KPI row to avoid the "Standard Streamlit" look
total_rev = filtered_df['Purchase Amount (USD)'].sum()
total_cust = filtered_df['Customer ID'].nunique()
avg_val = filtered_df['Purchase Amount (USD)'].mean()
avg_rating = filtered_df['Review Rating'].mean()

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-box">
        <div class="kpi-label">Gross Revenue</div>
        <div class="kpi-value">${total_rev:,.0f}</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-label">Active Customers</div>
        <div class="kpi-value">{total_cust:,}</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-label">Avg Order Value</div>
        <div class="kpi-value">${avg_val:.2f}</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-label">Net Satisfaction</div>
        <div class="kpi-value">{avg_rating:.2f}★</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== MAIN ANALYTICS TABS ====================
tab1, tab2, tab3 = st.tabs(["🚀 Revenue Engine", "👤 Behavior Profiling", "📦 Product Ecosystem"])

# --- TAB 1: REVENUE ENGINE ---
with tab1:
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Revenue Flow by Category & Season")
        
        # Using a modern Area Chart for revenue trends
        fig_rev = px.area(
            filtered_df.groupby(['Season', 'Category'])['Purchase Amount (USD)'].sum().reset_index(),
            x="Season", y="Purchase Amount (USD)", color="Category",
            template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel,
            line_shape="spline"
        )
        fig_rev.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_rev, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Revenue Share")
        fig_pie = px.pie(
            filtered_df, values='Purchase Amount (USD)', names='Category',
            hole=0.7, template="plotly_dark",
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Bottom Insight Section
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("💡 Executive Insight")
    top_cat = filtered_df.groupby('Category')['Purchase Amount (USD)'].sum().idxmax()
    st.write(f"The **{top_cat}** category is currently driving the highest revenue. To maximize growth, consider expanding the product line in this category or launching targeted loyalty campaigns for high-spending users in this segment.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: BEHAVIOR PROFILING ---
with tab2:
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Spending by Age & Gender")
        fig_scatter = px.scatter(
            filtered_df, x='Age', y='Purchase Amount (USD)', color='Gender',
            template="plotly_dark", opacity=0.6,
            color_discrete_map={"Male": "#3b82f6", "Female": "#ec4899"}
        )
        fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Customer Segmentation")
        # Using a Sunburst chart for a more high-end feel
        fig_sun = px.sunburst(
            filtered_df, path=['Gender', 'Category'], values='Purchase Amount (USD)',
            template="plotly_dark", color='Purchase Amount (USD)', 
            color_continuous_scale='RdBu'
        )
        fig_sun.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_sun, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 3: PRODUCT ECOSYSTEM ---
with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Product Value vs. Satisfaction Matrix")
    
    # Custom Chart: Bubble chart of Rating vs Revenue
    prod_data = filtered_df.groupby('Category').agg({
        'Purchase Amount (USD)': 'mean',
        'Review Rating': 'mean',
        'Customer ID': 'count'
    }).reset_index()
    
    fig_bubble = px.scatter(
        prod_data, x='Review Rating', y='Purchase Amount (USD)',
        size='Customer ID', color='Category',
        template="plotly_dark", size_max=60,
        labels={'Purchase Amount (USD)': 'Avg Revenue', 'Review Rating': 'Avg Rating'}
    )
    fig_bubble.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bubble, use_container_width=True)
    
    st.info("🚩 **Quadrant Analysis:** Top-Right categories are 'Champions' (High Value, High Satisfaction). Bottom-Left are 'Underperformers'.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #475569; font-size: 0.8rem;'>
    <p>Designed for OmniChannel Intelligence | Proprietary Analysis Framework v3.1</p>
</div>
""", unsafe_allow_html=True)

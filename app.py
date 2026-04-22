import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import seaborn as sns

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Executive Consumer Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== MODERN PROFESSIONAL CSS ====================
st.markdown("""
<style>
    /* Main Background and Font */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Header Styling */
    .main-header {
        background-color: #1e293b;
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Custom KPI Card */
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4f46e5;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #f1f5f9 !important;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        padding: 0 20px;
        background-color: transparent;
        border-radius: 5px 5px 0 0;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4f46e5 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA ENGINE ====================
@st.cache_data
def load_and_clean_data():
    """Load data with robustness checks"""
    try:
        df = pd.read_csv("dataset/Consumer_Shopping_Behavior_dataset.csv")
        df.columns = df.columns.str.strip()
        
        # Handle missing values
        df = df.fillna({
            'Purchase Amount (USD)': df['Purchase Amount (USD)'].median(),
            'Review Rating': df['Review Rating'].median(),
            'Age': df['Age'].median()
        })
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_and_clean_data()

if df.empty:
    st.stop()

# ==================== SIDEBAR FILTERS ====================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/analytics.png", width=60)
    st.title("Control Panel")
    st.markdown("---")
    
    # Dynamic Filter Helper
    def create_filter(label, column):
        if column in df.columns:
            return st.multiselect(label, options=sorted(df[column].unique()), default=df[column].unique())
        return []

    selected_gender = create_filter("👤 Gender", 'Gender')
    selected_locations = create_filter("📍 Location", 'Location')
    selected_categories = create_filter("🏷️ Category", 'Category')
    selected_seasons = create_filter("🌞 Season", 'Season')
    selected_payment = create_filter("💳 Payment Method", 'Payment Method')

    if 'Age' in df.columns:
        age_range = st.slider("🎂 Age Range", int(df['Age'].min()), int(df['Age'].max()), (int(df['Age'].min()), int(df['Age'].max())))
    else:
        age_range = None

    st.markdown("---")
    if st.button("🔄 Reset Filters", use_container_width=True):
        st.rerun()

# ==================== APPLY FILTERS ====================
mask = (
    (df['Gender'].isin(selected_gender)) & 
    (df['Location'].isin(selected_locations)) & 
    (df['Category'].isin(selected_categories)) & 
    (df['Season'].isin(selected_seasons)) & 
    (df['Payment Method'].isin(selected_payment)) &
    (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])
)
filtered_df = df[mask]

# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <h1>Consumer Intelligence Hub</h1>
    <p>Data-driven insights into purchasing behavior and revenue growth</p>
</div>
""", unsafe_allow_html=True)

# ==================== TOP KPI ROW ====================
# Using a custom function to render professional cards
def render_kpi(label, value, delta=None):
    delta_html = f'<div style="color: #10b981; font-size: 0.8rem;">{delta}</div>' if delta else ""
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    total_rev = filtered_df['Purchase Amount (USD)'].sum()
    render_kpi("Total Revenue", f"${total_rev:,.0f}", f"{(total_rev/df['Purchase Amount (USD)'].sum()*100):.1f}% of Total")
with col2:
    total_cust = filtered_df['Customer ID'].nunique()
    render_kpi("Unique Customers", f"{total_cust:,}", f"{(total_cust/df['Customer ID'].nunique()*100):.1f}% of Base")
with col3:
    avg_ov = filtered_df['Purchase Amount (USD)'].mean()
    render_kpi("Avg Order Value", f"${avg_ov:.2f}", f"{avg_ov - df['Purchase Amount (USD)'].mean():.2f} vs Avg")
with col4:
    avg_rat = filtered_df['Review Rating'].mean()
    render_kpi("Customer Satisfaction", f"{avg_rat:.2f} / 5", f"{avg_rat - df['Review Rating'].mean():.2f} shift")

st.markdown("<br>", unsafe_allow_html=True)

# ==================== TABS ====================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Revenue Analysis", "👥 Customer Profiling", "📦 Product Intelligence", "💳 Logistics & Ops", "🛠️ Data Lab"
])

# --- TAB 1: REVENUE ANALYSIS ---
with tab1:
    c1, c2 = st.columns([6, 4])
    with c1:
        st.subheader("Revenue by Category & Season")
        rev_data = filtered_df.groupby(['Category', 'Season'])['Purchase Amount (USD)'].sum().reset_index()
        fig_rev = px.bar(rev_data, x='Category', y='Purchase Amount (USD)', color='Season', 
                         barmode='group', color_discrete_sequence=px.colors.qualitative.Prism,
                         template="plotly_white")
        st.plotly_chart(fig_rev, use_container_width=True)
    
    with c2:
        st.subheader("Revenue Share")
        fig_pie = px.pie(filtered_df, values='Purchase Amount (USD)', names='Category', 
                         hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

# --- TAB 2: CUSTOMER PROFILING ---
with tab2:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Age vs. Spending Power")
        fig_scatter = px.scatter(filtered_df, x='Age', y='Purchase Amount (USD)', color='Gender',
                                 trendline="ols", template="plotly_white",
                                 color_discrete_map={"Male": "#4f46e5", "Female": "#ec4899"})
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with c2:
        st.subheader("Purchase Frequency Distribution")
        freq_df = filtered_df['Frequency of Purchases'].value_counts().sort_index().reset_index()
        fig_freq = px.bar(freq_df, x='index', y='count', 
                          labels={'index': 'Frequency', 'count': 'Number of Customers'},
                          color='count', color_continuous_scale='Blues')
        st.plotly_chart(fig_freq, use_container_width=True)

# --- TAB 3: PRODUCT INTELLIGENCE ---
with tab3:
    st.subheader("Product Performance Matrix")
    # Analyzing the relationship between Rating and Revenue
    prod_perf = filtered_df.groupby('Item Purchased').agg({
        'Purchase Amount (USD)': 'sum',
        'Review Rating': 'mean'
    }).reset_index()
    
    fig_bubble = px.scatter(prod_perf, x='Review Rating', y='Purchase Amount (USD)', 
                            size='Purchase Amount (USD)', color='Review Rating',
                            hover_name='Item Purchased', size_max=40,
                            color_continuous_scale='RdYlGn', template="plotly_white")
    st.plotly_chart(fig_bubble, use_container_width=True)
    st.caption("💡 Interpretation: Top Right = High Revenue & High Satisfaction (Star Products)")

# --- TAB 4: LOGISTICS & OPS ---
with tab4:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Payment Method Efficiency")
        pay_df = filtered_df.groupby('Payment Method')['Purchase Amount (USD)'].mean().sort_values().reset_index()
        fig_pay = px.bar(pay_df, x='Purchase Amount (USD)', y='Payment Method', 
                         orientation='h', color='Purchase Amount (USD)', 
                         color_continuous_scale='Viridis')
        st.plotly_chart(fig_pay, use_container_width=True)
    
    with c2:
        st.subheader("Shipping Preference")
        ship_df = filtered_df['Shipping Type'].value_counts().reset_index()
        fig_ship = px.pie(ship_df, values='count', names='Shipping Type', 
                          color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_ship, use_container_width=True)

# --- TAB 5: DATA LAB ---
with tab5:
    st.subheader("Advanced Statistical Analysis")
    
    # Correlation Heatmap
    st.markdown("#### Feature Correlation Matrix")
    numeric_df = filtered_df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    fig_corr, ax = plt.subplots(figsize=(10, 6)) if 'plt' in globals() else None 
    # Using plotly for the heatmap to keep it consistent
    fig_heat = px.imshow(corr, text_auto=True, aspect="auto", 
                         color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
    st.plotly_chart(fig_heat, use_container_width=True)
    
    st.markdown("#### Raw Data Explorer")
    st.dataframe(filtered_df, use_container_width=True)
    
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export filtered data to CSV", data=csv, file_name="analytics_export.csv", mime="text/csv")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94a3b8; padding: 1rem;'>
    <p>Enterprise Consumer Analytics Hub | <b>Version 2.0 (Robust)</b></p>
</div>
""", unsafe_allow_html=True)

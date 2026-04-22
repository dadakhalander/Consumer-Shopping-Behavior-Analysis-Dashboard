import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Consumer Shopping Analytics Hub",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* KPI Card Styling */
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .kpi-card-green {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .kpi-card-blue {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .kpi-card-orange {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    .kpi-card-purple {
        background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .kpi-label {
        font-size: 1rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .kpi-delta {
        font-size: 0.9rem;
        margin-top: 5px;
    }
    
    /* Header styling */
    .dashboard-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 20px;
        color: white;
        text-align: center;
    }
    
    /* Metric boxes */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 15px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    div[data-testid="metric-container"] label {
        color: white !important;
        font-weight: 600;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: white;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA LOADING ====================
@st.cache_data
def load_data():
    """Load and preprocess the dataset"""
    df = pd.read_csv("dataset/Consumer_Shopping_Behavior_dataset.csv")
    df.columns = df.columns.str.strip()
    return df

# Load data
df = load_data()

# ==================== SIDEBAR FILTERS ====================
st.sidebar.image("https://img.icons8.com/fluency/96/shopping-cart.png", width=80)
st.sidebar.title("🎯 Filter Dashboard")
st.sidebar.markdown("---")

# Gender Filter
if 'Gender' in df.columns:
    gender_options = ['All'] + list(df['Gender'].unique())
    selected_gender = st.sidebar.multiselect(
        "👤 Gender",
        options=df['Gender'].unique(),
        default=df['Gender'].unique()
    )
else:
    selected_gender = []

# Age Range Filter
if 'Age' in df.columns:
    age_min, age_max = int(df['Age'].min()), int(df['Age'].max())
    age_range = st.sidebar.slider(
        "🎂 Age Range",
        min_value=age_min,
        max_value=age_max,
        value=(age_min, age_max)
    )
else:
    age_range = None

# Location Filter
if 'Location' in df.columns:
    selected_locations = st.sidebar.multiselect(
        "📍 Location",
        options=sorted(df['Location'].unique()),
        default=df['Location'].unique()
    )
else:
    selected_locations = []

# Category Filter
if 'Category' in df.columns:
    selected_categories = st.sidebar.multiselect(
        "🏷️ Product Category",
        options=sorted(df['Category'].unique()),
        default=df['Category'].unique()
    )
else:
    selected_categories = []

# Season Filter
if 'Season' in df.columns:
    selected_seasons = st.sidebar.multiselect(
        "🌞 Season",
        options=df['Season'].unique(),
        default=df['Season'].unique()
    )
else:
    selected_seasons = []

# Payment Method Filter
if 'Payment Method' in df.columns:
    selected_payment = st.sidebar.multiselect(
        "💳 Payment Method",
        options=df['Payment Method'].unique(),
        default=df['Payment Method'].unique()
    )
else:
    selected_payment = []

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset All Filters"):
    st.rerun()

# ==================== APPLY FILTERS ====================
filtered_df = df.copy()

if selected_gender:
    filtered_df = filtered_df[filtered_df['Gender'].isin(selected_gender)]

if age_range:
    filtered_df = filtered_df[(filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1])]

if selected_locations:
    filtered_df = filtered_df[filtered_df['Location'].isin(selected_locations)]

if selected_categories:
    filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories)]

if selected_seasons:
    filtered_df = filtered_df[filtered_df['Season'].isin(selected_seasons)]

if selected_payment:
    filtered_df = filtered_df[filtered_df['Payment Method'].isin(selected_payment)]

# ==================== HEADER ====================
st.markdown("""
<div class="dashboard-header">
    <h1>🛍️ Consumer Shopping Analytics Hub</h1>
    <p style="font-size: 1.2rem; margin-top: 10px;">
        Comprehensive insights into consumer behavior, purchasing patterns, and business performance
    </p>
</div>
""", unsafe_allow_html=True)

# ==================== KEY METRICS ====================
st.markdown("### 📊 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

# Total Revenue
total_revenue = filtered_df['Purchase Amount (USD)'].sum()
avg_revenue = df['Purchase Amount (USD)'].sum() / len(df['Customer ID'].unique()) if len(df) > 0 else 0
revenue_per_customer = total_revenue / filtered_df['Customer ID'].nunique() if len(filtered_df) > 0 else 0

with col1:
    st.metric(
        label="💰 Total Revenue",
        value=f"${total_revenue:,.0f}",
        delta=f"{(total_revenue/df['Purchase Amount (USD)'].sum()*100):.1f}% of total"
    )

# Total Customers
total_customers = filtered_df['Customer ID'].nunique()
with col2:
    st.metric(
        label="👥 Unique Customers",
        value=f"{total_customers:,}",
        delta=f"{(total_customers/df['Customer ID'].nunique()*100):.1f}% of base"
    )

# Average Order Value
avg_order_value = filtered_df['Purchase Amount (USD)'].mean()
with col3:
    st.metric(
        label="🛒 Avg Order Value",
        value=f"${avg_order_value:.2f}",
        delta=f"${avg_order_value - df['Purchase Amount (USD)'].mean():.2f}"
    )

# Total Transactions
total_transactions = len(filtered_df)
with col4:
    st.metric(
        label="📦 Total Orders",
        value=f"{total_transactions:,}",
        delta=f"{(total_transactions/len(df)*100):.1f}% of total"
    )

# Average Rating
avg_rating = filtered_df['Review Rating'].mean()
with col5:
    st.metric(
        label="⭐ Avg Rating",
        value=f"{avg_rating:.2f}/5.0",
        delta=f"{avg_rating - df['Review Rating'].mean():.2f}"
    )

st.markdown("---")

# ==================== SECONDARY METRICS ====================
st.markdown("### 📈 Advanced Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    # Customer Lifetime Value proxy
    clv = filtered_df.groupby('Customer ID')['Purchase Amount (USD)'].sum().mean()
    st.metric(
        label="💎 Avg Customer Value",
        value=f"${clv:.2f}",
        delta="Lifetime estimate"
    )

with col2:
    # Discount penetration
    discount_rate = (filtered_df['Discount Applied'] == 'Yes').sum() / len(filtered_df) * 100
    st.metric(
        label="🎁 Discount Rate",
        value=f"{discount_rate:.1f}%",
        delta=f"{discount_rate - ((df['Discount Applied'] == 'Yes').sum() / len(df) * 100):.1f}%"
    )

with col3:
    # Subscription rate
    subscription_rate = (filtered_df['Subscription Status'] == 'Yes').sum() / len(filtered_df) * 100
    st.metric(
        label="🔔 Subscription Rate",
        value=f"{subscription_rate:.1f}%",
        delta=f"{subscription_rate - ((df['Subscription Status'] == 'Yes').sum() / len(df) * 100):.1f}%"
    )

with col4:
    # Repeat customers
    repeat_customers = (filtered_df['Previous Purchases'] > 0).sum() / len(filtered_df) * 100
    st.metric(
        label="🔁 Repeat Customers",
        value=f"{repeat_customers:.1f}%",
        delta=f"{repeat_customers - ((df['Previous Purchases'] > 0).sum() / len(df) * 100):.1f}%"
    )

st.markdown("---")

# ==================== TAB LAYOUT ====================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Sales Analytics", 
    "👥 Customer Insights", 
    "🏷️ Product Analysis", 
    "💳 Payment & Shipping",
    "🔍 Data Explorer"
])

# ==================== TAB 1: SALES ANALYTICS ====================
with tab1:
    st.markdown("### 💵 Sales Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by Category
        st.markdown("#### Revenue by Category")
        category_sales = filtered_df.groupby('Category')['Purchase Amount (USD)'].sum().reset_index()
        category_sales = category_sales.sort_values('Purchase Amount (USD)', ascending=False)
        
        fig_cat_revenue = px.bar(
            category_sales,
            x='Category',
            y='Purchase Amount (USD)',
            color='Purchase Amount (USD)',
            color_continuous_scale='Viridis',
            text_auto='$.2s',
            title='Total Revenue by Product Category'
        )
        fig_cat_revenue.update_layout(
            showlegend=False,
            height=400,
            xaxis_title="Category",
            yaxis_title="Revenue (USD)"
        )
        st.plotly_chart(fig_cat_revenue, use_container_width=True)
    
    with col2:
        # Revenue by Season
        st.markdown("#### Seasonal Revenue Distribution")
        season_sales = filtered_df.groupby('Season')['Purchase Amount (USD)'].sum().reset_index()
        
        fig_season = px.pie(
            season_sales,
            values='Purchase Amount (USD)',
            names='Season',
            title='Revenue Distribution by Season',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_season.update_layout(height=400)
        st.plotly_chart(fig_season, use_container_width=True)
    
    # Revenue Distribution Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Purchase Amount Distribution")
        fig_dist = px.histogram(
            filtered_df,
            x='Purchase Amount (USD)',
            nbins=30,
            title='Distribution of Purchase Amounts',
            color_discrete_sequence=['#667eea']
        )
        fig_dist.update_layout(
            showlegend=False,
            height=400,
            xaxis_title="Purchase Amount (USD)",
            yaxis_title="Frequency"
        )
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        st.markdown("#### Top 10 Locations by Revenue")
        location_sales = filtered_df.groupby('Location')['Purchase Amount (USD)'].sum().reset_index()
        location_sales = location_sales.sort_values('Purchase Amount (USD)', ascending=False).head(10)
        
        fig_loc = px.bar(
            location_sales,
            x='Purchase Amount (USD)',
            y='Location',
            orientation='h',
            color='Purchase Amount (USD)',
            color_continuous_scale='Plasma',
            text_auto='$.2s',
            title='Top 10 Revenue-Generating Locations'
        )
        fig_loc.update_layout(
            showlegend=False,
            height=400,
            xaxis_title="Revenue (USD)",
            yaxis_title="Location"
        )
        st.plotly_chart(fig_loc, use_container_width=True)
    
    # Category Performance Matrix
    st.markdown("#### Category Performance Matrix")
    category_metrics = filtered_df.groupby('Category').agg({
        'Purchase Amount (USD)': ['sum', 'mean', 'count'],
        'Review Rating': 'mean'
    }).reset_index()
    category_metrics.columns = ['Category', 'Total Revenue', 'Avg Order Value', 'Order Count', 'Avg Rating']
    category_metrics = category_metrics.sort_values('Total Revenue', ascending=False)
    
    fig_matrix = go.Figure(data=[go.Table(
        header=dict(
            values=list(category_metrics.columns),
            fill_color='#667eea',
            align='left',
            font=dict(color='white', size=12)
        ),
        cells=dict(
            values=[category_metrics[col] for col in category_metrics.columns],
            fill_color='lavender',
            align='left',
            format=['', '$,.0f', '$,.2f', ',d', '.2f']
        )
    )])
    fig_matrix.update_layout(height=300)
    st.plotly_chart(fig_matrix, use_container_width=True)

# ==================== TAB 2: CUSTOMER INSIGHTS ====================
with tab2:
    st.markdown("### 👤 Customer Demographics & Behavior")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Gender Distribution
        st.markdown("#### Gender Distribution")
        gender_counts = filtered_df['Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']
        
        fig_gender = px.pie(
            gender_counts,
            values='Count',
            names='Gender',
            title='Customer Gender Split',
            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb']
        )
        fig_gender.update_layout(height=350)
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with col2:
        # Subscription Status
        st.markdown("#### Subscription Status")
        sub_counts = filtered_df['Subscription Status'].value_counts().reset_index()
        sub_counts.columns = ['Status', 'Count']
        
        fig_sub = px.pie(
            sub_counts,
            values='Count',
            names='Status',
            title='Subscription Distribution',
            hole=0.4,
            color_discrete_sequence=['#4facfe', '#00f2fe']
        )
        fig_sub.update_layout(height=350)
        st.plotly_chart(fig_sub, use_container_width=True)
    
    with col3:
        # Purchase Frequency
        st.markdown("#### Purchase Frequency")
        freq_counts = filtered_df['Frequency of Purchases'].value_counts().reset_index()
        freq_counts.columns = ['Frequency', 'Count']
        
        fig_freq = px.bar(
            freq_counts,
            x='Frequency',
            y='Count',
            title='Purchase Frequency Distribution',
            color='Count',
            color_continuous_scale='Teal'
        )
        fig_freq.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig_freq, use_container_width=True)
    
    # Age Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Age Distribution")
        fig_age = px.histogram(
            filtered_df,
            x='Age',
            nbins=20,
            title='Customer Age Distribution',
            color='Gender',
            barmode='overlay',
            color_discrete_sequence=['#667eea', '#f5576c']
        )
        fig_age.update_layout(height=400)
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        st.markdown("#### Age vs Purchase Amount")
        age_purchase = filtered_df.groupby('Age')['Purchase Amount (USD)'].mean().reset_index()
        
        fig_age_purchase = px.scatter(
            filtered_df,
            x='Age',
            y='Purchase Amount (USD)',
            color='Gender',
            trendline='lowess',
            title='Age vs Purchase Amount Analysis',
            color_discrete_sequence=['#667eea', '#f5576c']
        )
        fig_age_purchase.update_layout(height=400)
        st.plotly_chart(fig_age_purchase, use_container_width=True)
    
    # Customer Segmentation
    st.markdown("#### Customer Segmentation by Value")
    
    customer_value = filtered_df.groupby('Customer ID').agg({
        'Purchase Amount (USD)': 'sum',
        'Customer ID': 'count'
    }).reset_index()
    customer_value.columns = ['Customer ID', 'Total Spent', 'Order Count']
    
    # Create segments
    customer_value['Segment'] = pd.cut(
        customer_value['Total Spent'],
        bins=[0, 50, 100, 200, float('inf')],
        labels=['Low Value', 'Medium Value', 'High Value', 'VIP']
    )
    
    segment_dist = customer_value['Segment'].value_counts().reset_index()
    segment_dist.columns = ['Segment', 'Count']
    
    fig_segment = px.funnel(
        segment_dist,
        x='Count',
        y='Segment',
        title='Customer Value Segmentation',
        color='Segment',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_segment.update_layout(height=400)
    st.plotly_chart(fig_segment, use_container_width=True)

# ==================== TAB 3: PRODUCT ANALYSIS ====================
with tab3:
    st.markdown("### 🏷️ Product Performance & Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top Items
        st.markdown("#### Top 15 Best-Selling Items")
        item_sales = filtered_df.groupby('Item Purchased').agg({
            'Purchase Amount (USD)': 'sum',
            'Item Purchased': 'count'
        }).reset_index()
        item_sales.columns = ['Item', 'Revenue', 'Units Sold']
        item_sales = item_sales.sort_values('Revenue', ascending=False).head(15)
        
        fig_items = px.bar(
            item_sales,
            x='Revenue',
            y='Item',
            orientation='h',
            color='Revenue',
            color_continuous_scale='Turbo',
            text_auto='$.2s',
            title='Top Products by Revenue'
        )
        fig_items.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_items, use_container_width=True)
    
    with col2:
        # Color Preferences
        st.markdown("#### Color Preferences")
        color_counts = filtered_df['Color'].value_counts().head(10).reset_index()
        color_counts.columns = ['Color', 'Count']
        
        fig_colors = px.bar(
            color_counts,
            x='Color',
            y='Count',
            title='Top 10 Popular Colors',
            color='Count',
            color_continuous_scale='Rainbow'
        )
        fig_colors.update_layout(height=250, showlegend=False)
        st.plotly_chart(fig_colors, use_container_width=True)
        
        # Size Distribution
        st.markdown("#### Size Distribution")
        size_counts = filtered_df['Size'].value_counts().reset_index()
        size_counts.columns = ['Size', 'Count']
        
        fig_sizes = px.pie(
            size_counts,
            values='Count',
            names='Size',
            title='Size Preference Distribution',
            hole=0.3
        )
        fig_sizes.update_layout(height=250)
        st.plotly_chart(fig_sizes, use_container_width=True)
    
    # Review Rating Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Review Rating Distribution")
        fig_rating = px.histogram(
            filtered_df,
            x='Review Rating',
            nbins=10,
            title='Customer Review Ratings',
            color_discrete_sequence=['#667eea']
        )
        fig_rating.update_layout(height=400)
        st.plotly_chart(fig_rating, use_container_width=True)
    
    with col2:
        st.markdown("#### Average Rating by Category")
        category_rating = filtered_df.groupby('Category')['Review Rating'].mean().reset_index()
        category_rating = category_rating.sort_values('Review Rating', ascending=False)
        
        fig_cat_rating = px.bar(
            category_rating,
            x='Category',
            y='Review Rating',
            title='Category Performance by Rating',
            color='Review Rating',
            color_continuous_scale='YlGn',
            text_auto='.2f'
        )
        fig_cat_rating.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_cat_rating, use_container_width=True)
    
    # Category-Season Heatmap
    st.markdown("#### Category Performance by Season")
    season_category = filtered_df.groupby(['Season', 'Category'])['Purchase Amount (USD)'].sum().reset_index()
    season_category_pivot = season_category.pivot(index='Category', columns='Season', values='Purchase Amount (USD)')
    
    fig_heatmap = px.imshow(
        season_category_pivot,
        title='Revenue Heatmap: Category vs Season',
        color_continuous_scale='YlOrRd',
        aspect='auto',
        labels=dict(color="Revenue (USD)")
    )
    fig_heatmap.update_layout(height=400)
    st.plotly_chart(fig_heatmap, use_container_width=True)

# ==================== TAB 4: PAYMENT & SHIPPING ====================
with tab4:
    st.markdown("### 💳 Payment Methods & Shipping Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Payment Methods
        st.markdown("#### Payment Method Distribution")
        payment_counts = filtered_df['Payment Method'].value_counts().reset_index()
        payment_counts.columns = ['Method', 'Count']
        
        fig_payment = px.pie(
            payment_counts,
            values='Count',
            names='Method',
            title='Payment Preferences',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_payment.update_layout(height=400)
        st.plotly_chart(fig_payment, use_container_width=True)
    
    with col2:
        # Shipping Types
        st.markdown("#### Shipping Type Distribution")
        shipping_counts = filtered_df['Shipping Type'].value_counts().reset_index()
        shipping_counts.columns = ['Type', 'Count']
        
        fig_shipping = px.bar(
            shipping_counts,
            x='Type',
            y='Count',
            title='Shipping Method Preferences',
            color='Count',
            color_continuous_scale='Blues'
        )
        fig_shipping.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_shipping, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Discount Analysis
        st.markdown("#### Discount Impact Analysis")
        discount_revenue = filtered_df.groupby('Discount Applied')['Purchase Amount (USD)'].agg(['sum', 'mean', 'count']).reset_index()
        discount_revenue.columns = ['Discount Applied', 'Total Revenue', 'Avg Order', 'Order Count']
        
        fig_discount = px.bar(
            discount_revenue,
            x='Discount Applied',
            y='Total Revenue',
            title='Revenue by Discount Status',
            color='Total Revenue',
            text_auto='$.2s',
            color_continuous_scale='Greens'
        )
        fig_discount.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_discount, use_container_width=True)
    
    with col2:
        # Promo Code Usage
        st.markdown("#### Promo Code Utilization")
        promo_counts = filtered_df['Promo Code Used'].value_counts().reset_index()
        promo_counts.columns = ['Promo Used', 'Count']
        
        fig_promo = px.pie(
            promo_counts,
            values='Count',
            names='Promo Used',
            title='Promo Code Usage',
            color_discrete_sequence=['#667eea', '#f5576c']
        )
        fig_promo.update_layout(height=400)
        st.plotly_chart(fig_promo, use_container_width=True)
    
    # Payment Method by Category
    st.markdown("#### Payment Methods by Product Category")
    payment_category = filtered_df.groupby(['Category', 'Payment Method']).size().reset_index(name='Count')
    
    fig_payment_cat = px.bar(
        payment_category,
        x='Category',
        y='Count',
        color='Payment Method',
        title='Payment Method Preferences Across Categories',
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_payment_cat.update_layout(height=400)
    st.plotly_chart(fig_payment_cat, use_container_width=True)
    
    # Shipping + Subscription Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Subscription vs Non-Subscription Revenue")
        sub_revenue = filtered_df.groupby('Subscription Status')['Purchase Amount (USD)'].sum().reset_index()
        
        fig_sub_rev = px.bar(
            sub_revenue,
            x='Subscription Status',
            y='Purchase Amount (USD)',
            title='Revenue by Subscription Status',
            color='Purchase Amount (USD)',
            text_auto='$.2s',
            color_continuous_scale='Purples'
        )
        fig_sub_rev.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_sub_rev, use_container_width=True)
    
    with col2:
        st.markdown("#### Previous Purchases Distribution")
        fig_prev = px.histogram(
            filtered_df,
            x='Previous Purchases',
            nbins=20,
            title='Customer Purchase History',
            color_discrete_sequence=['#764ba2']
        )
        fig_prev.update_layout(height=400)
        st.plotly_chart(fig_prev, use_container_width=True)

# ==================== TAB 5: DATA EXPLORER ====================
with tab5:
    st.markdown("### 🔍 Raw Data Explorer")
    
    # Summary Statistics
    st.markdown("#### Dataset Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**Total Rows:** {len(filtered_df):,}")
    with col2:
        st.info(f"**Total Columns:** {len(filtered_df.columns)}")
    with col3:
        st.info(f"**Date Range:** All Time")
    
    # Show filtered data
    st.markdown("#### Filtered Dataset")
    st.dataframe(
        filtered_df.head(100),
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_shopping_data.csv',
        mime='text/csv',
    )
    
    # Statistical Summary
    st.markdown("#### Statistical Summary")
    st.dataframe(
        filtered_df.describe(),
        use_container_width=True
    )

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🛍️ Consumer Shopping Analytics Dashboard | Built with Streamlit & Plotly</p>
    <p>Data refreshes in real-time based on filter selections</p>
</div>
""", unsafe_allow_html=True)

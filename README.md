# 🛍️ Consumer Shopping Analytics Dashboard

A comprehensive, interactive KPI dashboard built with Streamlit for analyzing consumer shopping behavior and business performance metrics.

## ✨ Features

### 📊 Key Performance Indicators
- **Total Revenue** - Real-time revenue tracking with percentage insights
- **Unique Customers** - Customer base analytics
- **Average Order Value** - Purchase size metrics
- **Total Orders** - Transaction volume
- **Average Rating** - Customer satisfaction scores
- **Customer Lifetime Value** - Revenue per customer
- **Discount & Subscription Rates** - Promotional metrics
- **Repeat Customer Rate** - Retention analytics

### 📈 Analytics Modules

#### 1. Sales Analytics
- Revenue by product category
- Seasonal revenue distribution
- Purchase amount distribution
- Top revenue-generating locations
- Category performance matrix

#### 2. Customer Insights
- Gender demographics
- Age distribution analysis
- Subscription status breakdown
- Purchase frequency patterns
- Age vs purchase correlation
- Customer value segmentation

#### 3. Product Analysis
- Best-selling items (Top 15)
- Color preferences
- Size distribution
- Review rating analysis
- Category performance ratings
- Category-Season performance heatmap

#### 4. Payment & Shipping Analytics
- Payment method preferences
- Shipping type distribution
- Discount impact analysis
- Promo code utilization
- Payment methods by category
- Subscription revenue comparison

#### 5. Data Explorer
- Raw data preview
- Statistical summaries
- CSV export functionality

### 🎨 Design Features
- Professional gradient color schemes
- Interactive filters with real-time updates
- Responsive layout for all screen sizes
- Custom CSS styling for modern UI
- Tab-based navigation
- Dynamic KPI cards with delta indicators

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download this repository**
```bash
cd your-project-folder
```

2. **Install required packages**
```bash
pip install streamlit pandas plotly numpy
```

3. **Prepare your dataset**
   - Place your CSV file in a folder named `dataset/`
   - Ensure the file is named: `Consumer_Shopping_Behavior_dataset.csv`
   - Your directory structure should look like:
   ```
   your-project-folder/
   ├── dashboard.py
   └── dataset/
       └── Consumer_Shopping_Behavior_dataset.csv
   ```

4. **Run the dashboard**
```bash
streamlit run dashboard.py
```

5. **Access the dashboard**
   - The dashboard will automatically open in your browser
   - Default URL: `http://localhost:8501`

## 📋 Dataset Requirements

Your CSV file should contain the following columns:
- `Customer ID` - Unique customer identifier
- `Age` - Customer age
- `Gender` - Customer gender
- `Item Purchased` - Product name
- `Category` - Product category
- `Purchase Amount (USD)` - Transaction amount
- `Location` - Purchase location
- `Size` - Product size
- `Color` - Product color
- `Season` - Purchase season
- `Review Rating` - Customer rating (1-5)
- `Subscription Status` - Yes/No
- `Shipping Type` - Shipping method
- `Discount Applied` - Yes/No
- `Promo Code Used` - Yes/No
- `Previous Purchases` - Number of previous orders
- `Payment Method` - Payment type
- `Frequency of Purchases` - Purchase frequency category

## 🎯 Usage Guide

### Filtering Data
Use the sidebar filters to segment your data:
- **Gender**: Select specific genders
- **Age Range**: Use slider to set age boundaries
- **Location**: Choose specific locations
- **Category**: Filter by product categories
- **Season**: Select seasonal data
- **Payment Method**: Filter by payment types

### Navigating Tabs
1. **Sales Analytics**: Overview of revenue and sales performance
2. **Customer Insights**: Demographic and behavioral analysis
3. **Product Analysis**: Product performance and preferences
4. **Payment & Shipping**: Transaction and logistics metrics
5. **Data Explorer**: Raw data access and export

### Exporting Data
- Navigate to the "Data Explorer" tab
- Click "Download Filtered Data as CSV" to export current filtered view

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended for Free Hosting)

1. **Create a GitHub repository** with your code
2. **Push your files** (dashboard.py and dataset folder)
3. **Go to** [share.streamlit.io](https://share.streamlit.io)
4. **Sign in** with GitHub
5. **Deploy** by selecting your repository
6. Your dashboard will be live at: `https://your-app.streamlit.app`

**Important for Streamlit Cloud:**
- Create a `requirements.txt` file:
```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
numpy>=1.24.0
```

### Option 2: Heroku

1. **Create a Heroku account** at [heroku.com](https://heroku.com)
2. **Install Heroku CLI**
3. **Create required files:**

`requirements.txt`:
```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
numpy>=1.24.0
```

`setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

`Procfile`:
```
web: sh setup.sh && streamlit run dashboard.py
```

4. **Deploy**:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### Option 3: AWS EC2

1. Launch an EC2 instance (Ubuntu recommended)
2. SSH into your instance
3. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip
pip3 install streamlit pandas plotly numpy
```
4. Upload your files
5. Run with nohup:
```bash
nohup streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0 &
```
6. Configure security group to allow port 8501

### Option 4: Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t shopping-dashboard .
docker run -p 8501:8501 shopping-dashboard
```

## 🎨 Customization

### Changing Colors
Edit the CSS gradient colors in the dashboard.py file:
```python
# Look for these sections:
.kpi-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Adding New Metrics
Add custom KPIs in the metrics section:
```python
with col6:
    custom_metric = filtered_df['YourColumn'].sum()
    st.metric(
        label="📊 Your Metric",
        value=f"{custom_metric:,.0f}",
        delta="Change description"
    )
```

### Adding New Visualizations
Use Plotly Express to create new charts:
```python
fig = px.bar(your_data, x='column1', y='column2')
st.plotly_chart(fig, use_container_width=True)
```

## 📊 Sample Insights You Can Derive

1. **Revenue Trends**: Identify top-performing categories and seasons
2. **Customer Segments**: Understand different customer value tiers
3. **Product Performance**: Track best-sellers and customer preferences
4. **Marketing Effectiveness**: Measure discount and promo code impact
5. **Geographic Analysis**: Identify high-value locations
6. **Payment Patterns**: Understand preferred payment methods
7. **Subscription Value**: Compare subscriber vs non-subscriber behavior
8. **Customer Retention**: Track repeat purchase patterns

## 🔧 Troubleshooting

### Dashboard won't load
- Check that your CSV file path is correct
- Verify all required columns exist in your dataset
- Ensure Python packages are installed

### Slow performance
- Reduce the dataset size for testing
- Use `@st.cache_data` decorator (already implemented)
- Filter data before creating visualizations

### Deployment issues
- For Streamlit Cloud: Check your repository is public
- For Heroku: Verify Procfile and requirements.txt are correct
- For AWS: Check security group rules allow inbound traffic on port 8501

## 📝 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Feel free to fork, modify, and enhance this dashboard. Contributions are welcome!

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
3. Plotly documentation: [plotly.com/python](https://plotly.com/python/)

## 🎯 Roadmap

Future enhancements:
- [ ] Real-time data integration
- [ ] Predictive analytics with ML models
- [ ] Advanced customer segmentation (RFM analysis)
- [ ] Email report scheduling
- [ ] Multi-language support
- [ ] Dark mode toggle
- [ ] Custom date range filters
- [ ] Export to PDF reports

---

**Built with ❤️ using Streamlit and Plotly**

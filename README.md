# Personal Habit Tracking Dashboard

A Streamlit-based dashboard for tracking habits and personal metrics, with automated weekly reminders and progress visualization.

## 🎯 Project Overview

This dashboard connects to Google Sheets or Notion databases to visualize personal habits, track progress, and send weekly updates to keep you accountable. Built with Streamlit for rapid development and easy deployment.

## 🚀 Tech Stack

### Core Framework
- **Streamlit** - Python-based web app framework for data dashboards
- **Python 3.8+** - Backend logic and data processing
- **Pandas** - Data manipulation and analysis

### Essential Libraries

#### Data & Visualization
- **Plotly** - Interactive charts and visualizations
- **Altair** - Declarative visualization grammar
- **Matplotlib/Seaborn** - Additional plotting options
- **Streamlit-extras** - Additional components

#### Data Processing
- **NumPy** - Numerical computations
- **datetime** - Date manipulation for habit tracking

#### Integrations
- **gspread** - Google Sheets API wrapper
- **google-auth** - Authentication for Google services
- **notion-client** - Official Notion SDK for Python

#### Scheduling & Notifications
- **schedule** - Weekly reminder automation
- **smtplib** - Email notifications
- **streamlit-autorefresh** - Auto-refresh dashboard data

### Development Tools
- **Poetry** or **pip** - Package management
- **Black** - Code formatting
- **Pylint** - Code quality
- **python-dotenv** - Environment variables

## 🏗️ Project Structure

```
habit-dashboard/
├── app.py                 # Main Streamlit application
├── pages/                 # Multi-page app structure
│   ├── 1_📊_Overview.py
│   ├── 2_📈_Analytics.py
│   └── 3_⚙️_Settings.py
├── components/            # Reusable UI components
│   ├── habit_card.py
│   ├── charts.py
│   └── metrics.py
├── data/                  # Data processing modules
│   ├── google_sheets.py
│   ├── notion_api.py
│   └── processors.py
├── utils/                 # Helper functions
│   ├── calculations.py
│   ├── notifications.py
│   └── date_helpers.py
├── config/               # Configuration files
│   └── settings.py
├── .streamlit/           # Streamlit config
│   └── config.toml
├── requirements.txt      # Dependencies
└── .env                 # Environment variables
```

## 💡 AI-Assisted Development Tips

### Component Generation
```bash
# Describe to AI:
"Create a Streamlit component that shows:
- Habit name with emoji icon
- Current streak in a metric display
- Completion percentage with progress bar
- Last 7 days mini chart
Using st.columns and Plotly for visualization"
```

### Data Processing Patterns
```bash
# Ask AI for:
"Google Sheets integration with Streamlit
- Authenticate using service account
- Cache data for 5 minutes
- Convert to pandas DataFrame
- Handle connection errors"
```

### Quick Wins with AI
1. **Layout Generation**: "Create a Streamlit dashboard layout with sidebar filters and main metrics grid"
2. **Data Calculations**: "Calculate habit streaks from DataFrame with date and completion columns"
3. **Chart Creation**: "Plotly heatmap for habit completion by day and week"
4. **State Management**: "Implement session state for user preferences and filters"

## 🎨 UI Component Patterns

### Essential Dashboard Components

#### Metric Cards
```python
def display_metric_card(title, value, delta=None, help_text=None):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.metric(title, value, delta, help=help_text)
    with col2:
        st.plotly_chart(mini_sparkline, use_container_width=True)
```

#### Habit Grid
```python
# Responsive grid using columns
habits_per_row = 3
for i in range(0, len(habits), habits_per_row):
    cols = st.columns(habits_per_row)
    for j, habit in enumerate(habits[i:i+habits_per_row]):
        with cols[j]:
            render_habit_card(habit)
```

#### Interactive Filters
```python
# Sidebar filters
with st.sidebar:
    date_range = st.date_input("Date Range", [])
    selected_categories = st.multiselect("Categories", categories)
    view_type = st.radio("View", ["Daily", "Weekly", "Monthly"])
```

## 📊 Data Structure Recommendations

### Habit Schema
```python
# DataFrame columns for habits
HABIT_COLUMNS = [
    'id',
    'name',
    'category',
    'target_frequency',  # daily, weekly, monthly
    'color',
    'emoji_icon'
]

# DataFrame columns for habit logs
LOG_COLUMNS = [
    'habit_id',
    'date',
    'completed',
    'notes',
    'value'  # For measurable habits
]
```

### Data Processing Functions
```python
def calculate_streak(habit_logs):
    """Calculate current streak for a habit"""
    # Sort by date descending
    # Count consecutive True values
    # Return streak count

def get_completion_rate(habit_logs, period='week'):
    """Calculate completion percentage for period"""
    # Filter logs by period
    # Calculate percentage
    # Return rate
```

## 🚦 Performance Best Practices

### Caching Strategy
```python
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_habits_data():
    return fetch_from_google_sheets()

@st.cache_resource
def init_google_sheets_client():
    return authenticate_google_sheets()
```

### State Management
```python
# Initialize session state
if 'selected_habit' not in st.session_state:
    st.session_state.selected_habit = None

# Update state on user interaction
if st.button("Select Habit"):
    st.session_state.selected_habit = habit_id
```

### Optimization Tips
1. Use `st.cache_data` for data fetching
2. Implement `st.fragment` for partial updates
3. Use `use_container_width=True` for responsive charts
4. Batch API calls to external services
5. Pre-calculate metrics during data load

## 🔧 Streamlit Configuration

### .streamlit/config.toml
```toml
[theme]
primaryColor = "#7C3AED"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
enableCORS = false
port = 8501

[browser]
gatherUsageStats = false
```

## 📖 Key Resources

### Documentation
- [Streamlit Docs](https://docs.streamlit.io) - Official documentation
- [Plotly Python](https://plotly.com/python/) - Interactive visualizations
- [Pandas Docs](https://pandas.pydata.org/docs/) - Data manipulation
- [Google Sheets API](https://developers.google.com/sheets/api) - Sheets integration

### Streamlit-Specific Resources
- [Streamlit Gallery](https://streamlit.io/gallery) - Example apps
- [Streamlit Components](https://streamlit.io/components) - Extended functionality
- [Awesome Streamlit](https://github.com/MarcSkovMadsen/awesome-streamlit) - Curated resources

## 🎯 MVP Feature Checklist

- [ ] Google Sheets/Notion connection setup
- [ ] Main dashboard with key metrics
- [ ] Habit cards with completion tracking
- [ ] Interactive date range selector
- [ ] Streak calculations and display
- [ ] Progress charts (line, bar, heatmap)
- [ ] Category filtering
- [ ] Data export functionality
- [ ] Auto-refresh capability
- [ ] Weekly summary statistics
- [ ] Email reminder configuration
- [ ] Mobile-responsive layout

## 🚀 Getting Started

```bash
# Create project directory
mkdir habit-dashboard && cd habit-dashboard

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install streamlit pandas plotly gspread google-auth
pip install streamlit-extras python-dotenv altair

# Create main app file
touch app.py

# Run the app
streamlit run app.py
```

### Initial App Structure
```python
# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Habit Tracker",
    page_icon="📊",
    layout="wide"
)

st.title("🎯 Personal Habit Tracker")

# Sidebar
with st.sidebar:
    st.header("Filters")
    date_range = st.date_input(
        "Select Date Range",
        value=(datetime.now() - timedelta(days=30), datetime.now())
    )

# Main content
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Active Habits", "12", "+2")
with col2:
    st.metric("Completion Rate", "78%", "+5%")
with col3:
    st.metric("Current Streak", "7 days", "+1")
with col4:
    st.metric("Best Streak", "21 days")

# Habit grid
st.subheader("Today's Habits")
# Add your habit components here
```

## 💬 AI Prompt Templates

### For Building Features
"Create a Streamlit function that [specific functionality] using pandas for data processing and plotly for visualization. Include error handling and use st.cache_data for performance."

### For Data Processing
"Write a Python function that calculates [metric] from a pandas DataFrame containing habit logs. Include docstrings and handle edge cases."

### For Visualizations
"Create a Plotly [chart type] in Streamlit that shows [data insight]. Make it interactive and use custom colors. Include proper labels and formatting."

### For Integration
"Show how to connect Streamlit to [Google Sheets/Notion] with proper authentication, error handling, and data caching. Include environment variable setup."

---

Remember: Streamlit's simplicity allows you to focus on data logic and visualization rather than frontend complexity. Use your backend skills to create robust data pipelines while Streamlit handles the UI. Let AI help with boilerplate code and focus on creating insights from your habit data.

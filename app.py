import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Personal Habit Tracker",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }
    .goal-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .habit-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-bottom: 0.5rem;
        cursor: pointer;
    }
    .habit-card:hover {
        background-color: #f8f9fa;
        border-color: #7c3aed;
    }
    .selected-habit {
        background-color: #7c3aed !important;
        color: white !important;
        border-color: #7c3aed !important;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_habit' not in st.session_state:
    st.session_state.selected_habit = None

if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'dashboard'

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Sample data (placeholder)
SAMPLE_HABITS = [
    {"id": 1, "name": "Morning Run", "category": "Fitness", "emoji": "🏃‍♂️", "status": "completed", "streak": 7},
    {"id": 2, "name": "Meditation", "category": "Mindfulness", "emoji": "🧘‍♀️", "status": "completed", "streak": 12},
    {"id": 3, "name": "Read 30 Pages", "category": "Learning", "emoji": "📚", "status": "in_progress", "streak": 3},
    {"id": 4, "name": "Drink Water", "category": "Health", "emoji": "💧", "status": "pending", "streak": 5},
    {"id": 5, "name": "Guitar Practice", "category": "Learning", "emoji": "🎸", "status": "pending", "streak": 2},
    {"id": 6, "name": "Journal", "category": "Mindfulness", "emoji": "📝", "status": "pending", "streak": 15}
]

# Password protection
if not st.session_state.authenticated:
    st.markdown('<h1 class="main-header">🔐 Access Required</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        background-color: #f8f9fa;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        text-align: center;
    ">
        <h3 style="color: #2c3e50; margin-bottom: 1rem;">🎯 Personal Habit Tracker</h3>
        <p style="color: #6c757d; margin-bottom: 1.5rem;">Please enter the password to access your dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the password input
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        password = st.text_input("Password:", type="password", placeholder="Enter password")
        
        if st.button("🔓 Access Dashboard", use_container_width=True, type="primary"):
            if password == "pass8":
                st.session_state.authenticated = True
                st.success("✅ Access granted! Welcome to your habit tracker.")
                st.rerun()
            else:
                st.error("❌ Incorrect password. Please try again.")
    
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; color: #6c757d; font-size: 0.8rem;">
        <p>🔒 Your habit data is protected</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# Main header
st.markdown('<h1 class="main-header">🎯 Personal Habit Tracker</h1>', unsafe_allow_html=True)

# Goals section at the top
st.markdown("## 🎯 Goals")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid #dee2e6;
    ">
        <h4 style="color: #2c3e50; margin-bottom: 1rem;">🎯 Long-term Goals</h4>
        <ul style="color: #34495e; margin: 0; padding-left: 1.2rem;">
            <li style="margin-bottom: 0.5rem;">Build consistent daily routines</li>
            <li style="margin-bottom: 0.5rem;">Improve physical and mental health</li>
            <li style="margin-bottom: 0.5rem;">Develop new skills and knowledge</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid #dee2e6;
    ">
        <h4 style="color: #2c3e50; margin-bottom: 1rem;">⚡ Short-term Goals (This Week)</h4>
        <ul style="color: #34495e; margin: 0; padding-left: 1.2rem;">
            <li style="margin-bottom: 0.5rem;">Complete all habits 5+ days</li>
            <li style="margin-bottom: 0.5rem;">Maintain morning routine streak</li>
            <li style="margin-bottom: 0.5rem;">Focus on consistency over perfection</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Layout: Sidebar for habits, Main area for dashboard
sidebar_col, main_col = st.columns([1, 3])

with sidebar_col:
    st.markdown("### 📋 Habits")
    
    # Logout button at the top of sidebar
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        st.session_state.authenticated = False
        st.rerun()
    
    st.markdown("---")
    
    # Filter options
    categories = list(set([habit["category"] for habit in SAMPLE_HABITS]))
    selected_categories = st.multiselect("Filter by category:", categories, default=categories)
    
    # Status filter
    status_filter = st.selectbox("Filter by status:", ["All", "Completed", "In Progress", "Pending"])
    
    st.markdown("---")
    
    # Habit list
    filtered_habits = SAMPLE_HABITS
    if selected_categories:
        filtered_habits = [h for h in filtered_habits if h["category"] in selected_categories]
    
    if status_filter != "All":
        status_map = {"Completed": "completed", "In Progress": "in_progress", "Pending": "pending"}
        filtered_habits = [h for h in filtered_habits if h["status"] == status_map[status_filter]]
    
    # Dashboard button
    if st.button("🏠 Main Dashboard", use_container_width=True, type="primary" if st.session_state.view_mode == 'dashboard' else "secondary"):
        st.session_state.view_mode = 'dashboard'
        st.session_state.selected_habit = None
        st.rerun()
    
    st.markdown("**Select a habit:**")
    
    for habit in filtered_habits:
        # Status indicator
        status_emoji = {"completed": "✅", "in_progress": "🔄", "pending": "⏳"}
        status_text = status_emoji.get(habit["status"], "⏳")
        
        # Create clickable habit card
        habit_key = f"habit_{habit['id']}"
        button_type = "primary" if st.session_state.selected_habit == habit['id'] else "secondary"
        
        if st.button(
            f"{habit['emoji']} {habit['name']}\n{status_text} Streak: {habit['streak']} days",
            key=habit_key,
            use_container_width=True,
            type=button_type
        ):
            st.session_state.selected_habit = habit['id']
            st.session_state.view_mode = 'habit_detail'
            st.rerun()

with main_col:
    if st.session_state.view_mode == 'dashboard':
        # Main Dashboard View
        st.markdown("### 📊 Dashboard Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Active Habits", "6", "+1")
        
        with col2:
            st.metric("Completion Rate", "67%", "+12%")
        
        with col3:
            st.metric("Current Streak", "7 days", "+1")
        
        with col4:
            st.metric("Best Streak", "21 days", "0")
        
        st.markdown("---")
        
        # Today's Habits
        st.markdown("### 📅 Today's Habits")
        
        # Habit cards in grid
        habit_cols = st.columns(3)
        
        for i, habit in enumerate(SAMPLE_HABITS):
            col_idx = i % 3
            
            with habit_cols[col_idx]:
                # Status styling
                if habit["status"] == "completed":
                    card_color = "#d4edda"
                    border_color = "#c3e6cb"
                elif habit["status"] == "in_progress":
                    card_color = "#fff3cd"
                    border_color = "#ffeaa7"
                else:
                    card_color = "#f8f9fa"
                    border_color = "#dee2e6"
                
                st.markdown(f"""
                <div style="
                    background-color: {card_color};
                    border: 2px solid {border_color};
                    border-radius: 8px;
                    padding: 1rem;
                    margin-bottom: 1rem;
                    text-align: center;
                    color: #2c3e50;
                ">
                    <h4 style="color: #2c3e50; margin-bottom: 0.5rem; font-weight: bold;">{habit['emoji']} {habit['name']}</h4>
                    <p style="color: #34495e; margin: 0.25rem 0; font-size: 0.9rem;"><strong>Category:</strong> {habit['category']}</p>
                    <p style="color: #34495e; margin: 0.25rem 0; font-size: 0.9rem;"><strong>Streak:</strong> {habit['streak']} days</p>
                    <p style="color: #34495e; margin: 0.25rem 0; font-size: 0.9rem;"><strong>Status:</strong> {habit['status'].title()}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Analytics section
        st.markdown("### 📈 Analytics")
        
        # Placeholder charts
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("#### Weekly Progress")
            # Placeholder line chart
            sample_data = pd.DataFrame({
                'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'Completion': [80, 75, 90, 85, 70, 60, 85]
            })
            fig = px.line(sample_data, x='Day', y='Completion', title="Weekly Completion Rate")
            st.plotly_chart(fig, use_container_width=True)
        
        with chart_col2:
            st.markdown("#### Category Distribution")
            # Placeholder pie chart
            category_data = pd.DataFrame({
                'Category': categories,
                'Count': [2, 2, 1, 1]
            })
            fig = px.pie(category_data, values='Count', names='Category', title="Habits by Category")
            st.plotly_chart(fig, use_container_width=True)
        
        # Heatmap placeholder
        st.markdown("#### Habit Completion Heatmap (Last 4 Weeks)")
        st.info("📊 Interactive heatmap showing daily completion status will be displayed here")
        
    else:
        # Individual Habit Detail View
        selected_habit_data = next((h for h in SAMPLE_HABITS if h['id'] == st.session_state.selected_habit), None)
        
        if selected_habit_data:
            st.markdown(f"### {selected_habit_data['emoji']} {selected_habit_data['name']} - Detailed View")
            
            # Habit details
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Current Streak", f"{selected_habit_data['streak']} days")
            
            with col2:
                st.metric("Category", selected_habit_data['category'])
            
            with col3:
                st.metric("Status", selected_habit_data['status'].title())
            
            st.markdown("---")
            
            # Habit-specific analytics
            st.markdown("#### 📊 Progress Analytics")
            
            # Placeholder for detailed charts
            tab1, tab2, tab3 = st.tabs(["📈 Trends", "📅 Calendar", "📝 Notes"])
            
            with tab1:
                st.info("📈 Detailed progress trends will be shown here")
                # Placeholder trend chart
                sample_trend = pd.DataFrame({
                    'Date': pd.date_range(start='2024-06-01', periods=30),
                    'Completed': [1 if i % 3 != 2 else 0 for i in range(30)]
                })
                fig = px.line(sample_trend, x='Date', y='Completed', title=f"{selected_habit_data['name']} - 30 Day Trend")
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                st.info("📅 Calendar view with completion status will be displayed here")
            
            with tab3:
                st.info("📝 Notes and insights for this habit will be shown here")
                st.text_area("Add a note:", placeholder="How did this habit go today?")
                
        else:
            st.error("Habit not found!")

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit • Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M") + "*")
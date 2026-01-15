# LegacyLoop - Main Application
# Bridging the engagement gap between wealthy clients, heirs, and advisors

import streamlit as st
from datetime import datetime

# Import our modules
from data import (
    DEFAULT_PORTFOLIO, USERS, ASSET_TYPES, 
    format_currency, get_total_portfolio_value, 
    add_asset, update_asset, delete_asset
)
import copy
from services import (
    generate_mission_statement,
    generate_heir_content,
    generate_advisor_email,
    is_simulation_mode
)
from ui_components import (
    render_sidebar,
    render_user_header,
    render_legacy_card,
    render_mission_statement,
    render_engagement_log,
    render_metric_card
)

# Page Configuration
st.set_page_config(
    page_title="LegacyLoop",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for overall styling
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
    }
    
    /* Header Styling */
    .main-header {
        text-align: center;
        padding: 20px 0;
        margin-bottom: 30px;
    }
    
    .main-header h1 {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 25px;
        font-weight: 600;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Text Area Styling */
    .stTextArea textarea {
        background: #1a1a2e;
        border: 1px solid #333;
        border-radius: 8px;
        color: #fff;
    }
    
    /* Metric styling for Advisor view */
    .advisor-view {
        background: #f8f9fa;
        border-radius: 16px;
        padding: 20px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize all session state variables"""
    if 'current_role' not in st.session_state:
        st.session_state.current_role = 'primary'
    
    if 'mission_statement' not in st.session_state:
        st.session_state.mission_statement = None
    
    if 'family_values' not in st.session_state:
        st.session_state.family_values = ""
    
    if 'family_goals' not in st.session_state:
        st.session_state.family_goals = ""
    
    if 'engagement_logs' not in st.session_state:
        st.session_state.engagement_logs = []
    
    if 'heir_content_cache' not in st.session_state:
        st.session_state.heir_content_cache = {}
    
    # Initialize portfolio from default if not set
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = copy.deepcopy(DEFAULT_PORTFOLIO)
    
    # Asset management state
    if 'editing_asset_id' not in st.session_state:
        st.session_state.editing_asset_id = None
    
    if 'show_add_asset' not in st.session_state:
        st.session_state.show_add_asset = False


def primary_client_view():
    """View for the Primary Client (Arthur) - Family Mission Builder"""
    render_user_header('primary')
    
    st.markdown("---")
    
    # Get portfolio from session state
    portfolio = st.session_state.portfolio
    
    # Portfolio Overview
    st.markdown("### 💰 Portfolio Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Portfolio Value", format_currency(get_total_portfolio_value(portfolio)))
    with col2:
        st.metric("Asset Classes", len(set(a['type'] for a in portfolio)))
    with col3:
        st.metric("Total Holdings", len(portfolio))
    
    st.markdown("---")
    
    # Asset Management Section
    st.markdown("## 🏦 Portfolio Management")
    st.markdown("*Add, edit, or remove assets from your family portfolio.*")
    
    # Add Asset Button
    col_add, col_spacer = st.columns([1, 4])
    with col_add:
        if st.button("➕ Add New Asset", use_container_width=True):
            st.session_state.show_add_asset = True
            st.session_state.editing_asset_id = None
    
    # Add Asset Form
    if st.session_state.show_add_asset:
        with st.expander("📝 Add New Asset", expanded=True):
            with st.form("add_asset_form"):
                st.markdown("#### New Asset Details")
                
                col1, col2 = st.columns(2)
                with col1:
                    new_name = st.text_input("Asset Name*", placeholder="e.g., Tesla Inc")
                    new_value = st.number_input("Value ($)*", min_value=0, value=100000, step=10000)
                with col2:
                    new_type = st.selectbox("Asset Type*", ASSET_TYPES)
                    new_symbol = st.text_input("Symbol (optional)", placeholder="e.g., TSLA")
                
                new_description = st.text_area("Description", placeholder="Brief description of this asset...")
                
                col_submit, col_cancel = st.columns(2)
                with col_submit:
                    submit = st.form_submit_button("✅ Add Asset", use_container_width=True)
                with col_cancel:
                    cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                
                if submit and new_name:
                    add_asset(portfolio, new_name, new_value, new_type, new_symbol, new_description)
                    st.session_state.show_add_asset = False
                    st.session_state.heir_content_cache = {}  # Clear cache for new asset
                    st.success(f"✅ Added {new_name} to portfolio!")
                    st.rerun()
                elif cancel:
                    st.session_state.show_add_asset = False
                    st.rerun()
    
    # Display Assets with Edit/Delete
    st.markdown("### Current Holdings")
    
    for asset in portfolio:
        asset_id = asset.get('id', 0)
        
        with st.container():
            # Asset display row
            col_info, col_value, col_actions = st.columns([3, 2, 2])
            
            with col_info:
                type_emoji = {'Equities': '📈', 'Index Fund': '📊', 'Bonds': '💵', 'Real Estate': '🏠', 
                             'Cryptocurrency': '🪙', 'Private Equity': '🏢', 'Cash/Savings': '💰', 'Alternative Investments': '💎'}
                emoji = type_emoji.get(asset['type'], '📦')
                st.markdown(f"**{emoji} {asset['name']}**")
                st.caption(f"{asset['type']} {f'({asset.get("symbol", "")})' if asset.get('symbol') else ''}")
            
            with col_value:
                st.markdown(f"### {format_currency(asset['value'])}")
            
            with col_actions:
                col_edit, col_delete = st.columns(2)
                with col_edit:
                    if st.button("✏️", key=f"edit_{asset_id}", help="Edit asset"):
                        st.session_state.editing_asset_id = asset_id
                        st.session_state.show_add_asset = False
                with col_delete:
                    if st.button("🗑️", key=f"delete_{asset_id}", help="Delete asset"):
                        delete_asset(portfolio, asset_id)
                        st.session_state.heir_content_cache = {}
                        st.success(f"Deleted {asset['name']}")
                        st.rerun()
        
        # Edit Form (inline)
        if st.session_state.editing_asset_id == asset_id:
            with st.form(f"edit_form_{asset_id}"):
                st.markdown("#### Edit Asset")
                col1, col2 = st.columns(2)
                with col1:
                    edit_name = st.text_input("Name", value=asset['name'])
                    edit_value = st.number_input("Value ($)", value=asset['value'], min_value=0, step=10000)
                with col2:
                    type_index = ASSET_TYPES.index(asset['type']) if asset['type'] in ASSET_TYPES else 0
                    edit_type = st.selectbox("Type", ASSET_TYPES, index=type_index)
                    edit_symbol = st.text_input("Symbol", value=asset.get('symbol', ''))
                
                edit_description = st.text_area("Description", value=asset.get('description', ''))
                
                col_save, col_cancel = st.columns(2)
                with col_save:
                    save = st.form_submit_button("💾 Save", use_container_width=True)
                with col_cancel:
                    cancel_edit = st.form_submit_button("❌ Cancel", use_container_width=True)
                
                if save:
                    update_asset(portfolio, asset_id, edit_name, edit_value, edit_type, edit_symbol, edit_description)
                    st.session_state.editing_asset_id = None
                    st.session_state.heir_content_cache = {}
                    st.success(f"✅ Updated {edit_name}!")
                    st.rerun()
                elif cancel_edit:
                    st.session_state.editing_asset_id = None
                    st.rerun()
        
        st.markdown("---")
    
    st.markdown("---")
    
    # Family Mission Builder
    st.markdown("## 📜 Family Mission Builder")
    st.markdown("*Define what wealth means to your family and create a lasting legacy statement.*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Core Family Values")
        values = st.text_area(
            "What values do you want to pass down?",
            value=st.session_state.family_values,
            placeholder="e.g., Hard work, education, philanthropy, family unity, integrity...",
            height=150,
            key="values_input"
        )
        st.session_state.family_values = values
    
    with col2:
        st.markdown("#### Vision for Family Wealth")
        goals = st.text_area(
            "What do you want your money to accomplish?",
            value=st.session_state.family_goals,
            placeholder="e.g., Keep the family together, fund grandchildren's education, support charitable causes...",
            height=150,
            key="goals_input"
        )
        st.session_state.family_goals = goals
    
    st.markdown("")
    
    # Generate Mission Statement
    if st.button("✨ Draft Family Constitution", use_container_width=True):
        if not values.strip() or not goals.strip():
            st.error("Please fill in both your values and goals to generate a mission statement.")
        else:
            with st.spinner("Crafting your family's mission statement..."):
                statement = generate_mission_statement(values, goals)
                st.session_state.mission_statement = statement
    
    # Display Mission Statement
    if st.session_state.mission_statement:
        st.markdown("---")
        render_mission_statement(st.session_state.mission_statement)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.toast("Mission statement ready to copy!")
        with col2:
            if st.button("🔄 Regenerate", use_container_width=True):
                with st.spinner("Regenerating..."):
                    statement = generate_mission_statement(
                        st.session_state.family_values,
                        st.session_state.family_goals
                    )
                    st.session_state.mission_statement = statement
                    st.rerun()


def heir_view():
    """View for the Heir (Leo) - Learning Feed with Legacy Cards"""
    render_user_header('heir')
    
    st.markdown("---")
    
    # Show family mission if available
    if st.session_state.mission_statement:
        with st.expander("📜 Your Family's Mission Statement", expanded=False):
            st.markdown(st.session_state.mission_statement)
    
    # Header
    st.markdown("## 🎯 Your Legacy Portfolio")
    st.markdown("*Discover the investments your family has built for generations. Tap to learn more!*")
    
    # Portfolio Value Teaser
    portfolio = st.session_state.portfolio
    total_value = get_total_portfolio_value(portfolio)
    st.info(f"💎 **Total Family Portfolio:** {format_currency(total_value)}")
    
    st.markdown("---")
    
    # Display Legacy Cards
    heir_profile = USERS['heir']
    
    for i, asset in enumerate(portfolio[:5]):  # Show top 5 assets
        asset_name = asset['name']
        
        # Check cache for AI content
        if asset_name not in st.session_state.heir_content_cache:
            if is_simulation_mode():
                # In simulation mode, generate content immediately
                content = generate_heir_content(asset, heir_profile)
                st.session_state.heir_content_cache[asset_name] = content
            else:
                # With API, also generate (could add lazy loading later)
                content = generate_heir_content(asset, heir_profile)
                st.session_state.heir_content_cache[asset_name] = content
        
        explanation = st.session_state.heir_content_cache.get(
            asset_name,
            "Loading explanation..."
        )
        
        render_legacy_card(asset, explanation, show_action=True)
    
    # Engagement Summary
    if st.session_state.engagement_logs:
        st.markdown("---")
        st.success(f"🎉 You've explored {len(st.session_state.engagement_logs)} asset(s)! Sarah will be in touch.")


def advisor_view():
    """View for the Advisor (Sarah) - Pulse Dashboard"""
    render_user_header('advisor')
    
    st.markdown("---")
    
    # Dashboard Header
    st.markdown("## 📊 Heir Engagement Dashboard")
    st.markdown("*Monitor engagement and nurture the next generation relationship.*")
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    logs = st.session_state.engagement_logs
    
    with col1:
        render_metric_card(
            "Total Interactions",
            str(len(logs)),
            "Active" if logs else None,
            "#4CAF50"
        )
    
    with col2:
        unique_assets = len(set(log['asset'] for log in logs)) if logs else 0
        render_metric_card(
            "Assets Explored",
            str(unique_assets),
            None,
            "#2196F3"
        )
    
    with col3:
        # Calculate engagement score (simple formula for prototype)
        score = min(100, len(logs) * 20) if logs else 0
        render_metric_card(
            "Engagement Score",
            f"{score}%",
            "Growing" if score > 0 else None,
            "#FF9800"
        )
    
    with col4:
        client = USERS['primary']['name']
        render_metric_card(
            "Client Family",
            client.split()[0],
            None,
            "#9C27B0"
        )
    
    st.markdown("---")
    
    # Engagement Feed
    st.markdown("### 🔔 Recent Activity Feed")
    
    if not logs:
        st.info("📭 No engagement activity yet. Leo hasn't explored any assets.")
        st.markdown("*Tip: Switch to Leo's view and click 'Ask Advisor' on some assets to see activity here.*")
    else:
        for log in reversed(logs):  # Show most recent first
            render_engagement_log(log)
            
            # Add email draft button
            asset_name = log['asset']
            if st.button(f"✉️ Draft Email about {asset_name}", key=f"email_{log['timestamp']}"):
                with st.spinner("Drafting personalized email..."):
                    email = generate_advisor_email(
                        asset_name,
                        USERS['heir']['name'],
                        USERS['primary']['name']
                    )
                
                st.markdown("#### 📧 Draft Email")
                st.text_area(
                    "Edit and send:",
                    value=email,
                    height=200,
                    key=f"email_content_{log['timestamp']}"
                )
    
    st.markdown("---")
    
    # Client Overview Section
    st.markdown("### 👨‍👩‍👦 Family Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Primary Client")
        primary = USERS['primary']
        st.markdown(f"""
        **{primary['avatar']} {primary['name']}**  
        Age: {primary['age']}  
        {primary['bio']}
        """)
    
    with col2:
        st.markdown("#### Heir")
        heir = USERS['heir']
        st.markdown(f"""
        **{heir['avatar']} {heir['name']}**  
        Age: {heir['age']}  
        Interests: {', '.join(heir['interests'])}  
        Financial Literacy: {heir['fin_lit_level']}
        """)
    
    # Mission Statement (if exists)
    if st.session_state.mission_statement:
        st.markdown("---")
        st.markdown("### 📜 Family Mission Statement")
        with st.expander("View Statement", expanded=False):
            st.markdown(st.session_state.mission_statement)


def main():
    """Main application entry point"""
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar (this sets current_role)
    render_sidebar()
    
    # App Header
    st.markdown("""
    <div class="main-header">
        <h1>🔄 LegacyLoop</h1>
        <p style="color: #888;">Bridging Generations Through Wealth Understanding</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Route to appropriate view
    current_role = st.session_state.current_role
    
    if current_role == 'primary':
        primary_client_view()
    elif current_role == 'heir':
        heir_view()
    elif current_role == 'advisor':
        advisor_view()
    else:
        st.error("Unknown role selected")


if __name__ == "__main__":
    main()

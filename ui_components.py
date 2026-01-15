# LegacyLoop - Reusable UI Components
# Styled widgets for consistent look and feel across views

import streamlit as st
from datetime import datetime
from data import USERS, format_currency


def render_sidebar():
    """Render the sidebar with role switcher and API key input"""
    with st.sidebar:
        st.markdown("## 🔄 LegacyLoop Dev Mode")
        st.markdown("---")
        
        # Role Selector
        role_options = [
            "Primary Client (Arthur)",
            "Heir (Leo)",
            "Advisor (Sarah)"
        ]
        
        selected_role = st.selectbox(
            "👤 Switch View",
            role_options,
            key="role_selector"
        )
        
        # Map selection to role key
        role_map = {
            "Primary Client (Arthur)": "primary",
            "Heir (Leo)": "heir",
            "Advisor (Sarah)": "advisor"
        }
        st.session_state.current_role = role_map[selected_role]
        
        st.markdown("---")
        
        # API Key Input
        st.markdown("### 🔑 API Configuration")
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            key="gemini_api_key",
            help="Enter your Google Gemini API key. Leave empty for simulation mode."
        )
        
        # Check for API key in both text input and secrets
        has_api_key = bool(api_key)
        if not has_api_key:
            try:
                if "GEMINI_API_KEY" in st.secrets:
                    has_api_key = True
            except Exception:
                pass
        
        if not has_api_key:
            st.warning("⚡ **Simulation Mode**\nUsing mock AI responses")
        else:
            st.success("✅ API Key configured")
        
        st.markdown("---")
        
        # Session State Debug
        with st.expander("🔧 Debug Info"):
            st.write("**Session State Keys:**")
            for key in st.session_state:
                if key not in ['gemini_api_key']:
                    st.write(f"- {key}")
            
            if 'engagement_logs' in st.session_state:
                st.write(f"\n**Engagement Logs:** {len(st.session_state.engagement_logs)}")


def render_user_header(role: str):
    """Render the current user header"""
    user = USERS.get(role, USERS['primary'])
    
    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown(f"<h1 style='margin:0;'>{user['avatar']}</h1>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"### {user['name']}")
        st.caption(f"{user['role']} • {user.get('bio', '')[:60]}...")


def render_legacy_card(asset: dict, explanation: str, show_action: bool = True):
    """
    Render a TikTok-style Legacy Card for an asset.
    
    Args:
        asset: Asset dictionary with name, value, type
        explanation: AI-generated explanation
        show_action: Whether to show the "Ask Advisor" button
    """
    asset_name = asset.get('name', 'Unknown Asset')
    asset_type = asset.get('type', 'Investment')
    asset_value = asset.get('value', 0)
    
    # Type-based color coding
    color_map = {
        'Equities': '#4CAF50',
        'Index Fund': '#2196F3',
        'Bonds': '#9C27B0',
        'Real Estate': '#FF9800'
    }
    accent_color = color_map.get(asset_type, '#607D8B')
    
    # Card HTML
    card_html = f"""
    <div style="
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-left: 4px solid {accent_color};
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span style="
                background: {accent_color}33;
                color: {accent_color};
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
            ">{asset_type}</span>
            <span style="color: #aaa; font-size: 14px;">{format_currency(asset_value)}</span>
        </div>
        <h3 style="color: #fff; margin: 10px 0; font-size: 20px;">{asset_name}</h3>
        <p style="color: #ccc; line-height: 1.6; font-size: 14px;">{explanation}</p>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    if show_action:
        if st.button(f"💬 Ask Advisor about this", key=f"ask_{asset_name}"):
            # Log the engagement
            log_entry = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'heir': USERS['heir']['name'],
                'action': 'Asked Advisor',
                'asset': asset_name,
                'asset_type': asset_type
            }
            
            if 'engagement_logs' not in st.session_state:
                st.session_state.engagement_logs = []
            
            st.session_state.engagement_logs.append(log_entry)
            st.success(f"✅ Your interest in **{asset_name}** has been shared with Sarah!")
            st.balloons()


def render_mission_statement(statement: str):
    """Render the family mission statement in a styled container"""
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    ">
        <h2 style="color: #fff; margin-bottom: 20px; text-align: center;">📜 Family Mission Statement</h2>
        <div style="
            background: rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 20px;
            color: #fff;
            line-height: 1.8;
            font-size: 16px;
        ">
    """, unsafe_allow_html=True)
    
    st.markdown(statement)
    
    st.markdown("</div></div>", unsafe_allow_html=True)


def render_engagement_log(log: dict):
    """Render a single engagement log entry"""
    timestamp = log.get('timestamp', 'Unknown time')
    heir = log.get('heir', 'Unknown')
    action = log.get('action', 'Viewed')
    asset = log.get('asset', 'Unknown asset')
    asset_type = log.get('asset_type', 'Investment')
    
    st.markdown(f"""
    <div style="
        background: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border-left: 3px solid #4CAF50;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong style="color: #333;">🔔 {heir}</strong>
                <span style="color: #666;"> {action.lower()} regarding </span>
                <strong style="color: #1976D2;">{asset}</strong>
            </div>
            <span style="color: #888; font-size: 12px;">🕐 {timestamp}</span>
        </div>
        <div style="margin-top: 8px;">
            <span style="
                background: #e3f2fd;
                color: #1976D2;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 11px;
            ">{asset_type}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, delta: str = None, color: str = "#4CAF50"):
    """Render a styled metric card"""
    delta_html = ""
    if delta:
        delta_html = f'<span style="color: {color}; font-size: 14px;">↑ {delta}</span>'
    
    st.markdown(f"""
    <div style="
        background: #fff;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-top: 3px solid {color};
    ">
        <p style="color: #666; margin: 0; font-size: 14px;">{label}</p>
        <h2 style="color: #333; margin: 10px 0;">{value}</h2>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

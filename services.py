# LegacyLoop - AI Services Layer
# Handles all Gemini API interactions with graceful fallbacks

import streamlit as st

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

# Fallback responses for simulation mode
FALLBACK_RESPONSES = {
    'mission_statement': """**The Moneybags Family Mission Statement**

We believe that wealth is not merely a number, but a responsibility and an opportunity to create lasting positive impact. Our family commits to the values of hard work, continuous education, and meaningful philanthropy.

We pledge to use our resources to keep our family united across generations, to empower each member to pursue their fullest potential, and to leave the world better than we found it. This is our legacy.""",
    
    'heir_content': """Did you know? This investment has been carefully chosen by your family to build long-term wealth. Like planting a tree that grows for decades, this asset is designed to appreciate over time while providing stability. Your grandfather Arthur sees this as part of building something that lasts beyond any one generation - a financial foundation for your future dreams!""",
    
    'advisor_email': """Hi Leo,

I noticed you were checking out some of the family investments - that's awesome! Your grandfather Arthur has always been passionate about this particular holding, and I'd love to share some of the story behind it.

No pressure at all, but if you ever want to grab a coffee and chat about how these investments fit into your own goals, I'm here. Whether it's questions about tech stocks or just understanding the basics, I've got your back.

Best,
Sarah"""
}


def get_api_key():
    """Get API key from session state or secrets"""
    # First check session state (user-provided key)
    if 'gemini_api_key' in st.session_state and st.session_state.gemini_api_key:
        return st.session_state.gemini_api_key
    
    # Then check secrets file (Streamlit secrets uses attribute/key access, not .get())
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    
    return None


def get_gemini_response(prompt: str, model: str = "gemini-2.0-flash") -> str:
    """
    Get response from Gemini API with graceful fallback.
    
    Args:
        prompt: The prompt to send to Gemini
        model: The model to use (default: gemini-2.0-flash)
    
    Returns:
        Generated text response or fallback string
    """
    api_key = get_api_key()
    
    if not GENAI_AVAILABLE:
        return "[Simulation Mode] google-generativeai package not installed."
    
    if not api_key:
        return None  # Return None to trigger fallback handling
    
    try:
        genai.configure(api_key=api_key)
        model_instance = genai.GenerativeModel(model)
        response = model_instance.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[API Error] {str(e)}"


def generate_mission_statement(values: str, goals: str) -> str:
    """
    Generate a Family Mission Statement based on values and goals.
    
    Args:
        values: Core family values (e.g., "Hard work, education, philanthropy")
        goals: What the client wants their money to do
    
    Returns:
        Formatted mission statement
    """
    prompt = f"""You are a specialized wealth consultant helping ultra-high-net-worth families articulate their legacy.

Based on these inputs from the family patriarch:

**Core Family Values:** {values}

**Vision for the Family Wealth:** {goals}

Draft a formal yet warm 3-paragraph Family Mission Statement that:
1. Opens with a powerful statement about what wealth means to this family
2. Articulates the core values and how they guide financial decisions
3. Closes with a forward-looking pledge about legacy and future generations

Keep it inspiring, authentic, and avoid generic platitudes. Make it feel personal to THIS family."""
    
    response = get_gemini_response(prompt)
    
    if response is None:
        return FALLBACK_RESPONSES['mission_statement']
    
    return response


def generate_heir_content(asset: dict, heir_profile: dict) -> str:
    """
    Generate educational content about an asset tailored to the heir's profile.
    
    Args:
        asset: Asset dictionary with name, value, type, etc.
        heir_profile: Heir's profile with age, interests, fin_lit_level
    
    Returns:
        Engaging explanation of the asset
    """
    asset_name = asset.get('name', 'Unknown Asset')
    asset_type = asset.get('type', 'Investment')
    asset_value = asset.get('value', 0)
    
    age = heir_profile.get('age', 22)
    interests = ', '.join(heir_profile.get('interests', ['general topics']))
    
    prompt = f"""You are creating educational financial content for young adults who are inheriting wealth.

Explain the asset '{asset_name}' (a {asset_type} worth ${asset_value:,}) to a {age}-year-old who is interested in {interests}.

Rules:
- Explain why a wealthy family might own this for the long term
- Connect it to concepts they'd understand (gaming, tech, social media analogies welcome)
- Do NOT use financial jargon - explain like talking to a smart friend
- Keep it under 100 words
- Make it sound like a "Did you know?" fun fact
- End with something that sparks curiosity

Start directly with the content, no preamble."""
    
    response = get_gemini_response(prompt)
    
    if response is None:
        return FALLBACK_RESPONSES['heir_content']
    
    return response


def generate_advisor_email(asset_name: str, heir_name: str, client_name: str) -> str:
    """
    Generate a casual outreach email from advisor to heir.
    
    Args:
        asset_name: The asset the heir showed interest in
        heir_name: Name of the heir
        client_name: Name of the primary client (grandfather/parent)
    
    Returns:
        Draft email text
    """
    prompt = f"""You are Sarah Jenkins, a financial advisor who has managed {client_name}'s wealth for 15 years.

Draft a short, casual email to {heir_name} (the heir) who just expressed interest in learning about '{asset_name}'.

Guidelines:
- Keep it warm and low-pressure - you're building a relationship, not selling
- Mention that {client_name} (their grandfather) has always been passionate about this investment
- Offer to explain more over coffee or a quick call
- Sound like a friendly mentor, not a stiff banker
- Keep it under 100 words
- Sign off as "Sarah"

Write only the email body, no subject line."""
    
    response = get_gemini_response(prompt)
    
    if response is None:
        return FALLBACK_RESPONSES['advisor_email'].replace('Leo', heir_name)
    
    return response


def is_simulation_mode() -> bool:
    """Check if we're running in simulation mode (no API key)"""
    return get_api_key() is None

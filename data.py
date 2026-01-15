# LegacyLoop - Mock Data
# Contains portfolio assets, user profiles, and engagement tracking

from datetime import datetime

# Portfolio Assets - Diverse wealth holdings
PORTFOLIO = [
    {
        'symbol': 'AAPL',
        'name': 'Apple Inc',
        'value': 250000,
        'type': 'Equities',
        'description': 'Technology company known for iPhone and innovative products'
    },
    {
        'symbol': 'VTSAX',
        'name': 'Vanguard Total Stock Market Index',
        'value': 1000000,
        'type': 'Index Fund',
        'description': 'Broad market exposure across thousands of US companies'
    },
    {
        'symbol': 'BND',
        'name': 'Vanguard Total Bond Market ETF',
        'value': 500000,
        'type': 'Bonds',
        'description': 'Investment-grade bonds for stable income'
    },
    {
        'name': 'Family Vacation Home - Hamptons',
        'value': 3000000,
        'type': 'Real Estate',
        'description': 'Beachfront property owned by the family for 25 years'
    },
    {
        'symbol': 'GOOGL',
        'name': 'Alphabet Inc',
        'value': 350000,
        'type': 'Equities',
        'description': 'Parent company of Google and YouTube'
    },
    {
        'name': 'Commercial Real Estate - Manhattan',
        'value': 2500000,
        'type': 'Real Estate',
        'description': 'Office building in midtown producing rental income'
    },
    {
        'symbol': 'MSFT',
        'name': 'Microsoft Corporation',
        'value': 400000,
        'type': 'Equities',
        'description': 'Enterprise software and cloud computing leader'
    }
]

# User Profiles
USERS = {
    'primary': {
        'name': 'Arthur P. Moneybags',
        'age': 65,
        'role': 'Primary Client',
        'avatar': '👴',
        'bio': 'Self-made entrepreneur, founded a manufacturing company at 28. Passionate about family legacy and philanthropy.'
    },
    'heir': {
        'name': 'Leo Moneybags',
        'age': 22,
        'role': 'Heir',
        'avatar': '👦',
        'interests': ['Tech', 'Gaming', 'Startups', 'Crypto'],
        'fin_lit_level': 'Low',
        'bio': 'Recent college graduate interested in technology and gaming. Just starting to learn about the family wealth.'
    },
    'advisor': {
        'name': 'Sarah Jenkins',
        'role': 'Financial Advisor',
        'avatar': '👩‍💼',
        'firm': 'Jenkins Wealth Management',
        'credentials': 'CFP®, CFA',
        'bio': 'Managing the Moneybags family wealth for 15 years. Specializes in multi-generational planning.'
    }
}

# Engagement Logs - Tracks heir interactions
# This will be populated via session state in the app
INITIAL_ENGAGEMENT_LOGS = []

def get_total_portfolio_value():
    """Calculate total portfolio value"""
    return sum(asset['value'] for asset in PORTFOLIO)

def format_currency(value):
    """Format value as currency string"""
    return f"${value:,.0f}"

def get_asset_by_name(name):
    """Find an asset by its name"""
    for asset in PORTFOLIO:
        if asset['name'] == name:
            return asset
    return None

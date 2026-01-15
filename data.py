# LegacyLoop - Mock Data
# Contains portfolio assets, user profiles, and engagement tracking

from datetime import datetime

# Asset Type Options
ASSET_TYPES = [
    'Equities',
    'Index Fund',
    'Bonds',
    'Real Estate',
    'Cryptocurrency',
    'Private Equity',
    'Cash/Savings',
    'Alternative Investments'
]

# Portfolio Assets - Diverse wealth holdings (initial/default data)
DEFAULT_PORTFOLIO = [
    {
        'id': 1,
        'symbol': 'AAPL',
        'name': 'Apple Inc',
        'value': 250000,
        'type': 'Equities',
        'description': 'Technology company known for iPhone and innovative products'
    },
    {
        'id': 2,
        'symbol': 'VTSAX',
        'name': 'Vanguard Total Stock Market Index',
        'value': 1000000,
        'type': 'Index Fund',
        'description': 'Broad market exposure across thousands of US companies'
    },
    {
        'id': 3,
        'symbol': 'BND',
        'name': 'Vanguard Total Bond Market ETF',
        'value': 500000,
        'type': 'Bonds',
        'description': 'Investment-grade bonds for stable income'
    },
    {
        'id': 4,
        'symbol': '',
        'name': 'Family Vacation Home - Hamptons',
        'value': 3000000,
        'type': 'Real Estate',
        'description': 'Beachfront property owned by the family for 25 years'
    },
    {
        'id': 5,
        'symbol': 'GOOGL',
        'name': 'Alphabet Inc',
        'value': 350000,
        'type': 'Equities',
        'description': 'Parent company of Google and YouTube'
    },
    {
        'id': 6,
        'symbol': '',
        'name': 'Commercial Real Estate - Manhattan',
        'value': 2500000,
        'type': 'Real Estate',
        'description': 'Office building in midtown producing rental income'
    },
    {
        'id': 7,
        'symbol': 'MSFT',
        'name': 'Microsoft Corporation',
        'value': 400000,
        'type': 'Equities',
        'description': 'Enterprise software and cloud computing leader'
    }
]

# Keep PORTFOLIO as a reference (will be replaced by session state in app)
PORTFOLIO = DEFAULT_PORTFOLIO.copy()

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


def get_total_portfolio_value(portfolio=None):
    """Calculate total portfolio value"""
    if portfolio is None:
        portfolio = PORTFOLIO
    return sum(asset['value'] for asset in portfolio)


def format_currency(value):
    """Format value as currency string"""
    return f"${value:,.0f}"


def get_asset_by_name(name, portfolio=None):
    """Find an asset by its name"""
    if portfolio is None:
        portfolio = PORTFOLIO
    for asset in portfolio:
        if asset['name'] == name:
            return asset
    return None


def get_asset_by_id(asset_id, portfolio):
    """Find an asset by its ID"""
    for asset in portfolio:
        if asset.get('id') == asset_id:
            return asset
    return None


def get_next_asset_id(portfolio):
    """Get the next available asset ID"""
    if not portfolio:
        return 1
    return max(asset.get('id', 0) for asset in portfolio) + 1


def add_asset(portfolio, name, value, asset_type, symbol='', description=''):
    """Add a new asset to the portfolio"""
    new_asset = {
        'id': get_next_asset_id(portfolio),
        'symbol': symbol,
        'name': name,
        'value': value,
        'type': asset_type,
        'description': description
    }
    portfolio.append(new_asset)
    return new_asset


def update_asset(portfolio, asset_id, name=None, value=None, asset_type=None, symbol=None, description=None):
    """Update an existing asset"""
    for asset in portfolio:
        if asset.get('id') == asset_id:
            if name is not None:
                asset['name'] = name
            if value is not None:
                asset['value'] = value
            if asset_type is not None:
                asset['type'] = asset_type
            if symbol is not None:
                asset['symbol'] = symbol
            if description is not None:
                asset['description'] = description
            return asset
    return None


def delete_asset(portfolio, asset_id):
    """Delete an asset from the portfolio"""
    for i, asset in enumerate(portfolio):
        if asset.get('id') == asset_id:
            return portfolio.pop(i)
    return None


"""
Improved Configuration Template for MT5 Scalping Bot
=====================================================

Optimized for ACY Securities ProZero Account
- Zero spread pairs
- $6 commission per lot (round-turn)
- Professional risk management
"""

CONFIG = {
    # MT5 Connection
    'mt5_login': 12345,  # Your MT5 account number
    'mt5_password': 'YOUR_PASSWORD_HERE',
    'mt5_server': 'ACYSecurities-Demo',  # or 'ACYSecurities-Live'
    
    # Trading Symbols - Focus on major pairs with zero spread
    'symbols': [
        # Major Forex Pairs (zero spread on ACY ProZero)
        'EURUSD',
        'GBPUSD', 
        'USDJPY',
        'AUDUSD',
        # Add more pairs as needed, but start with 2-4 for testing
    ],
    
    # Risk Management (CRITICAL - DO NOT CHANGE WITHOUT UNDERSTANDING)
    'risk_per_trade': 0.01,  # 1% risk per trade (industry standard)
    'max_concurrent_trades': 3,  # Maximum 3 positions at once
    'max_daily_loss': 0.03,  # Stop trading if -3% daily loss
    
    # Broker-Specific Settings (ACY ProZero)
    'commission_per_lot': 6,  # $6 USD per lot (round-turn)
    
    # Signal Settings
    'min_confidence': 70,  # Minimum confidence to execute trade (70-80 recommended)
    
    # Timeframe
    'timeframe': 'M5',  # M5 recommended for scalping
    
    # Position Limits
    'min_margin_level': 1000,  # Conservative: Stop trading if margin < 1000%
    
    # Scanning
    'check_interval': 60,  # Scan every 60 seconds
    
    # Debug
    'debug_mode': True,  # Show detailed analysis
}

"""
IMPORTANT NOTES FOR ACY PROZERO ACCOUNT:

1. ZERO SPREAD ADVANTAGE:
   - Your account has 0.0 pip spreads on major pairs
   - This saves ~40% on transaction costs vs regular accounts
   - Commission is fixed at $6 per lot (both open and close)
   
2. RISK MANAGEMENT:
   - 1% risk per trade means:
     * $10,000 account = max $100 risk per trade
     * $100,000 account = max $1,000 risk per trade
   - With 3 max concurrent trades = max 3% total risk
   - This is CONSERVATIVE and SAFE
   
3. COMMISSION COSTS:
   - Each trade costs $6 per lot (round-turn)
   - Example: 1 lot trade = $6 total cost
   - Example: 0.5 lot trade = $3 total cost
   - Bot accounts for this in calculations
   
4. RECOMMENDED STARTING SETTINGS:
   - Start with 2-3 pairs only (EURUSD, GBPUSD)
   - Keep risk_per_trade at 0.01 (1%)
   - Keep max_concurrent_trades at 3
   - Run on DEMO account first for 1-2 weeks
   
5. WHEN TO INCREASE RISK:
   - Only after 2-3 months of profitable demo trading
   - Only if you fully understand the risks
   - Maximum recommended: 2% per trade (for experienced traders)
   
6. SESSION TIMES (UTC):
   - London: 08:00 - 16:00
   - New York: 13:00 - 21:00
   - Best overlap: 13:00 - 16:00 (highest liquidity)
   - Bot automatically filters for these sessions
"""


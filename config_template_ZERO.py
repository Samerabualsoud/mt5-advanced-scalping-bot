"""
Configuration Template for MT5 Advanced Scalping Bot
=====================================================

⚠️  CRITICAL: ACY ProZero Zero-Spread Symbol Names
- Zero-spread pairs have "ZERO" suffix (e.g., EURUSDZERO)
- Regular pairs have spreads (e.g., EURUSD)
- Make sure you're using the ZERO versions!

Run find_zero_spread_symbols.py to see all available pairs on your account
"""

CONFIG = {
    # MT5 Connection
    'mt5_login': 12345,  # Your MT5 account number
    'mt5_password': 'YOUR_PASSWORD_HERE',
    'mt5_server': 'ACYSecurities-Demo',  # or 'ACYSecurities-Live'
    
    # Trading Symbols - ACY ProZero ZERO SPREAD pairs
    # ⚠️  IMPORTANT: Use the "ZERO" suffix for zero-spread pairs!
    'symbols': [
        # Major Forex Pairs (zero spread on ACY ProZero)
        'EURUSDZERO',    # EUR/USD with zero spread
        'GBPUSDZERO',    # GBP/USD with zero spread
        # 'USDJPYZERO',    # USD/JPY with zero spread (uncomment if available)
        # 'AUDU SDZERO',    # AUD/USD with zero spread (uncomment if available)
        
        # Start with just 2 pairs for testing, add more later
        # Run find_zero_spread_symbols.py to see all available ZERO pairs
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
SETUP INSTRUCTIONS:

1. FIND YOUR ZERO-SPREAD SYMBOLS:
   Run: python find_zero_spread_symbols.py
   This will show you all available ZERO pairs on your account
   
2. UPDATE SYMBOLS LIST:
   Copy the correct symbol names (with ZERO suffix) to the 'symbols' list above
   
3. VERIFY YOU'RE USING ZERO SPREAD:
   - Symbol name should end with "ZERO" (e.g., EURUSDZERO)
   - NOT regular symbols (e.g., EURUSD)
   
4. TEST CONFIGURATION:
   Run: python diagnose_bot.py
   This will verify your symbols are correct and have zero spread

IMPORTANT NOTES FOR ACY PROZERO ACCOUNT:

1. ZERO SPREAD SYMBOLS:
   - Symbol format: [PAIR]ZERO (e.g., EURUSDZERO, GBPUSDZERO)
   - Spread = 0.0 pips (confirmed in diagnose_bot.py)
   - Commission = $6 per lot (round-turn)
   - Total cost per trade = $6 per lot (vs $10-20 with spread)
   
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
   - Start with 2 pairs only (EURUSDZERO, GBPUSDZERO)
   - Keep risk_per_trade at 0.01 (1%)
   - Keep max_concurrent_trades at 3
   - Run on DEMO account first for 1-2 weeks
   
5. SESSION TIMES (UTC):
   - London: 08:00 - 16:00
   - New York: 13:00 - 21:00
   - Best overlap: 13:00 - 16:00 (highest liquidity)
   - Bot automatically filters for these sessions
   
6. VERIFY ZERO SPREAD:
   After configuring, run diagnose_bot.py to verify:
   - Symbols are available
   - Spread is actually 0.0
   - Data is flowing correctly
"""


"""
Quick Diagnostic Script for Advanced Scalping Bot
==================================================
This script helps diagnose why the bot isn't showing analysis
"""

import MetaTrader5 as mt5
from datetime import datetime, timezone
import pandas as pd

print("="*80)
print("BOT DIAGNOSTIC TOOL")
print("="*80)

# 1. Check UTC time
print("\n1. TIME CHECK:")
print("-" * 40)
now_utc = datetime.now(timezone.utc)
now_local = datetime.now()
print(f"Your local time: {now_local.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Actual UTC time: {now_utc.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"UTC Hour: {now_utc.hour}")

# Check if in active session
hour = now_utc.hour
is_london = 8 <= hour < 16
is_ny = 13 <= hour < 21
is_active = is_london or is_ny

print(f"\nLondon Session (08:00-16:00 UTC): {'✅ ACTIVE' if is_london else '❌ Inactive'}")
print(f"New York Session (13:00-21:00 UTC): {'✅ ACTIVE' if is_ny else '❌ Inactive'}")
print(f"Overall: {'✅ TRADING ALLOWED' if is_active else '❌ OUTSIDE TRADING HOURS'}")

# 2. Check MT5 connection
print("\n2. MT5 CONNECTION:")
print("-" * 40)

try:
    from config import CONFIG
    
    if not mt5.initialize():
        print("❌ MT5 initialization failed!")
        exit(1)
    
    print("✅ MT5 initialized")
    
    if not mt5.login(CONFIG['mt5_login'], password=CONFIG['mt5_password'], server=CONFIG['mt5_server']):
        print(f"❌ MT5 login failed: {mt5.last_error()}")
        exit(1)
    
    print(f"✅ Logged in to {CONFIG['mt5_server']}")
    
    account_info = mt5.account_info()
    print(f"Account: {account_info.login}")
    print(f"Balance: ${account_info.balance:,.2f}")
    
except ImportError:
    print("❌ config.py not found! Copy config_template.py to config.py")
    exit(1)

# 3. Check symbols
print("\n3. SYMBOL CHECK:")
print("-" * 40)

for symbol in CONFIG['symbols']:
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"❌ {symbol}: NOT AVAILABLE")
        continue
    
    if not symbol_info.visible:
        print(f"⚠️  {symbol}: Not visible in Market Watch (adding...)")
        mt5.symbol_select(symbol, True)
    
    tick = mt5.symbol_info_tick(symbol)
    if tick:
        print(f"✅ {symbol}: Bid={tick.bid:.5f}, Ask={tick.ask:.5f}, Spread={tick.ask-tick.bid:.5f}")
    else:
        print(f"❌ {symbol}: No tick data")

# 4. Check data availability
print("\n4. DATA AVAILABILITY CHECK:")
print("-" * 40)

timeframe = mt5.TIMEFRAME_M5
symbol = CONFIG['symbols'][0]

print(f"Testing {symbol} on M5 timeframe...")

rates_m5 = mt5.copy_rates_from_pos(symbol, timeframe, 0, 200)
if rates_m5 is None or len(rates_m5) == 0:
    print(f"❌ No M5 data available for {symbol}")
else:
    print(f"✅ M5 data: {len(rates_m5)} candles available")
    df = pd.DataFrame(rates_m5)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    print(f"   Latest candle: {df['time'].iloc[-1]}")
    print(f"   Close price: {df['close'].iloc[-1]:.5f}")

rates_h1 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 100)
if rates_h1 is None or len(rates_h1) == 0:
    print(f"❌ No H1 data available for {symbol}")
else:
    print(f"✅ H1 data: {len(rates_h1)} candles available")

# 5. Test strategy engine
print("\n5. STRATEGY ENGINE TEST:")
print("-" * 40)

try:
    from advanced_scalping_engine import AdvancedScalpingEngine
    
    engine = AdvancedScalpingEngine()
    print("✅ Engine initialized")
    
    action, confidence, details = engine.analyze(symbol, timeframe)
    
    print(f"\nAnalysis Result:")
    print(f"  Action: {action if action else 'None'}")
    print(f"  Confidence: {confidence}%")
    print(f"  Details: {details}")
    
    if not details:
        print("\n❌ WARNING: No details returned from analysis!")
        print("   This means the strategy engine is failing silently.")
    
except Exception as e:
    print(f"❌ Error testing engine: {str(e)}")
    import traceback
    traceback.print_exc()

# 6. Configuration check
print("\n6. CONFIGURATION CHECK:")
print("-" * 40)

print(f"Risk per trade: {CONFIG.get('risk_per_trade', 0.01) * 100}%")
print(f"Max concurrent trades: {CONFIG.get('max_concurrent_trades', 3)}")
print(f"Min confidence: {CONFIG.get('min_confidence', 70)}%")
print(f"Commission per lot: ${CONFIG.get('commission_per_lot', 6)}")
print(f"Check interval: {CONFIG.get('check_interval', 60)}s")

print("\n" + "="*80)
print("DIAGNOSTIC COMPLETE")
print("="*80)

mt5.shutdown()


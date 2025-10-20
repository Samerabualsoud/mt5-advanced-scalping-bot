"""
Find Zero Spread Symbols on ACY Securities
===========================================
This script scans your MT5 account to find all available zero-spread symbols
"""

import MetaTrader5 as mt5

print("="*80)
print("ZERO SPREAD SYMBOL FINDER")
print("="*80)

# Initialize MT5
if not mt5.initialize():
    print("❌ MT5 initialization failed!")
    exit(1)

print("✅ MT5 initialized\n")

# Get all symbols
all_symbols = mt5.symbols_get()

if all_symbols is None or len(all_symbols) == 0:
    print("❌ No symbols found!")
    mt5.shutdown()
    exit(1)

print(f"Total symbols available: {len(all_symbols)}\n")

# Find zero-spread symbols
print("ZERO SPREAD SYMBOLS:")
print("-" * 80)

zero_spread_symbols = []
forex_zero = []
metals_zero = []
indices_zero = []

for symbol in all_symbols:
    symbol_name = symbol.name
    
    # Look for "ZERO" in the name
    if 'ZERO' in symbol_name.upper():
        zero_spread_symbols.append(symbol_name)
        
        # Categorize
        if any(pair in symbol_name.upper() for pair in ['EUR', 'GBP', 'USD', 'JPY', 'AUD', 'NZD', 'CAD', 'CHF']):
            forex_zero.append(symbol_name)
        elif any(metal in symbol_name.upper() for metal in ['XAU', 'XAG', 'GOLD', 'SILVER']):
            metals_zero.append(symbol_name)
        else:
            indices_zero.append(symbol_name)

# Display results
if forex_zero:
    print("\n📊 FOREX PAIRS (Zero Spread):")
    for sym in sorted(forex_zero):
        tick = mt5.symbol_info_tick(sym)
        if tick:
            spread = tick.ask - tick.bid
            print(f"  ✅ {sym:20s} | Bid: {tick.bid:.5f} | Ask: {tick.ask:.5f} | Spread: {spread:.5f}")
        else:
            print(f"  ⚠️  {sym:20s} | No tick data")

if metals_zero:
    print("\n🥇 METALS (Zero Spread):")
    for sym in sorted(metals_zero):
        tick = mt5.symbol_info_tick(sym)
        if tick:
            spread = tick.ask - tick.bid
            print(f"  ✅ {sym:20s} | Bid: {tick.bid:.2f} | Ask: {tick.ask:.2f} | Spread: {spread:.2f}")
        else:
            print(f"  ⚠️  {sym:20s} | No tick data")

if indices_zero:
    print("\n📈 INDICES (Zero Spread):")
    for sym in sorted(indices_zero):
        tick = mt5.symbol_info_tick(sym)
        if tick:
            spread = tick.ask - tick.bid
            print(f"  ✅ {sym:20s} | Spread: {spread:.2f}")
        else:
            print(f"  ⚠️  {sym:20s} | No tick data")

# Generate config
print("\n" + "="*80)
print("RECOMMENDED CONFIG FOR YOUR config.py:")
print("="*80)

if forex_zero:
    print("\n'symbols': [")
    for sym in sorted(forex_zero)[:6]:  # Top 6 major pairs
        print(f"    '{sym}',")
    print("],")

print("\n" + "="*80)
print(f"Found {len(zero_spread_symbols)} zero-spread symbols total")
print("="*80)

mt5.shutdown()


# Troubleshooting Guide - Advanced Scalping Bot

## Issue: Bot Shows "Signals 0 | Trades Executed 0"

### Problem 1: Wrong Symbol Names (CRITICAL)

**Symptom:** Bot runs but never finds signals, or trades on regular pairs instead of zero-spread pairs.

**Cause:** You're using regular symbol names (e.g., `EURUSD`) instead of zero-spread names (e.g., `EURUSDZERO`).

**Solution:**

1. **Find your zero-spread symbols:**
```bash
python find_zero_spread_symbols.py
```

2. **Update config.py with correct names:**
```python
'symbols': [
    'EURUSDZERO',    # ✅ Correct (zero spread)
    'GBPUSDZERO',    # ✅ Correct (zero spread)
    # NOT 'EURUSD'   # ❌ Wrong (has spread)
],
```

3. **Verify:**
```bash
python diagnose_bot.py
```

Look for:
```
✅ EURUSDZERO: Bid=1.16570, Ask=1.16570, Spread=0.00000
```

If spread > 0, you're using the wrong symbol!

---

### Problem 2: UTC Time Detection Issue

**Symptom:** Bot shows UTC time that matches your local time (Riyadh = UTC+3).

**Cause:** Python's `datetime.utcnow()` might not work correctly on some systems.

**Solution:**

The bot has been updated to use `datetime.now(timezone.utc)` which is more reliable.

**Verify current UTC time:**
```bash
python diagnose_bot.py
```

Look for:
```
Your local time: 2025-10-20 13:07:53
Actual UTC time: 2025-10-20 10:07:53  # Should be 3 hours behind Riyadh
UTC Hour: 10
```

**Manual check:**
- Riyadh time: 13:00
- UTC time should be: 10:00 (3 hours behind)
- London session: 08:00-16:00 UTC (11:00-19:00 Riyadh time)
- NY session: 13:00-21:00 UTC (16:00-00:00 Riyadh time)

---

### Problem 3: No Analysis Shown

**Symptom:** Bot scans but doesn't show detailed analysis like:
```
[EURUSDZERO] Regime: TRENDING | Strategy: ...
```

**Possible Causes:**

**A. Outside Trading Hours**
```bash
python diagnose_bot.py
```

Check if you're in active session:
```
✅ Active Session: LONDON (08:00-16:00 UTC)
```

If you see:
```
⏸️  Inactive Session: Current hour 5 UTC is outside...
```

Then the bot won't trade (by design).

**B. No Data Available**
```bash
python diagnose_bot.py
```

Look for:
```
✅ M5 data: 200 candles available
✅ H1 data: 100 candles available
```

If you see:
```
❌ No M5 data available
```

Then MT5 can't get historical data. Solutions:
- Ensure MT5 is running
- Ensure symbols are in Market Watch
- Wait a few minutes for data to load

**C. Strategy Engine Error**

Run diagnostic:
```bash
python diagnose_bot.py
```

Look at "STRATEGY ENGINE TEST" section. If you see errors, there's a bug in the analysis code.

---

### Problem 4: Bot Runs But No Signals

**Symptom:** Bot shows analysis but never generates signals.

**Possible Causes:**

**A. Market Conditions Don't Meet Criteria**

The bot is very selective. It needs:
- EMA crossover (9 crosses 21)
- RSI confirmation (>50 for buy, <50 for sell)
- H1 trend alignment
- Normal volatility (not too high/low)

**This is NORMAL.** The bot might only find 5-10 good signals per day.

**B. Confidence Threshold Too High**

Check your config:
```python
'min_confidence': 70,  # Try lowering to 65 for testing
```

**C. Wrong Timeframe**

Ensure you're using M5:
```python
'timeframe': 'M5',  # Not M1 or M15
```

---

## Quick Diagnostic Checklist

Run these in order:

### 1. Find Zero-Spread Symbols
```bash
python find_zero_spread_symbols.py
```

Expected output:
```
📊 FOREX PAIRS (Zero Spread):
  ✅ EURUSDZERO        | Spread: 0.00000
  ✅ GBPUSDZERO        | Spread: 0.00000
```

### 2. Update Config
```bash
cp config_template_ZERO.py config.py
# Edit config.py with your credentials and ZERO symbols
```

### 3. Run Diagnostic
```bash
python diagnose_bot.py
```

Check all sections pass:
- ✅ Time check (UTC correct)
- ✅ MT5 connection
- ✅ Symbol check (all ZERO symbols available, spread = 0)
- ✅ Data availability
- ✅ Strategy engine test

### 4. Run Bot
```bash
python advanced_scalping_bot.py
```

---

## Common Errors and Solutions

### Error: "Symbol not found"
**Solution:** Run `find_zero_spread_symbols.py` to get correct names

### Error: "No data available"
**Solution:** 
- Ensure MT5 is running
- Add symbols to Market Watch
- Wait 2-3 minutes for data to load

### Error: "Outside active session"
**Solution:** 
- Check UTC time with `diagnose_bot.py`
- Trade during London (08:00-16:00 UTC) or NY (13:00-21:00 UTC)
- Riyadh time: London = 11:00-19:00, NY = 16:00-00:00

### Bot shows signals but doesn't execute
**Check:**
- Margin level > 1000%
- Max concurrent trades not reached
- Daily loss limit not hit
- Auto-trading enabled in MT5

---

## Still Having Issues?

1. **Enable debug mode:**
```python
'debug_mode': True,
```

2. **Check log file:**
```
advanced_scalping_bot.log
```

3. **Run diagnostic:**
```bash
python diagnose_bot.py > diagnostic_output.txt
```

4. **Check MT5:**
- Is MT5 running?
- Is auto-trading enabled? (Tools → Options → Expert Advisors → Allow automated trading)
- Are symbols in Market Watch?

---

## Expected Behavior

**Normal operation:**

```
ADVANCED MARKET SCAN - 2025-10-20 10:07:53 UTC
Current UTC time: 10:07:53 (Hour: 10)
✅ Active Session: LONDON (08:00-16:00 UTC)

📊 Analyzing 2 symbols...

[EURUSDZERO] Regime: TRENDING | Strategy: TRENDING_EMA_RSI
  ⏸  No signal - Waiting for EMA crossover

[GBPUSDZERO] Regime: RANGING | Strategy: RANGING_BB_REVERSION
  🎯 SIGNAL: BUY (75% confidence)
  📊 H1 Trend: bullish
  📈 RSI: 32.5
  🎲 Volume: ✅ Confirmed
  🔄 Divergence: None
  🎯 TP: 12.5 pips | SL: 8.3 pips | R:R = 1.50

SCAN COMPLETE: Signals 1 | Trades Executed 1
```

**It's NORMAL to see:**
- Many scans with 0 signals (market not ready)
- Only 5-15 signals per day (selective strategy)
- More signals during London/NY overlap (13:00-16:00 UTC)

**It's NOT NORMAL to see:**
- Zero analysis output (check symbols)
- "Outside active session" during London/NY hours (check UTC time)
- Errors in log file (check diagnostic)


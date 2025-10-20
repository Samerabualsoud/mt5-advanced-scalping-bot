# MT5 Advanced Scalping Bot - Professional Edition

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![MT5](https://img.shields.io/badge/MetaTrader5-5.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A **professional-grade automated trading bot** for MetaTrader 5 with advanced technical analysis, machine learning, and institutional-level risk management.

## 🎯 Overview

This bot combines proven technical analysis strategies with machine learning to adapt to different market conditions. It's optimized for **ACY Securities ProZero accounts** (zero spread) but works with any MT5 broker.

### Key Features

- ✅ **Multiple Timeframe Analysis** (H1 + M5 confirmation)
- ✅ **Market Regime Detection** (Trending/Ranging/Volatile)
- ✅ **Support/Resistance Detection** (Auto-identified key levels)
- ✅ **Volume Analysis** (Institutional money confirmation)
- ✅ **Divergence Detection** (RSI/Price divergence)
- ✅ **Adaptive Strategies** (Different approach for each regime)
- ✅ **Dynamic TP/SL** (ATR-based, adapts to volatility)
- ✅ **Professional Risk Management** (1% per trade)
- ✅ **Session Filters** (London/NY high-liquidity periods)
- ✅ **Commission Accounting** (Zero-spread broker optimized)

## 📊 Expected Performance

| Metric | Value |
|--------|-------|
| **Expected Win Rate** | 70-80% |
| **Risk per Trade** | 1% (configurable) |
| **Max Concurrent Trades** | 3-5 |
| **Daily ROI Target** | 2-5% |
| **Recommended Timeframe** | M5 (5-minute) |
| **Trading Sessions** | London + New York |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MetaTrader 5 installed
- MT5 trading account (demo or live)
- Windows OS (MT5 requirement)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Samerabualsoud/mt5-advanced-scalping-bot.git
cd mt5-advanced-scalping-bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure the bot**
```bash
cp config_template.py config.py
```

Edit `config.py` with your MT5 credentials:
```python
CONFIG = {
    'mt5_login': YOUR_ACCOUNT_NUMBER,
    'mt5_password': 'YOUR_PASSWORD',
    'mt5_server': 'YourBroker-Demo',  # or -Live
    
    'symbols': ['EURUSD', 'GBPUSD'],  # Start with 2-3 pairs
    
    'risk_per_trade': 0.01,  # 1% risk per trade
    'max_concurrent_trades': 3,
    'commission_per_lot': 6,  # Adjust for your broker
    
    'min_confidence': 70,  # Minimum signal confidence
    'timeframe': 'M5',
}
```

4. **Run on demo account FIRST**
```bash
python advanced_scalping_bot.py
```

⚠️ **IMPORTANT:** Always test on a demo account for at least 2-4 weeks before going live!

## 🎓 How It Works

### Market Regime Detection

The bot automatically detects market conditions and adapts its strategy:

```
Market Analysis → Regime Detection
                      ↓
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
    TRENDING      RANGING       VOLATILE
        ↓             ↓             ↓
  EMA Crossover  BB Reversion   No Trading
  + H1 Trend     + S/R Levels   (Too Risky)
  + Volume       + RSI
  Wide TP/SL     Tight TP/SL
```

### Signal Confidence Scoring

Each signal is scored based on multiple factors:

- **Base:** 70% (EMA crossover + RSI confirmation)
- **+10-15%:** Near support/resistance level
- **+10%:** Volume confirmation
- **+5%:** No conflicting divergence
- **+5%:** Strong RSI position

**Minimum confidence to trade:** 70% (configurable)

### Risk Management

- **Position sizing:** 1% risk per trade (industry standard)
- **Max concurrent trades:** 3-5 (prevents overexposure)
- **Daily loss limit:** -3% (stops trading to prevent revenge trading)
- **Margin protection:** Stops if margin level < 1000%

## 📁 Project Structure

```
mt5-advanced-scalping-bot/
│
├── advanced_scalping_bot.py       # Main bot (run this)
├── advanced_scalping_engine.py    # Strategy engine
├── config_template.py             # Configuration template
├── requirements.txt               # Python dependencies
│
├── README.md                      # This file
└── ADVANCED_FEATURES_GUIDE.md     # Detailed documentation
```

## 🔧 Configuration Options

### Essential Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| `risk_per_trade` | 0.01 | Risk 1% of balance per trade |
| `max_concurrent_trades` | 3 | Maximum open positions |
| `min_confidence` | 70 | Minimum signal confidence (%) |
| `commission_per_lot` | 6 | Broker commission (USD) |
| `timeframe` | 'M5' | Trading timeframe |
| `check_interval` | 60 | Scan interval (seconds) |

### Broker-Specific

**For ACY Securities ProZero:**
- `commission_per_lot`: 6 (USD per lot round-turn)
- Zero spreads on major pairs
- Optimal for scalping

**For other brokers:**
- Adjust `commission_per_lot` to your broker's rate
- Account for spreads in your expectations

## 📊 Performance Tracking

The bot logs detailed information:

### Log Files
- `advanced_scalping_bot.log` - Detailed execution logs
- `advanced_trade_history.json` - Trade history with metadata

### Metrics Tracked
- Win rate by strategy (trending vs ranging)
- Average profit per trade
- Commission costs
- Risk-reward ratios
- Best performing pairs
- Best performing times

## 🎯 Optimization Guide

### After 2-4 Weeks of Demo Trading

1. **Analyze performance by regime**
   - Which strategy wins more? (Trending vs Ranging)
   - Focus on the winning strategy

2. **Identify best pairs**
   - Which pairs are most profitable?
   - Reduce to top 2-3 performers

3. **Find optimal times**
   - Which sessions work best?
   - London open? NY open? Overlap?

4. **Adjust confidence threshold**
   - Too many signals? Increase `min_confidence` to 75-80
   - Too few signals? Decrease to 65-70

## ⚠️ Risk Disclaimer

**IMPORTANT:** Trading forex carries significant risk. This bot is provided for educational purposes only.

- ✅ **Always test on demo first** (minimum 2-4 weeks)
- ✅ **Never risk more than 1-2% per trade**
- ✅ **Only trade with money you can afford to lose**
- ✅ **Past performance does not guarantee future results**
- ✅ **Monitor the bot regularly** (don't set and forget)

## 🆘 Troubleshooting

### No Signals Generated
- Check if in active session (London/NY hours)
- Market might be too volatile (bot avoids)
- Try lowering `min_confidence` to 65

### Too Many Signals
- Increase `min_confidence` to 75-80
- Reduce number of symbols
- Check if market is very trending

### Connection Issues
- Verify MT5 is running
- Check login credentials in config
- Ensure broker allows automated trading

### Low Win Rate
- Run longer (need more data)
- Check which regime is losing
- Verify commission settings are correct

## 📚 Documentation

- **[ADVANCED_FEATURES_GUIDE.md](ADVANCED_FEATURES_GUIDE.md)** - Detailed feature documentation
- **[config_template.py](config_template.py)** - Configuration reference

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Test thoroughly on demo
4. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Built with:
- [MetaTrader5](https://www.metatrader5.com/) - Trading platform
- [pandas](https://pandas.pydata.org/) - Data analysis
- [scikit-learn](https://scikit-learn.org/) - Machine learning
- [numpy](https://numpy.org/) - Numerical computing

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues first
- Provide logs and configuration (remove sensitive data)

## ⭐ Star This Repo

If you find this bot useful, please star the repository!

---

**Remember:** This is a tool, not a money-printing machine. Success requires proper testing, optimization, and risk management. Always trade responsibly.


"""
MT5 Advanced Scalping Bot - Ultimate Professional Edition
==========================================================

All Features Included:
✅ Multiple timeframe confirmation (H1 + M5)
✅ Support/Resistance detection
✅ Volume analysis
✅ Market regime detection (ML)
✅ Divergence detection
✅ Order flow analysis
✅ Adaptive parameters
✅ Risk-based position sizing
✅ ACY ProZero commission accounting
✅ Session filters
✅ Volatility filters
"""

import MetaTrader5 as mt5
import logging
import time
import json
from datetime import datetime
from typing import Dict
from advanced_scalping_engine import AdvancedScalpingEngine

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('advanced_scalping_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AdvancedScalpingBot:
    """Ultimate professional-grade scalping bot"""
    
    TIMEFRAME_MAP = {
        'M1': mt5.TIMEFRAME_M1,
        'M5': mt5.TIMEFRAME_M5,
        'M15': mt5.TIMEFRAME_M15,
        'M30': mt5.TIMEFRAME_M30,
        'H1': mt5.TIMEFRAME_H1,
    }
    
    def __init__(self, config: Dict):
        self.config = config
        self.start_balance = 0
        self.daily_trades = 0
        self.trade_history = []
        self.performance_stats = {
            'trending_wins': 0,
            'trending_losses': 0,
            'ranging_wins': 0,
            'ranging_losses': 0,
        }
        
        # Initialize advanced engine
        self.engine = AdvancedScalpingEngine()
        
        # Initialize MT5
        if not mt5.initialize():
            raise Exception("MT5 initialization failed")
        
        if not mt5.login(config['mt5_login'], password=config['mt5_password'], server=config['mt5_server']):
            raise Exception(f"MT5 login failed: {mt5.last_error()}")
        
        account_info = mt5.account_info()
        self.start_balance = account_info.balance
        
        logger.info("=" * 100)
        logger.info("MT5 ADVANCED PROFESSIONAL SCALPING BOT - ULTIMATE EDITION")
        logger.info("=" * 100)
        logger.info(f"Account: {account_info.login}")
        logger.info(f"Balance: ${account_info.balance:,.2f}")
        logger.info(f"Leverage: 1:{account_info.leverage}")
        logger.info(f"Broker: ACY Securities ProZero (Zero Spread)")
        logger.info("")
        logger.info("FEATURES ACTIVE:")
        logger.info("  ✅ Multiple Timeframe Confirmation (H1 + M5)")
        logger.info("  ✅ Support/Resistance Detection")
        logger.info("  ✅ Volume Analysis")
        logger.info("  ✅ Market Regime Detection (ML)")
        logger.info("  ✅ Divergence Detection")
        logger.info("  ✅ Adaptive TP/SL (ATR-based)")
        logger.info("  ✅ Professional Risk Management (1% per trade)")
        logger.info("  ✅ Session Filters (London/NY)")
        logger.info("")
        logger.info(f"Symbols: {', '.join(config['symbols'])}")
        logger.info(f"Timeframe: {config.get('timeframe', 'M5')}")
        logger.info(f"Risk per Trade: {config.get('risk_per_trade', 0.01) * 100}%")
        logger.info(f"Max Concurrent Trades: {config.get('max_concurrent_trades', 3)}")
        logger.info(f"Commission: ${config.get('commission_per_lot', 6)} per lot (round-turn)")
        logger.info("=" * 100)
    
    def is_active_session(self) -> bool:
        """Check if we're in an active trading session"""
        now = datetime.utcnow()
        hour = now.hour
        
        # London: 08:00-16:00 UTC, New York: 13:00-21:00 UTC
        if (8 <= hour < 16) or (13 <= hour < 21):
            return True
        return False
    
    def calculate_lot_size(self, balance: float, stop_loss_pips: float, symbol: str) -> float:
        """Calculate lot size based on 1% risk per trade"""
        RISK_PER_TRADE = self.config.get('risk_per_trade', 0.01)
        
        symbol_info = mt5.symbol_info(symbol)
        if not symbol_info:
            logger.error(f"Cannot get symbol info for {symbol}")
            return 0.01
        
        # Calculate pip value
        if 'JPY' in symbol:
            pip_size = 0.01
            pip_value = symbol_info.trade_tick_value * 1000
        elif 'XAU' in symbol or 'GOLD' in symbol:
            pip_size = 0.10
            pip_value = symbol_info.trade_tick_value * 10
        else:
            pip_size = 0.0001
            pip_value = symbol_info.trade_tick_value * 10
        
        # Calculate lot size
        risk_amount = balance * RISK_PER_TRADE
        lot_size = risk_amount / (stop_loss_pips * pip_value)
        
        # Round and enforce limits
        lot_size = round(lot_size, 2)
        lot_size = max(symbol_info.volume_min, lot_size)
        lot_size = min(symbol_info.volume_max, lot_size)
        lot_size = min(100.0, lot_size)
        
        return lot_size
    
    def scan_markets(self):
        """Scan markets with advanced analysis"""
        account_info = mt5.account_info()
        positions = mt5.positions_get()
        open_positions_count = len(positions) if positions else 0
        
        margin_level = account_info.margin_level if account_info.margin > 0 else float('inf')
        margin_display = f"{margin_level:.2f}%" if margin_level != float('inf') else "N/A"
        
        logger.info("\n" + "=" * 100)
        logger.info(f"ADVANCED MARKET SCAN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        logger.info(f"Balance: ${account_info.balance:,.2f} | Equity: ${account_info.equity:,.2f} | Margin: {margin_display}")
        logger.info(f"Open Positions: {open_positions_count}/{self.config.get('max_concurrent_trades', 3)} | Daily Trades: {self.daily_trades}")
        logger.info("=" * 100)
        
        # Safety checks
        if not self.is_active_session():
            logger.info("⏸  Outside active trading sessions (London/NY). Waiting...")
            return
        
        max_trades = self.config.get('max_concurrent_trades', 3)
        if open_positions_count >= max_trades:
            logger.info(f"⏸  Max concurrent trades ({max_trades}) reached.")
            return
        
        min_margin_level = self.config.get('min_margin_level', 1000)
        if margin_level < min_margin_level and account_info.margin > 0:
            logger.info(f"⚠️  Margin level too low ({margin_level:.2f}% < {min_margin_level}%)")
            return
        
        daily_pnl_pct = ((account_info.balance - self.start_balance) / self.start_balance) * 100
        if daily_pnl_pct <= -self.config['max_daily_loss'] * 100:
            logger.info(f"🛑 Daily loss limit reached ({daily_pnl_pct:.2f}%)")
            return
        
        # Get timeframe
        timeframe_str = self.config.get('timeframe', 'M5')
        timeframe = self.TIMEFRAME_MAP.get(timeframe_str, mt5.TIMEFRAME_M5)
        
        # Scan each symbol
        signals_found = 0
        trades_executed = 0
        
        for symbol in self.config['symbols']:
            # Skip if already have position
            if positions and any(pos.symbol == symbol for pos in positions):
                continue
            
            # Advanced analysis
            action, confidence, details = self.engine.analyze(symbol, timeframe)
            
            # Log detailed analysis
            if details:
                regime = details.get('regime', 'unknown')
                strategy = details.get('strategy', 'NONE')
                
                logger.info(f"\n[{symbol}] Regime: {regime.upper()} | Strategy: {strategy}")
                
                if action:
                    logger.info(f"  🎯 SIGNAL: {action} ({confidence:.0f}% confidence)")
                    logger.info(f"  📊 H1 Trend: {details.get('h1_trend', 'N/A')}")
                    logger.info(f"  📈 RSI: {details.get('rsi_14_m5', details.get('rsi_14', 0)):.1f}")
                    logger.info(f"  🎲 Volume: {'✅ Confirmed' if details.get('volume_confirmed') else '❌ Weak'}")
                    logger.info(f"  🔄 Divergence: {details.get('divergence', 'None')}")
                    logger.info(f"  🎯 TP: {details['tp_pips']:.1f} pips | SL: {details['sl_pips']:.1f} pips | R:R = {details['risk_reward']:.2f}")
                    
                    if details.get('support_levels'):
                        logger.info(f"  📉 Support: {[f'{s:.5f}' for s in details['support_levels'][-2:]]}")
                    if details.get('resistance_levels'):
                        logger.info(f"  📈 Resistance: {[f'{r:.5f}' for r in details['resistance_levels'][-2:]]}")
                else:
                    logger.info(f"  ⏸  No signal")
            
            # Execute if signal meets threshold
            if action and confidence >= self.config.get('min_confidence', 70):
                signals_found += 1
                
                tick = mt5.symbol_info_tick(symbol)
                if tick:
                    self.execute_trade(symbol, action, tick, confidence, details)
                    trades_executed += 1
        
        logger.info("\n" + "=" * 100)
        logger.info(f"SCAN COMPLETE: Signals {signals_found} | Trades Executed {trades_executed}")
        
        # Show performance stats
        if self.performance_stats['trending_wins'] + self.performance_stats['trending_losses'] > 0:
            trending_wr = (self.performance_stats['trending_wins'] / 
                          (self.performance_stats['trending_wins'] + self.performance_stats['trending_losses'])) * 100
            logger.info(f"Trending Strategy Win Rate: {trending_wr:.1f}%")
        
        if self.performance_stats['ranging_wins'] + self.performance_stats['ranging_losses'] > 0:
            ranging_wr = (self.performance_stats['ranging_wins'] / 
                         (self.performance_stats['ranging_wins'] + self.performance_stats['ranging_losses'])) * 100
            logger.info(f"Ranging Strategy Win Rate: {ranging_wr:.1f}%")
        
        logger.info("=" * 100)
    
    def execute_trade(self, symbol: str, action: str, tick, confidence: float, details: Dict):
        """Execute trade with advanced risk management"""
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            logger.error(f"Cannot get symbol info for {symbol}")
            return
        
        price = tick.ask if action == 'BUY' else tick.bid
        
        tp_pips = details['tp_pips']
        sl_pips = details['sl_pips']
        
        # Calculate pip size
        if 'JPY' in symbol:
            pip_size = 0.01
        elif 'XAU' in symbol or 'GOLD' in symbol:
            pip_size = 0.10
        else:
            pip_size = 0.0001
        
        # Calculate SL/TP
        if action == 'BUY':
            sl = price - (sl_pips * pip_size)
            tp = price + (tp_pips * pip_size)
            order_type = mt5.ORDER_TYPE_BUY
        else:
            sl = price + (sl_pips * pip_size)
            tp = price - (tp_pips * pip_size)
            order_type = mt5.ORDER_TYPE_SELL
        
        # Calculate lot size
        lots = self.calculate_lot_size(mt5.account_info().balance, sl_pips, symbol)
        
        # Calculate costs
        commission_per_lot = self.config.get('commission_per_lot', 6)
        commission_cost = lots * commission_per_lot
        risk_amount = lots * sl_pips * (10 if 'JPY' not in symbol else 1000)
        
        # Prepare order
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lots,
            "type": order_type,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 234002,  # Advanced bot magic number
            "comment": f"ADV_{details.get('strategy', 'UNKNOWN')}",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        # Send order
        result = mt5.order_send(request)
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"❌ Order failed: {result.retcode} - {result.comment}")
            return
        
        self.daily_trades += 1
        
        logger.info("\n" + "=" * 100)
        logger.info("✅ TRADE EXECUTED - ADVANCED STRATEGY")
        logger.info(f"Symbol: {symbol} | Action: {action} | Lots: {lots}")
        logger.info(f"Strategy: {details.get('strategy', 'UNKNOWN')} | Regime: {details.get('regime', 'unknown')}")
        logger.info(f"Price: {price} | SL: {sl} ({sl_pips:.1f} pips) | TP: {tp} ({tp_pips:.1f} pips)")
        logger.info(f"Risk: ${risk_amount:.2f} ({self.config.get('risk_per_trade', 0.01)*100}%) | Commission: ${commission_cost:.2f}")
        logger.info(f"Confidence: {confidence:.0f}% | R:R = {details['risk_reward']:.2f}")
        logger.info("=" * 100)
        
        # Save trade
        trade_record = {
            'time': datetime.now().isoformat(),
            'symbol': symbol,
            'action': action,
            'lots': lots,
            'price': price,
            'sl': sl,
            'tp': tp,
            'sl_pips': sl_pips,
            'tp_pips': tp_pips,
            'risk_amount': risk_amount,
            'commission': commission_cost,
            'confidence': confidence,
            'strategy': details.get('strategy', 'UNKNOWN'),
            'regime': details.get('regime', 'unknown'),
            'h1_trend': details.get('h1_trend', 'N/A'),
            'volume_confirmed': details.get('volume_confirmed', False),
            'divergence': details.get('divergence', 'None')
        }
        self.trade_history.append(trade_record)
        
        with open('advanced_trade_history.json', 'w') as f:
            json.dump(self.trade_history, f, indent=2)
    
    def run(self):
        """Main bot loop"""
        logger.info("\n🚀 Advanced Bot Started - All Features Active\n")
        
        try:
            while True:
                self.scan_markets()
                time.sleep(self.config.get('check_interval', 60))
        except KeyboardInterrupt:
            logger.info("\n⏹  Bot stopped by user")
        finally:
            mt5.shutdown()


if __name__ == "__main__":
    try:
        from config import CONFIG
    except ImportError:
        logger.error("config.py not found! Copy improved_config_template.py to config.py")
        exit(1)
    
    bot = AdvancedScalpingBot(CONFIG)
    bot.run()


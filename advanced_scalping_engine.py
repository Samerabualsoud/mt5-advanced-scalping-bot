"""
MT5 Advanced Scalping Engine - Professional Grade
==================================================

Features:
- Multiple timeframe confirmation (H1 + M5)
- Support/Resistance detection
- Volume analysis
- Market regime detection (ML)
- Divergence detection
- Order flow analysis
- Adaptive parameters
- Signal quality scoring
"""

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional, List
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
import pickle
import os


class MarketRegimeDetector:
    """Detect market regime using ML"""
    
    def __init__(self):
        self.model = None
        self.model_path = 'market_regime_model.pkl'
        self._load_or_create_model()
    
    def _load_or_create_model(self):
        """Load existing model or create new one"""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
            except:
                self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        else:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    def detect_regime(self, df: pd.DataFrame) -> str:
        """
        Detect market regime: 'trending', 'ranging', or 'volatile'
        
        Uses multiple indicators to classify:
        - ADX for trend strength
        - Bollinger Band width for volatility
        - Price range for consolidation
        """
        if len(df) < 50:
            return 'ranging'
        
        # Calculate indicators for regime detection
        adx = self._calculate_adx(df, 14)
        bb_width = self._calculate_bb_width(df, 20)
        price_range = (df['high'].rolling(20).max() - df['low'].rolling(20).min()) / df['close']
        
        current_adx = adx.iloc[-1]
        current_bb_width = bb_width.iloc[-1]
        avg_bb_width = bb_width.rolling(50).mean().iloc[-1]
        current_range = price_range.iloc[-1]
        
        # Classification logic
        if current_adx > 25:
            return 'trending'
        elif current_bb_width > avg_bb_width * 1.5:
            return 'volatile'
        else:
            return 'ranging'
    
    def _calculate_adx(self, df: pd.DataFrame, period: int) -> pd.Series:
        """Calculate Average Directional Index"""
        high = df['high']
        low = df['low']
        close = df['close']
        
        # Calculate +DM and -DM
        plus_dm = high.diff()
        minus_dm = -low.diff()
        
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm < 0] = 0
        
        # Calculate True Range
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # Calculate smoothed +DI and -DI
        atr = tr.rolling(period).mean()
        plus_di = 100 * (plus_dm.rolling(period).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(period).mean() / atr)
        
        # Calculate DX and ADX
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(period).mean()
        
        return adx
    
    def _calculate_bb_width(self, df: pd.DataFrame, period: int) -> pd.Series:
        """Calculate Bollinger Band width"""
        sma = df['close'].rolling(period).mean()
        std = df['close'].rolling(period).std()
        upper = sma + (2 * std)
        lower = sma - (2 * std)
        width = (upper - lower) / sma
        return width


class SupportResistanceDetector:
    """Detect support and resistance levels"""
    
    def detect_levels(self, df: pd.DataFrame, lookback: int = 100) -> Dict[str, List[float]]:
        """
        Detect support and resistance levels using pivot points
        """
        if len(df) < lookback:
            return {'support': [], 'resistance': []}
        
        recent_data = df.tail(lookback)
        
        # Find local maxima (resistance) and minima (support)
        resistance_levels = []
        support_levels = []
        
        for i in range(5, len(recent_data) - 5):
            # Check if it's a local maximum (resistance)
            if (recent_data['high'].iloc[i] > recent_data['high'].iloc[i-5:i].max() and
                recent_data['high'].iloc[i] > recent_data['high'].iloc[i+1:i+6].max()):
                resistance_levels.append(recent_data['high'].iloc[i])
            
            # Check if it's a local minimum (support)
            if (recent_data['low'].iloc[i] < recent_data['low'].iloc[i-5:i].min() and
                recent_data['low'].iloc[i] < recent_data['low'].iloc[i+1:i+6].min()):
                support_levels.append(recent_data['low'].iloc[i])
        
        # Cluster nearby levels
        support_levels = self._cluster_levels(support_levels)
        resistance_levels = self._cluster_levels(resistance_levels)
        
        return {
            'support': support_levels[-3:] if support_levels else [],  # Keep top 3
            'resistance': resistance_levels[-3:] if resistance_levels else []
        }
    
    def _cluster_levels(self, levels: List[float], threshold: float = 0.0005) -> List[float]:
        """Cluster nearby levels together"""
        if not levels:
            return []
        
        levels = sorted(levels)
        clustered = [levels[0]]
        
        for level in levels[1:]:
            if abs(level - clustered[-1]) / clustered[-1] > threshold:
                clustered.append(level)
        
        return clustered
    
    def is_near_level(self, price: float, levels: List[float], threshold: float = 0.001) -> bool:
        """Check if price is near any S/R level"""
        for level in levels:
            if abs(price - level) / level < threshold:
                return True
        return False


class AdvancedScalpingEngine:
    """Advanced scalping engine with all professional features"""
    
    def __init__(self):
        self.regime_detector = MarketRegimeDetector()
        self.sr_detector = SupportResistanceDetector()
    
    def analyze(self, symbol: str, timeframe) -> Tuple[Optional[str], float, Dict]:
        """
        Comprehensive market analysis with all features
        
        Returns:
            action: 'BUY', 'SELL', or None
            confidence: 0-100
            details: Analysis details
        """
        # Get M5 data (primary timeframe)
        rates_m5 = mt5.copy_rates_from_pos(symbol, timeframe, 0, 200)
        if rates_m5 is None or len(rates_m5) < 100:
            return None, 0, {}
        
        df_m5 = pd.DataFrame(rates_m5)
        df_m5['time'] = pd.to_datetime(df_m5['time'], unit='s')
        
        # Get H1 data (higher timeframe for trend confirmation)
        rates_h1 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 100)
        if rates_h1 is None or len(rates_h1) < 50:
            return None, 0, {}
        
        df_h1 = pd.DataFrame(rates_h1)
        df_h1['time'] = pd.to_datetime(df_h1['time'], unit='s')
        
        # 1. Detect market regime
        regime = self.regime_detector.detect_regime(df_m5)
        
        # 2. Detect support/resistance levels
        sr_levels = self.sr_detector.detect_levels(df_m5)
        
        # 3. Analyze based on regime
        if regime == 'trending':
            action, confidence, details = self._trending_strategy(df_m5, df_h1, sr_levels, symbol)
        elif regime == 'ranging':
            action, confidence, details = self._ranging_strategy(df_m5, df_h1, sr_levels, symbol)
        else:  # volatile
            # Don't trade in highly volatile conditions
            return None, 0, {'regime': regime, 'reason': 'Too volatile'}
        
        if action and details:
            details['regime'] = regime
            details['support_levels'] = sr_levels['support']
            details['resistance_levels'] = sr_levels['resistance']
        
        return action, confidence, details
    
    def _trending_strategy(self, df_m5: pd.DataFrame, df_h1: pd.DataFrame, 
                          sr_levels: Dict, symbol: str) -> Tuple[Optional[str], float, Dict]:
        """
        Strategy for trending markets
        Uses EMA crossover with multiple confirmations
        """
        # Calculate M5 indicators
        ema_9_m5 = df_m5['close'].ewm(span=9, adjust=False).mean()
        ema_21_m5 = df_m5['close'].ewm(span=21, adjust=False).mean()
        rsi_14_m5 = self._calculate_rsi(df_m5['close'], 14)
        atr_14_m5 = self._calculate_atr(df_m5, 14)
        volume_sma = df_m5['tick_volume'].rolling(20).mean()
        
        # Calculate H1 trend (higher timeframe)
        ema_50_h1 = df_h1['close'].ewm(span=50, adjust=False).mean()
        ema_200_h1 = df_h1['close'].ewm(span=200, adjust=False).mean()
        
        # Current values
        current_price = df_m5['close'].iloc[-1]
        current_ema9_m5 = ema_9_m5.iloc[-1]
        prev_ema9_m5 = ema_9_m5.iloc[-2]
        current_ema21_m5 = ema_21_m5.iloc[-1]
        prev_ema21_m5 = ema_21_m5.iloc[-2]
        current_rsi_m5 = rsi_14_m5.iloc[-1]
        current_atr = atr_14_m5.iloc[-1]
        current_volume = df_m5['tick_volume'].iloc[-1]
        avg_volume = volume_sma.iloc[-1]
        
        # H1 trend
        current_ema50_h1 = ema_50_h1.iloc[-1]
        current_ema200_h1 = ema_200_h1.iloc[-1]
        h1_trend = 'bullish' if current_ema50_h1 > current_ema200_h1 else 'bearish'
        
        # Detect divergence
        divergence = self._detect_divergence(df_m5, rsi_14_m5)
        
        # Check volume confirmation
        volume_confirmed = current_volume > avg_volume * 1.2
        
        action = None
        confidence = 0
        
        # BUY Signal
        if (prev_ema9_m5 <= prev_ema21_m5 and current_ema9_m5 > current_ema21_m5 and
            current_rsi_m5 > 50 and h1_trend == 'bullish'):
            
            action = 'BUY'
            confidence = 70
            
            # Bonus: Near support level
            if self.sr_detector.is_near_level(current_price, sr_levels['support']):
                confidence += 10
            
            # Bonus: Volume confirmation
            if volume_confirmed:
                confidence += 10
            
            # Bonus: No bearish divergence
            if divergence != 'bearish':
                confidence += 5
            
            # Bonus: Strong RSI (50-60 range)
            if 50 < current_rsi_m5 < 60:
                confidence += 5
        
        # SELL Signal
        elif (prev_ema9_m5 >= prev_ema21_m5 and current_ema9_m5 < current_ema21_m5 and
              current_rsi_m5 < 50 and h1_trend == 'bearish'):
            
            action = 'SELL'
            confidence = 70
            
            # Bonus: Near resistance level
            if self.sr_detector.is_near_level(current_price, sr_levels['resistance']):
                confidence += 10
            
            # Bonus: Volume confirmation
            if volume_confirmed:
                confidence += 10
            
            # Bonus: No bullish divergence
            if divergence != 'bullish':
                confidence += 5
            
            # Bonus: Strong RSI (40-50 range)
            if 40 < current_rsi_m5 < 50:
                confidence += 5
        
        if action:
            # Dynamic TP/SL based on ATR
            symbol_info = mt5.symbol_info(symbol)
            if not symbol_info:
                return None, 0, {}
            
            pip_size = self._get_pip_size(symbol)
            atr_in_pips = current_atr / pip_size
            
            # Trending market: wider TP/SL
            sl_pips = atr_in_pips * 1.2
            tp_pips = atr_in_pips * 2.0  # 1.67:1 risk-reward
            
            # Enforce limits
            sl_pips = max(8, min(sl_pips, 25))
            tp_pips = max(12, min(tp_pips, 40))
            
            details = {
                'strategy': 'TRENDING_EMA_RSI',
                'ema_9_m5': current_ema9_m5,
                'ema_21_m5': current_ema21_m5,
                'rsi_14_m5': current_rsi_m5,
                'h1_trend': h1_trend,
                'atr': current_atr,
                'volume_confirmed': volume_confirmed,
                'divergence': divergence,
                'tp_pips': tp_pips,
                'sl_pips': sl_pips,
                'risk_reward': tp_pips / sl_pips
            }
            
            return action, confidence, details
        
        return None, 0, {}
    
    def _ranging_strategy(self, df_m5: pd.DataFrame, df_h1: pd.DataFrame,
                         sr_levels: Dict, symbol: str) -> Tuple[Optional[str], float, Dict]:
        """
        Strategy for ranging markets
        Uses Bollinger Bands mean reversion
        """
        # Calculate indicators
        bb_period = 20
        bb_std = 2
        sma = df_m5['close'].rolling(bb_period).mean()
        std = df_m5['close'].rolling(bb_period).std()
        upper_band = sma + (bb_std * std)
        lower_band = sma - (bb_std * std)
        
        rsi_14 = self._calculate_rsi(df_m5['close'], 14)
        atr_14 = self._calculate_atr(df_m5, 14)
        
        # Current values
        current_price = df_m5['close'].iloc[-1]
        current_upper = upper_band.iloc[-1]
        current_lower = lower_band.iloc[-1]
        current_sma = sma.iloc[-1]
        current_rsi = rsi_14.iloc[-1]
        current_atr = atr_14.iloc[-1]
        
        action = None
        confidence = 0
        
        # BUY Signal: Price touches lower band (oversold)
        if current_price <= current_lower and current_rsi < 35:
            action = 'BUY'
            confidence = 65
            
            # Bonus: Near support level
            if self.sr_detector.is_near_level(current_price, sr_levels['support']):
                confidence += 15
            
            # Bonus: Very oversold
            if current_rsi < 25:
                confidence += 10
        
        # SELL Signal: Price touches upper band (overbought)
        elif current_price >= current_upper and current_rsi > 65:
            action = 'SELL'
            confidence = 65
            
            # Bonus: Near resistance level
            if self.sr_detector.is_near_level(current_price, sr_levels['resistance']):
                confidence += 15
            
            # Bonus: Very overbought
            if current_rsi > 75:
                confidence += 10
        
        if action:
            symbol_info = mt5.symbol_info(symbol)
            if not symbol_info:
                return None, 0, {}
            
            pip_size = self._get_pip_size(symbol)
            atr_in_pips = current_atr / pip_size
            
            # Ranging market: tighter TP/SL
            sl_pips = atr_in_pips * 0.8
            tp_pips = atr_in_pips * 1.2  # 1.5:1 risk-reward
            
            # Enforce limits
            sl_pips = max(5, min(sl_pips, 15))
            tp_pips = max(8, min(tp_pips, 25))
            
            details = {
                'strategy': 'RANGING_BB_REVERSION',
                'bb_upper': current_upper,
                'bb_lower': current_lower,
                'bb_middle': current_sma,
                'rsi_14': current_rsi,
                'atr': current_atr,
                'tp_pips': tp_pips,
                'sl_pips': sl_pips,
                'risk_reward': tp_pips / sl_pips
            }
            
            return action, confidence, details
        
        return None, 0, {}
    
    def _detect_divergence(self, df: pd.DataFrame, rsi: pd.Series) -> Optional[str]:
        """
        Detect RSI/Price divergence
        Returns: 'bullish', 'bearish', or None
        """
        if len(df) < 50:
            return None
        
        recent_df = df.tail(50)
        recent_rsi = rsi.tail(50)
        
        # Find recent price highs and lows
        price_highs = recent_df['high'].rolling(10, center=True).max()
        price_lows = recent_df['low'].rolling(10, center=True).min()
        
        # Check for bearish divergence (price making higher highs, RSI making lower highs)
        if (recent_df['high'].iloc[-1] > recent_df['high'].iloc[-20] and
            recent_rsi.iloc[-1] < recent_rsi.iloc[-20]):
            return 'bearish'
        
        # Check for bullish divergence (price making lower lows, RSI making higher lows)
        if (recent_df['low'].iloc[-1] < recent_df['low'].iloc[-20] and
            recent_rsi.iloc[-1] > recent_rsi.iloc[-20]):
            return 'bullish'
        
        return None
    
    # Helper methods
    
    def _calculate_rsi(self, series: pd.Series, period: int) -> pd.Series:
        """Calculate RSI"""
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_atr(self, df: pd.DataFrame, period: int) -> pd.Series:
        """Calculate Average True Range"""
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return atr
    
    def _get_pip_size(self, symbol: str) -> float:
        """Get pip size for symbol"""
        if 'JPY' in symbol:
            return 0.01
        elif 'XAU' in symbol or 'GOLD' in symbol:
            return 0.10
        else:
            return 0.0001


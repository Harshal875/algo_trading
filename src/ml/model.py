"""
ML Model for Stock Prediction - Simple but Effective
"""
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))

from data_fetcher import DataFetcher
from indicators import TechnicalIndicators

class StockPredictor:
    def __init__(self):
        print("Stock Predictor initialized!")
        self.data_fetcher = DataFetcher()
        self.indicators = TechnicalIndicators()
        self.models = {}
    
    def prepare_features(self, data):
        """Create features for ML model"""
        print("Preparing ML features...")
        
        # Calculate all indicators
        rsi = self.indicators.calculate_rsi(data['Close'])
        ma20, ma50 = self.indicators.calculate_moving_averages(data['Close'])
        
        # Create feature DataFrame
        features = pd.DataFrame(index=data.index)
        features['RSI'] = rsi
        features['MA20'] = ma20
        features['MA50'] = ma50
        features['Price'] = data['Close']
        features['Volume'] = data['Volume']
        
        # Price-based features
        features['Price_Change'] = data['Close'].pct_change()
        features['High_Low_Ratio'] = data['High'] / data['Low']
        features['MA_Ratio'] = ma20 / ma50
        
        # Target: Next day direction (1 = up, 0 = down)
        features['Next_Day_Up'] = (data['Close'].shift(-1) > data['Close']).astype(int)
        
        # Remove rows with NaN values
        features = features.dropna()
        
        return features
    
    def train_models(self, features):
        """Train ML models for prediction"""
        print("Training ML models...")
        
        # Prepare data for training
        X = features.drop(['Next_Day_Up'], axis=1)
        y = features['Next_Day_Up']
        
        # Split data (80% train, 20% test)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")
        
        # Train Decision Tree
        dt_model = DecisionTreeClassifier(max_depth=5, random_state=42)
        dt_model.fit(X_train, y_train)
        dt_pred = dt_model.predict(X_test)
        dt_accuracy = accuracy_score(y_test, dt_pred)
        
        # Train Logistic Regression
        lr_model = LogisticRegression(random_state=42, max_iter=1000)
        lr_model.fit(X_train, y_train)
        lr_pred = lr_model.predict(X_test)
        lr_accuracy = accuracy_score(y_test, lr_pred)
        
        # Store models
        self.models['decision_tree'] = dt_model
        self.models['logistic_regression'] = lr_model
        
        return {
            'decision_tree_accuracy': dt_accuracy,
            'logistic_regression_accuracy': lr_accuracy,
            'X_test': X_test,
            'y_test': y_test,
            'dt_pred': dt_pred,
            'lr_pred': lr_pred
        }

    def get_feature_importance(self, features):
        """Get feature importance from Decision Tree"""
        if 'decision_tree' not in self.models:
            return None
        
        model = self.models['decision_tree']
        feature_names = features.drop(['Next_Day_Up'], axis=1).columns
        importance = model.feature_importances_
        
        return pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)

# Test it
if __name__ == "__main__":
    import yfinance as yf
    
    predictor = StockPredictor()
    
    # Test feature preparation
    print("Testing feature preparation...")
    data = yf.download("RELIANCE.NS", period="6mo")
    features = predictor.prepare_features(data)
    
    print(f"\n📊 FEATURE ANALYSIS:")
    print(f"Total samples: {len(features)}")
    print(f"Next day UP probability: {features['Next_Day_Up'].mean():.1%}")
    
    # TRAIN MODELS
    results = predictor.train_models(features)
    
    print(f"\n🤖 ML MODEL RESULTS:")
    print(f"Decision Tree Accuracy: {results['decision_tree_accuracy']:.1%}")
    print(f"Logistic Regression Accuracy: {results['logistic_regression_accuracy']:.1%}")
    
    # Feature importance
    importance = predictor.get_feature_importance(features)
    print(f"\n📈 FEATURE IMPORTANCE:")
    for _, row in importance.head(5).iterrows():
        print(f"  {row['feature']}: {row['importance']:.3f}")
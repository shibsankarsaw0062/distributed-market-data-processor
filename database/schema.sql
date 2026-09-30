-- Create the table for processed market features
CREATE TABLE IF NOT EXISTS market_features (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    original_feed VARCHAR(255) NOT NULL,
    trading_signal VARCHAR(10) NOT NULL,
    confidence_score FLOAT NOT NULL
);

-- Example insert query the processing_service will run
-- INSERT INTO market_features (original_feed, trading_signal, confidence_score) 
-- VALUES ('BTC/USD: 64000', 'BUY', 0.85);
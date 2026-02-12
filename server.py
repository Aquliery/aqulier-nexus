import time
import random
from typing import Optional
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- CONFIGURATION ---
VERSION = "1.0.0 (Nexus Core)"
WALLET_ADDRESS = "0x72d1c605f91a0b0ece160d5fe4f56f1e5dc1c798"
PRICE_USDC = "0.1"

app = FastAPI(title="Aqulier Nexus API", version=VERSION)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MOCK AI ENGINE ---
# In a real production env, this would call Gemini Pro.
# For Hackathon demo, we simulate the AI's "thought process".

BULLISH_PHRASES = [
    "Whale accumulation detected at support levels.",
    "Social volume spiking with positive sentiment.",
    "Funding rates are neutral, room for growth.",
    "Institutional inflows observed in ETF data."
]

BEARISH_PHRASES = [
    "High sell pressure detected on Coinbase Pro.",
    "Influencer sentiment turning negative.",
    "Macro headwinds (CPI data) causing friction.",
    "Long liquidations cascading."
]

def generate_ai_insight(ticker: str):
    """Simulates a sophisticated AI analysis."""
    # Deterministic randomness based on time to make it feel alive but stable
    is_bullish = random.choice([True, False])
    
    score = random.randint(60, 95) if is_bullish else random.randint(10, 45)
    sentiment = "Greed" if score > 55 else ("Fear" if score < 45 else "Neutral")
    
    phrases = BULLISH_PHRASES if is_bullish else BEARISH_PHRASES
    insight = f"{random.choice(phrases)} Monitoring {ticker} correlation with S&P500."
    
    return {
        "ticker": ticker,
        "score": score,
        "sentiment": sentiment,
        "insight": insight,
        "compute_time_ms": random.randint(120, 800)
    }

# --- ROUTES ---

@app.get("/")
def health_check():
    return {"system": "Aqulier Nexus", "status": "OPERATIONAL", "payment_protocol": "x402"}

@app.get("/intelligence/{ticker}")
def get_intelligence(ticker: str, authorization: str = Header(None)):
    ticker = ticker.upper()
    
    # 1. x402 Payment Gate
    # Check for valid payment proof (mocked for hackathon with a magic string)
    has_payment = False
    if authorization and "valid_token" in authorization:
        has_payment = True
        
    if not has_payment:
        # Return standard 402 response with payment details
        # This allows the frontend/wallet to auto-detect the payment requirement
        print(f"🛑 [Access Denied] Payment required for {ticker}")
        raise HTTPException(
            status_code=402,
            detail="Payment Required",
            headers={
                "WWW-Authenticate": f'x402 realm="AqulierNexus", chain="SKALE", address="{WALLET_ADDRESS}", token="USDC", amount="{PRICE_USDC}"'
            }
        )

    # 2. AI Execution
    print(f"🟢 [Access Granted] Generating report for {ticker}...")
    report = generate_ai_insight(ticker)
    
    return {
        "meta": {"generated_by": "Aqulier-v1", "timestamp": time.time()},
        "payload": report
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Aqulier Nexus launching on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

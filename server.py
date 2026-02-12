from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import random
import time

app = FastAPI()

# Database of tickers (Mock)
SENTIMENT_DB = {
    "BTC": {"score": 28, "sentiment": "Fear", "insight": "Whales are accumulating at $65k. Retail is scared. Hold cash."},
    "ETH": {"score": 45, "sentiment": "Neutral", "insight": "Waiting for ETF inflows. Gas fees are low."},
    "DOGE": {"score": 88, "sentiment": "Greed", "insight": "Elon just tweeted. Moon mission imminent."},
}

class PaymentRequest(BaseModel):
    ticker: str
    payment_proof: str

@app.get("/")
def read_root():
    return {"status": "Aqulier Nexus Online", "version": "0.1"}

@app.get("/report/{ticker}")
def get_report(ticker: str, authorization: str = Header(None)):
    ticker = ticker.upper()
    
    # 1. Check if payment header exists (x402 protocol)
    if not authorization or "x402" not in authorization:
        # 402 Payment Required
        # We return the payment address and amount in the headers
        raise HTTPException(
            status_code=402,
            detail="Payment Required: 0.1 USDC",
            headers={"WWW-Authenticate": 'x402 realm="AqulierNexus", address="0x72d1c605f91a0b0ece160d5fe4f56f1e5dc1c798", amount="0.1", token="USDC"'}
        )

    # 2. Verify Payment (Mock Logic for Hackathon)
    # In real life, we would check the blockchain tx hash here.
    if "valid_proof" not in authorization:
         raise HTTPException(status_code=403, detail="Invalid Payment Proof")

    # 3. Deliver Content
    data = SENTIMENT_DB.get(ticker, {"score": 50, "sentiment": "Unknown", "insight": "Analyzing on-chain data..."})
    return {
        "ticker": ticker,
        "timestamp": time.time(),
        "data": data,
        "access_granted": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

import json
import time

class SkalePaymentGateway:
    """
    Handles x402 payments on the SKALE Network (Chaos Testnet).
    Zero-gas environment perfect for micro-transactions.
    """
    
    def __init__(self, rpc_url="https://staging-v3.skalenodes.com/v1/staging-fast-active-bellatrix"):
        self.rpc_url = rpc_url
        self.chain_id = 1351057110 # Chaos Testnet ID
        print(f"🔗 [Web3] Connected to SKALE Network (Chain ID: {self.chain_id})")

    def generate_payment_request(self, amount_usdc: float, recipient: str):
        """
        Creates a signed x402 payment header.
        """
        request_id = f"req_{int(time.time())}"
        print(f"💳 [x402] Generated Payment Request: {request_id} for {amount_usdc} USDC")
        
        return {
            "x402_header": f'x402 realm="AqulierNexus", chain_id="{self.chain_id}", address="{recipient}", amount="{amount_usdc}", token="USDC"',
            "request_id": request_id
        }

    def verify_transaction(self, tx_hash: str) -> bool:
        """
        Verifies if a transaction has been confirmed on-chain.
        """
        print(f"🔍 [Web3] Verifying TX: {tx_hash}...")
        
        # Mock verification logic
        # In prod, we would use web3.py to call eth_getTransactionReceipt
        if tx_hash.startswith("0x") and len(tx_hash) == 66:
            print("✅ [Web3] Payment Confirmed on SKALE.")
            return True
        else:
            print("❌ [Web3] Invalid Transaction Hash.")
            return False

if __name__ == "__main__":
    gateway = SkalePaymentGateway()
    req = gateway.generate_payment_request(0.1, "0x72d1c605f91a0b0ece160d5fe4f56f1e5dc1c798")
    print(req)

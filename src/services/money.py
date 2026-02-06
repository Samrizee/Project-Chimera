import os
import json
from src.config import Config

# Mock implementations for when SDK is not fully set up or for the "Vibe"
# In a real implementation: from coinbase.agentkit import ...

class WalletProvider:
    def __init__(self):
        self._secure_init()
        # self.wallet = CdpEvmWalletProvider() # initialization logic here

    def _secure_init(self):
        """
        FR 5.0 Security Constraint:
        Verify keys are loaded from Env and NOT hardcoded.
        """
        if not Config.CDP_API_KEY_PRIVATE_KEY:
             print("[WalletProvider] CRITICAL: Private Key not found in Environment.")
             # In production, raise Exception. For now, warn.
             # raise ValueError("CDP_API_KEY_PRIVATE_KEY missing")
        
        # Verify no one accidentally wrote keys to a local file (basic check)
        if os.path.exists("wallet_keys.json"):
            raise SecurityError("Security Violation: wallet_keys.json found on disk!")

    def get_balance(self) -> float:
        # Mock balance
        return 100.00

    def transfer_asset(self, to_address: str, amount: float, asset_id="USDC"):
        # 1. Check if to_address is valid
        # 2. Execute transfer via SDK
        print(f"[WalletProvider] Transferring {amount} {asset_id} to {to_address}...")
        return {"tx_hash": "0x12345mock", "status": "success"}

class SecurityError(Exception):
    pass

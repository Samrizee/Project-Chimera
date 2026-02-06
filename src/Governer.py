import time
import redis
import json
from enum import Enum
from src.config import Config

class BudgetStatus(Enum):
    ALLOW = "allow"
    WARN = "warn"
    BLOCK = "block"

class ResourceGovernor:
    def __init__(self, redis_client=None):
        self.redis = redis_client or redis.Redis.from_url(Config.REDIS_URL, decode_responses=True)
        self.max_daily = Config.MAX_DAILY_SPEND_USDC
        self.key_prefix = "governance:budget:"

    def _get_daily_key(self, agent_id: str) -> str:
        # Rotate key daily to reset budget
        timestamp = time.strftime("%Y-%m-%d")
        return f"{self.key_prefix}{agent_id}:{timestamp}"

    def check_request(self, agent_id: str, estimated_cost: float) -> BudgetStatus:
        """
        Check if the request can be fulfilled within the budget.
        Returns ALLOW, WARN (if >80%), or BLOCK (if >100%).
        Does NOT deduct the amount; just checks.
        """
        key = self._get_daily_key(agent_id)
        current_spend = float(self.redis.get(key) or 0.0)
        
        projected_total = current_spend + estimated_cost
        
        usage_ratio = projected_total / self.max_daily
        
        if usage_ratio > 1.0:
            return BudgetStatus.BLOCK
        elif usage_ratio > 0.8:
            return BudgetStatus.WARN
        else:
            return BudgetStatus.ALLOW

    def record_spend(self, agent_id: str, amount: float):
        """
        Atomically increment the spend.
        """
        key = self._get_daily_key(agent_id)
        self.redis.incrbyfloat(key, amount)
        # Set expiry for 48 hours to clean up old keys eventually
        self.redis.expire(key, 172800)

if __name__ == "__main__":
    # Test stub
    gov = ResourceGovernor()
    status = gov.check_request("agent-001", 5.0)
    print(f"Status for $5: {status}")

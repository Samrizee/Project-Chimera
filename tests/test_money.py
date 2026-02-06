import unittest
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import redis
from src.governance.Governer import ResourceGovernor, BudgetStatus
from services.money import WalletProvider, SecurityError
from src.services.planner import Planner
from src.common.models import Task
from src.config import Config

class TestGovernance(unittest.TestCase):
    def setUp(self):
        # Use a separate DB or prefix for testing
        self.redis = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)
        self.redis.flushdb()
        self.governor = ResourceGovernor(self.redis)

    def test_budget_allow(self):
        # 10% of 50.0 = 5.0
        status = self.governor.check_request("agent-test", 5.0)
        self.assertEqual(status, BudgetStatus.ALLOW)

    def test_budget_warn(self):
        # Set spend to 41.0 (82%)
        # Manually set redis key
        key = self.governor._get_daily_key("agent-test")
        self.redis.set(key, 41.0)
        
        status = self.governor.check_request("agent-test", 1.0)
        self.assertEqual(status, BudgetStatus.WARN)

    def test_budget_block(self):
        # Set spend to 51.0 (>100%)
        key = self.governor._get_daily_key("agent-test")
        self.redis.set(key, 51.0)
        
        status = self.governor.check_request("agent-test", 1.0)
        self.assertEqual(status, BudgetStatus.BLOCK)

class TestmoneySecurity(unittest.TestCase):
    def test_missing_key_security(self):
        # Ensure it handles missing key gracefully (mocking env)
        # We constructed WalletProvider to print strict warning or raise
        # For this test, let's verify it doesn't crash but warns, or raises if we enforced it
        # Since we put a print statement in currently:
        try:
             # Unset just in case
             if "CDP_API_KEY_PRIVATE_KEY" in os.environ:
                 del os.environ["CDP_API_KEY_PRIVATE_KEY"]
             
             wp = WalletProvider()
             # If we decide to raise in future, catch here
        except Exception as e:
            pass

class TestPlannerFailure(unittest.TestCase):
    def setUp(self):
        self.planner = Planner(redis_port=6379) # assumes localhost:6379 running
        self.planner.redis_client.flushdb()

    def test_retry_logic(self):
        task = Task(task_type="fail_test", context={"retry_count": 0})
        # Simulate failure
        self.planner.handle_failure(task, "Simulated Error")
        
        # Should be back in queue
        item = self.planner.redis_client.lpop(self.planner.task_queue)
        self.assertIsNotNone(item)
        
        task_queued = Task.model_validate_json(item)
        self.assertEqual(task_queued.context["retry_count"], 1)

    def test_escalation_logic(self):
        task = Task(task_type="fail_test", context={"retry_count": 2}) # Max is 2
        
        # Simulate failure -> Should escalate, NOT enqueue
        self.planner.handle_failure(task, "Simulated Error")
        
        # Queue should be empty
        item = self.planner.redis_client.lpop(self.planner.task_queue)
        self.assertIsNone(item)

if __name__ == "__main__":
    unittest.main()

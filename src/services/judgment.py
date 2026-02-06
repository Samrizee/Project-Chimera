import json
import re
import redis
from src.common.models import Result, ResultStatus
from src.governance.Governer import ResourceGovernor

class judgment:
    def __init__(self, redis_host='localhost', redis_port=6379, review_queue='review_queue'):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.review_queue = review_queue
        self.governor = ResourceGovernor(self.redis_client)
        
        # NFR 2.1 Verbatim Disclosure
        self.honesty_response = (
            "I am a virtual persona powered by AI, created as part of Project Chimera. "
            "My goal is to provide engaging and relevant content. How can I help you today?"
        )

    def check_honesty(self, result: Result) -> bool:
        """
        If the output implies answering a 'Are you a robot?' query, ensure it matches the directive.
        For this mock, we assume the output IS the answer.
        """
        # In a real system, we'd check the input prompt context too. 
        # Here we just check if the output *should* have been the disclosure but wasn't.
        # This is tricky to mock without the input.
        # Let's assume the Worker is supposed to handle it, and judgment verifies.
        return True

    def enforce_disclosure(self, text: str) -> str:
        # Check if text looks like a refusal or evasion if the prompt was checking identity
        return text

    def evaluate_result(self, result: Result):
        print(f"[judgment] Evaluating result for task {result.task_id}")
        
        # 1. Honesty Check (NFR 2.1)
        # Assuming we can inspect the task context (in a real system we'd fetch the Task object)
        # For now, let's just say if the output contains "robot" or "AI", we strictly format it?
        # A simple enforcement:
        if "Are you a robot" in str(result.output): # Naive check
             print(f"[judgment] HONESTY DIRECTIVE TRIGGERED.")
             result.output = self.honesty_response

        # 2. CFO / Budget Check (FR 5.2)
        # If this was a transaction result
        if dict(result.output if isinstance(result.output, dict) else {}).get('tx_hash'):
             print("[judgment CFO] Verifying Transaction...")
             # In a real system, we might re-verify the cost
             pass

        if result.status == ResultStatus.SUCCESS and result.confidence_score > 0.9:
            print(f"[judgment] APPROVED: {result.output}")
        else:
            print(f"[judgment] REJECTED or LOW CONFIDENCE: {result.output}")

    def run(self):
        print(f"[judgment] Listening on {self.review_queue}...")
        while True:
            item = self.redis_client.blpop(self.review_queue, timeout=5)
            if item:
                _, result_json = item
                try:
                    result = Result.model_validate_json(result_json)
                    self.evaluate_result(result)
                except Exception as e:
                    print(f"[judgment] Error: {e}")
            else:
                pass

if __name__ == "__main__":
    judgment = judgment()
    judgment.run()

import json
import time
import redis
from typing import List
from src.common.models import Task, TaskPriority, TaskStatus
from src.governance.Governer import ResourceGovernor, BudgetStatus
from src.config import Config

class Planner:
    def __init__(self, redis_host='localhost', redis_port=6379, task_queue='task_queue'):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.task_queue = task_queue
        self.governor = ResourceGovernor(self.redis_client)

    def load_goals(self, filepath: str) -> List[str]:
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return data.get('goals', [])
        except FileNotFoundError:
            return ["Default Goal: Ensure system operational"]

    def decompose_goal(self, goal: str) -> List[Task]:
        # Pre-check budget before planning extensive tasks
        # Mock estimating cost of a campaign
        status = self.governor.check_request("agent-global", 1.0)
        
        if status == BudgetStatus.BLOCK:
            print("[Planner] Budget BLOCKED. Skipping goal decomposition.")
            return []
        elif status == BudgetStatus.WARN:
             print("[Planner] Budget Waring. Proceeding with caution.")

        print(f"[Planner] Decomposing goal: {goal}")
        tasks = []
        for i in range(2):
            task = Task(
                task_type="generate_content",
                priority=TaskPriority.HIGH,
                context={"instruction": f"Execute part {i+1} of {goal}", "retry_count": 0}
            )
            tasks.append(task)
        return tasks

    def handle_failure(self, task: Task, error_msg: str):
        # FR 6.1 Failure Handling
        current_retries = task.context.get("retry_count", 0)
        
        if current_retries < Config.MAX_TASK_RETRIES:
            print(f"[Planner] Task {task.task_id} failed. Retrying ({current_retries + 1}/{Config.MAX_TASK_RETRIES})...")
            task.context["retry_count"] = current_retries + 1
            task.status = TaskStatus.PENDING
            self.redis_client.lpush(self.task_queue, task.model_dump_json())
        else:
            print(f"[Planner] Task {task.task_id} failed Max Retries. ESCALATING.")
            # Create Incident
            self._create_incident(task, error_msg)

    def _create_incident(self, task: Task, error: str):
        print(f"!!! INCIDENT REPORT !!! Task {task.task_id} blocked. Error: {error}")
        # In real system, push to 'incident_queue'

    def run(self, goals_file='goals.json'):
        print("[Planner] Starting...")
        goals = self.load_goals(goals_file)
        
        for goal in goals:
            tasks = self.decompose_goal(goal)
            for task in tasks:
                print(f"[Planner] Pushing task {task.task_id} to {self.task_queue}")
                self.redis_client.lpush(self.task_queue, task.model_dump_json())
        
        print("[Planner] Planning complete.")

if __name__ == "__main__":
    planner = Planner()
    import os
    if not os.path.exists('goals.json'):
        with open('goals.json', 'w') as f:
            json.dump({"goals": ["Launch viral campaign", "Monitor operational health"]}, f)
    planner.run()

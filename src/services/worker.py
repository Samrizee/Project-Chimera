import json
import time
import redis
import uuid
from src.common.models import Task, Result, ResultStatus

class Worker:
    def __init__(self, worker_id=None, redis_host='localhost', redis_port=6379, task_queue='task_queue', review_queue='review_queue'):
        self.worker_id = worker_id or str(uuid.uuid4())
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.task_queue = task_queue
        self.review_queue = review_queue

    def process_task(self, task: Task) -> Result:
        print(f"[Worker {self.worker_id}] Processing task {task.task_id}: {task.context}")
        # Simulate work
        time.sleep(2)
        
        output = f"Processed content for {task.context.get('instruction')}"
        
        return Result(
            task_id=task.task_id,
            worker_id=self.worker_id,
            output=output,
            confidence_score=0.95,
            status=ResultStatus.SUCCESS
        )

    def run(self):
        print(f"[Worker {self.worker_id}] Listening on {self.task_queue}...")
        while True:
            # BLPOP blocks until a generic item is available
            # returns tuple (queue_name, data)
            item = self.redis_client.blpop(self.task_queue, timeout=5)
            if item:
                _, task_json = item
                try:
                    task = Task.model_validate_json(task_json)
                    result = self.process_task(task)
                    print(f"[Worker {self.worker_id}] Pushing result to {self.review_queue}")
                    self.redis_client.lpush(self.review_queue, result.model_dump_json())
                except Exception as e:
                    print(f"[Worker {self.worker_id}] Error: {e}")
            else:
                pass # Timeout, loop again

if __name__ == "__main__":
    worker = Worker()
    worker.run()

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETE = "complete"
    FAILED = "failed"

class TaskPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Task(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    task_type: str
    priority: TaskPriority = TaskPriority.MEDIUM
    context: Dict[str, Any] = Field(default_factory=dict)
    assigned_worker_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: TaskStatus = TaskStatus.PENDING

class ResultStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"

class Result(BaseModel):
    task_id: str
    worker_id: str
    output: Any
    confidence_score: float = 0.0
    status: ResultStatus
    executed_at: datetime = Field(default_factory=datetime.utcnow)
    error: Optional[str] = None

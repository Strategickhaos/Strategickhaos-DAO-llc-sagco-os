#!/usr/bin/env python3
"""
SAGCO OS Scheduler
Task scheduling and execution management
"""

from dataclasses import dataclass, field
from typing import Callable, Any, Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum, auto
import threading
import time
from queue import PriorityQueue


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Task:
    """Scheduled task"""
    task_id: str
    name: str
    func: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    priority: TaskPriority = TaskPriority.NORMAL
    scheduled_time: datetime = field(default_factory=datetime.now)
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[Exception] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def __lt__(self, other: 'Task') -> bool:
        """For priority queue ordering"""
        if self.priority.value != other.priority.value:
            return self.priority.value > other.priority.value
        return self.scheduled_time < other.scheduled_time


@dataclass
class RecurringTask:
    """Task that runs on a schedule"""
    task_id: str
    name: str
    func: Callable
    interval: timedelta
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    next_run: datetime = field(default_factory=datetime.now)
    last_run: Optional[datetime] = None
    run_count: int = 0
    active: bool = True


class Scheduler:
    """
    Task scheduler for SAGCO OS
    Supports one-time and recurring tasks with priority
    """
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.task_queue: PriorityQueue = PriorityQueue()
        self.tasks: Dict[str, Task] = {}
        self.recurring_tasks: Dict[str, RecurringTask] = {}
        self.workers: List[threading.Thread] = []
        self.running = False
        self.lock = threading.RLock()
        self.task_counter = 0
        self.stats = {
            "scheduled": 0,
            "completed": 0,
            "failed": 0,
            "cancelled": 0
        }
    
    def _generate_task_id(self) -> str:
        """Generate unique task ID"""
        with self.lock:
            self.task_counter += 1
            return f"task-{self.task_counter}-{int(time.time()*1000)}"
    
    def schedule(
        self,
        func: Callable,
        name: Optional[str] = None,
        args: tuple = (),
        kwargs: Optional[Dict[str, Any]] = None,
        delay: Optional[timedelta] = None,
        priority: TaskPriority = TaskPriority.NORMAL
    ) -> str:
        """Schedule a one-time task"""
        task_id = self._generate_task_id()
        scheduled_time = datetime.now()
        if delay:
            scheduled_time += delay
        
        task = Task(
            task_id=task_id,
            name=name or func.__name__,
            func=func,
            args=args,
            kwargs=kwargs or {},
            priority=priority,
            scheduled_time=scheduled_time
        )
        
        with self.lock:
            self.tasks[task_id] = task
            self.task_queue.put(task)
            self.stats["scheduled"] += 1
        
        return task_id
    
    def schedule_recurring(
        self,
        func: Callable,
        interval: timedelta,
        name: Optional[str] = None,
        args: tuple = (),
        kwargs: Optional[Dict[str, Any]] = None
    ) -> str:
        """Schedule a recurring task"""
        task_id = self._generate_task_id()
        
        recurring = RecurringTask(
            task_id=task_id,
            name=name or func.__name__,
            func=func,
            interval=interval,
            args=args,
            kwargs=kwargs or {},
            next_run=datetime.now() + interval
        )
        
        with self.lock:
            self.recurring_tasks[task_id] = recurring
        
        return task_id
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending task"""
        with self.lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                if task.status == TaskStatus.PENDING:
                    task.status = TaskStatus.CANCELLED
                    self.stats["cancelled"] += 1
                    return True
            
            if task_id in self.recurring_tasks:
                self.recurring_tasks[task_id].active = False
                return True
        
        return False
    
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """Get task status"""
        with self.lock:
            if task_id in self.tasks:
                return self.tasks[task_id].status
        return None
    
    def get_task_result(self, task_id: str) -> Any:
        """Get task result (blocks if running)"""
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        # Wait for task to complete
        while task.status == TaskStatus.RUNNING:
            time.sleep(0.1)
        
        return task.result
    
    def _execute_task(self, task: Task) -> None:
        """Execute a single task"""
        from src.core.logger import get_logger
        logger = get_logger("scheduler")
        
        with self.lock:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
        
        try:
            result = task.func(*task.args, **task.kwargs)
            with self.lock:
                task.status = TaskStatus.COMPLETED
                task.result = result
                task.completed_at = datetime.now()
                self.stats["completed"] += 1
        
        except Exception as e:
            with self.lock:
                task.status = TaskStatus.FAILED
                task.error = e
                task.completed_at = datetime.now()
                self.stats["failed"] += 1
            logger.error(f"Task {task.name} failed", exception=e, task_id=task.task_id)
    
    def _worker_loop(self) -> None:
        """Worker thread loop"""
        while self.running:
            try:
                # Get task with timeout
                task = self.task_queue.get(timeout=0.1)
                
                # Wait if task is scheduled for future
                now = datetime.now()
                if task.scheduled_time > now:
                    wait_seconds = (task.scheduled_time - now).total_seconds()
                    time.sleep(min(wait_seconds, 1.0))
                    # Re-queue if still in future
                    if task.scheduled_time > datetime.now():
                        self.task_queue.put(task)
                        continue
                
                # Execute if not cancelled
                if task.status == TaskStatus.PENDING:
                    self._execute_task(task)
                
                self.task_queue.task_done()
            
            except Exception as e:
                # Queue was empty or other error
                pass
    
    def _recurring_loop(self) -> None:
        """Check and schedule recurring tasks"""
        from src.core.logger import get_logger
        logger = get_logger("scheduler.recurring")
        
        while self.running:
            try:
                time.sleep(1.0)  # Check every second
                
                now = datetime.now()
                with self.lock:
                    for recurring in list(self.recurring_tasks.values()):
                        if not recurring.active:
                            continue
                        
                        if now >= recurring.next_run:
                            # Schedule execution
                            self.schedule(
                                recurring.func,
                                name=f"{recurring.name} (recurring)",
                                args=recurring.args,
                                kwargs=recurring.kwargs
                            )
                            
                            # Update recurring task
                            recurring.last_run = now
                            recurring.next_run = now + recurring.interval
                            recurring.run_count += 1
            
            except Exception as e:
                logger.error("Recurring loop error", exception=e)
    
    def start(self) -> None:
        """Start scheduler workers"""
        if self.running:
            return
        
        self.running = True
        
        # Start worker threads
        for i in range(self.max_workers):
            worker = threading.Thread(
                target=self._worker_loop,
                name=f"scheduler-worker-{i}",
                daemon=True
            )
            worker.start()
            self.workers.append(worker)
        
        # Start recurring task thread
        recurring_thread = threading.Thread(
            target=self._recurring_loop,
            name="scheduler-recurring",
            daemon=True
        )
        recurring_thread.start()
        self.workers.append(recurring_thread)
    
    def stop(self) -> None:
        """Stop scheduler"""
        self.running = False
        for worker in self.workers:
            worker.join(timeout=1.0)
        self.workers.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get scheduler statistics"""
        with self.lock:
            pending = sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING)
            running = sum(1 for t in self.tasks.values() if t.status == TaskStatus.RUNNING)
            
            return {
                "stats": self.stats.copy(),
                "queue_size": self.task_queue.qsize(),
                "total_tasks": len(self.tasks),
                "pending": pending,
                "running": running,
                "recurring_tasks": len(self.recurring_tasks),
                "active_recurring": sum(1 for r in self.recurring_tasks.values() if r.active),
                "workers": self.max_workers,
                "running": self.running
            }
    
    def get_task_list(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get list of recent tasks"""
        with self.lock:
            recent_tasks = sorted(
                self.tasks.values(),
                key=lambda t: t.created_at,
                reverse=True
            )[:limit]
            
            return [
                {
                    "task_id": t.task_id,
                    "name": t.name,
                    "status": t.status.name,
                    "priority": t.priority.name,
                    "created_at": t.created_at.isoformat(),
                    "scheduled_time": t.scheduled_time.isoformat(),
                }
                for t in recent_tasks
            ]


def get_scheduler() -> Scheduler:
    """Get singleton scheduler instance"""
    if not hasattr(get_scheduler, '_instance'):
        get_scheduler._instance = Scheduler()
        get_scheduler._instance.start()
    return get_scheduler._instance

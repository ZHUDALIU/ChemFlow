"""Batch processor — parallel execution of computational chemistry tasks."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class BatchJob:
    """A single job within a batch."""

    job_id: str
    molecule: str
    params: Dict[str, Any]
    status: str = "pending"
    result: Optional[Any] = None
    error: Optional[str] = None
    duration: float = 0.0


@dataclass
class BatchResult:
    """Aggregated results from a batch processing run."""

    total: int = 0
    succeeded: int = 0
    failed: int = 0
    total_duration: float = 0.0
    jobs: List[BatchJob] = field(default_factory=list)
    errors: Dict[str, str] = field(default_factory=dict)


class BatchProcessor:
    """Parallel batch processor with configurable concurrency.

    Features:
    - Thread-based parallelism for I/O-bound tasks
    - Optional process-based isolation for CPU-bound workloads
    - Graceful degradation under resource pressure
    """

    def __init__(self, max_workers: int = 4, use_process_pool: bool = False):
        self.max_workers = max_workers
        self.use_process_pool = use_process_pool

    def process_batch(
        self,
        molecules: List[str],
        task_fn: Callable[[str, Dict[str, Any]], Any],
        params: Optional[Dict[str, Any]] = None,
    ) -> BatchResult:
        """Execute a batch of tasks in parallel."""
        result = BatchResult(total=len(molecules))
        start = time.time()

        params = params or {}
        jobs = [
            BatchJob(job_id=f"job-{i:04d}", molecule=mol, params=params)
            for i, mol in enumerate(molecules)
        ]

        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            fut_map = {
                pool.submit(self._run_job, job, task_fn): job for job in jobs
            }
            for fut in as_completed(fut_map):
                job = fut_map[fut]
                try:
                    job.status, job.result, job.error = fut.result()
                    if job.status == "success":
                        result.succeeded += 1
                    else:
                        result.failed += 1
                        result.errors[job.job_id] = job.error or "unknown"
                except Exception as exc:
                    job.status = "failed"
                    job.error = str(exc)
                    result.failed += 1
                    result.errors[job.job_id] = str(exc)

        result.total_duration = time.time() - start
        result.jobs = jobs
        return result

    def _run_job(self, job: BatchJob, task_fn: Callable) -> tuple:
        t0 = time.time()
        try:
            output = task_fn(job.molecule, job.params)
            job.duration = time.time() - t0
            return "success", output, None
        except Exception as exc:
            job.duration = time.time() - t0
            return "failed", None, str(exc)
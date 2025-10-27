"""TODO."""
import threading  # noqa: I001
from pathlib import Path
import sys
from typing import Optional

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent))

from celery.result import AsyncResult
from flask import Blueprint, jsonify, render_template, request, url_for
from pi_calculator import get_digits_of_pi

pi_result_page = Blueprint("pi_result_page", __name__)

# track the last created task id (process-wide)
# last_task_id: Optional[str] = None
# _last_task_lock = threading.Lock()

@pi_result_page.route("/calculate_pi", methods=["GET"])
def result_page() -> str:
    """
    Single endpoint to start and poll the Celery task.
    - If no `task_id` query param: start a task and render "calculating..." with a meta-refresh
      back to the same endpoint including `task_id` and `n`.
    - If `task_id` is present: check the task. If ready render final result, otherwise re-render
      "calculating..." with a meta-refresh back to this endpoint.
    """  # noqa: D205
    # robust parsing of n
    try:
        num_digits = int(request.args.get("n", "1"))
    except (TypeError, ValueError):
        num_digits = 1

    task_id = request.args.get("task_id")

    # Start a new task when no task_id is provided
    if not task_id:
        task = get_digits_of_pi.delay(num_digits)
        poll_url = url_for(".result_page", task_id=task.id, n=num_digits)
        return render_template(
            "result_page.html",
            num_digits=num_digits,
            result="calculating...",
            task_id=task.id,
            refresh_interval=2,
            refresh_url=poll_url,
        )

    # Poll an existing task
    task = AsyncResult(task_id)
    if task.ready():
        try:
            final = task.get(timeout=1)
            if num_digits == 1:
                try:
                    final = int(final)
                except Exception:
                    pass
        except Exception as exc:
            final = f"Error: {exc}"

        return render_template(
            "result_page.html",
            num_digits=num_digits,
            result=str(final),
            task_id=task_id,
            refresh_interval=0,
            refresh_url="",
        )

    # Still running -> re-render calculating page that refreshes to this endpoint
    poll_url = url_for(".result_page", task_id=task_id, n=num_digits)
    return render_template(
        "result_page.html",
        num_digits=num_digits,
        result="calculating...",
        task_id=task_id,
        refresh_interval=0.5,
        refresh_url=poll_url,
    )


@pi_result_page.route("/check_progress", methods=["GET"])
def check_progress():
    """
    Return JSON with the Celery task state and result (when ready).
    Query params:
      - task_id: required Celery task id
    Example: GET /check_progress?task_id=<id>
    """  # noqa: D400
    task_id = request.args.get("task_id")
    if not task_id:
        return jsonify({"error": "missing task_id"}), 400

    task = AsyncResult(task_id)
    payload = {"state": task.state}

    if task.ready():
        try:
            payload["result"] = task.get(timeout=1)
        except Exception as exc:
            payload["result"] = None
            payload["error"] = str(exc)

    return jsonify(payload)
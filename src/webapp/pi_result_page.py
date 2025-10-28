"""File implementing the result page endpoint of the pi calculator."""
from pathlib import Path
import sys

# add the src directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent))

from celery.result import AsyncResult
from flask import Blueprint, Response, jsonify, render_template, request, url_for

from .pi_calculator import MAX_NUMBER_OF_DIGITS, get_digits_of_pi

pi_result_page = Blueprint("pi_result_page", __name__)


@pi_result_page.route("/calculate_pi", methods=["GET"])
def result_page() -> str:
    """
    Start a new celery task to calculate digits of pi according to 'n' provided in url parameters
    or polls an existing task if one is provided in the url parameters.

    :return: rendered html page with the final result or a placeholder indicating calculation in progress
    """  # noqa: D205
    # read number of digits from url parameters -> if invalid default to 1
    try:
        num_digits = int(request.args.get("n", "1"))
        if num_digits < 1 or num_digits > MAX_NUMBER_OF_DIGITS:
            num_digits = 1
    except (TypeError, ValueError):
        num_digits = 1

    # get task_id from url parameters -> if missing start a new task
    task_id = request.args.get("task_id")

    if not task_id:
        #  if no task present -> start a new task
        task = get_digits_of_pi.delay(num_digits)
        poll_url = url_for(".result_page", task_id=task.id, n=num_digits)
        return render_template(
            "result_page.html",
            num_digits=num_digits,
            result="...",
            task_id=task.id,
            refresh_interval=2,
            refresh_url=poll_url,
        )

    # if task present -> poll the existing task
    task = AsyncResult(task_id)
    if task.ready():
        # if task finished -> get the result and render it
        try:
            final = task.info.get("result")
            if num_digits == 1:
                # if only 1 digit requested -> convert to int to avoid trailing .0
                final = int(final)
        except Exception as exc:  # noqa: BLE001 # need to catch Exception since task.get raises it
            final = f"Error: {exc}"

        return render_template(
            "result_page.html",
            num_digits=num_digits,
            result=str(final),
            task_id=task_id,
            refresh_interval=0,
            refresh_url="",
        )

    # still running -> re-render calculating page that refreshes to this endpoint
    poll_url = url_for(".result_page", task_id=task_id, n=num_digits)
    return render_template(
        "result_page.html",
        num_digits=num_digits,
        result="...",
        task_id=task_id,
        refresh_interval=1,
        refresh_url=poll_url,
    )


@pi_result_page.route("/check_progress", methods=["GET"])
def check_progress() -> tuple[Response, int]:
    """
    Check the progress of an existing celery task provided in the url parameters.

    :return: HTTP response with json payload containing the task state and result (if ready)
    """
    task_id = request.args.get("task_id")
    if not task_id:
        # missing task_id in url parameters -> bad request (can't check progress for non existing task)
        return jsonify({"error": "missing task_id"}), 400

    # get the task status
    task = AsyncResult(task_id)
    payload = {}
    match task.state:
        case "PENDING":
            payload["state"] = "PROGRESS"
        case "SUCCESS":
            payload["state"] = "FINISHED"
        case _:
            payload["state"] = task.state

    # try to extract progress/meta published by ProgressRecorder / update_state
    info = task.info
    if isinstance(info, dict):
        current = info.get("current")
        total = info.get("total")
        if current is not None and total is not None:
            payload["progress"] = current / total
        else:
            payload["progress"] = None # type: ignore[assignment]

    if task.ready():
        # if task is ready -> try to get the result
        try:
            payload["result"] = task.info.get("result")
        except Exception as exc: # noqa: BLE001 # need to catch Exception since task.get raises it
            payload["result"] = None  # type: ignore[assignment]
            payload["error"] = str(exc)
    else:
        payload["result"] = None # type: ignore[assignment]
    return jsonify(payload), 200

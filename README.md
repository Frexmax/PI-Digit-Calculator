# PI-Digit-Calculator
App to calculate digits of pi using Celery - project for the PostTagger Reimagined internship application

[![Build](https://github.com/Frexmax/PI-Digit-Calculator/actions/workflows/build.yml/badge.svg)](https://github.com/Frexmax/PI-Digit-Calculator/actions/workflows/build.yml)
[![Mypy](https://github.com/Frexmax/PI-Digit-Calculator/actions/workflows/mypy.yml/badge.svg)](https://github.com/Frexmax/PI-Digit-Calculator/actions/workflows/mypy.yml)
[![Test](https://github.com/Frexmax/PI-Digit-Calculator/actions/workflows/test.yml/badge.svg)](https://github.com/Frexmax/PI-Digit-Calculator/actions/workflows/test.yml)
[![Docker Image](https://github.com/Frexmax/PI-Digit-Calculator/actions/workflows/docker-image.yml/badge.svg)](https://github.com/Frexmax/PI-Digit-Calculator/actions/workflows/docker-image.yml)

# API Documentation

### GET `/` — Home page
- Purpose: Display the calculator UI - let the user type in the needded number of digits in a form
- Response: HTML page (renders the form where the user can specify the needed number of digits).
- Implemented in: `src/webapp/pi_home_page.py`

Example:
- Request: `GET /`
- Response: `200 OK` with HTML content.

### GET `/calculate_pi` — Do the PI calculation
- Purpose: Enqueue a Celery task to compute digits of Pi with requested parameters.
- Query parameters:
  - `n` (integer) — number of digits to compute.
- Response (JSON):
  - HTML page (renders the result of the computation or '...' if the computation isn't finished yet).
- Implemented in: `src/webapp/pi_result_page.py` 

Notes:
- The client should store `task_id` for progress/result polling.

### GET `/check_progress` — Check task progress and status
- Purpose: Return status, progress and (if finished) result for a task.
- Query parameters:
  - `task_id` — Celery task id to check the status of.
- Response (JSON) fields:
  - `state` (string)
  - `progress` (float)
  - `result` (float - or null if computation isn't finished yet)
- Implemented in: `src/webapp/pi_result_page.py` 

# ShapesAPI
A shape calculation application developed using FastAPI

## Overview:
This application is a backend API implemented in Python using FastAPI that allows users to calculate the area of geometric shapes asynchronously. It is designed to handle long-running computations efficiently by queuing tasks and providing immediate responses with a process_id that can be used to query the result later.

## Key Features:
**Endpoints:**

*POST /shapes:* -
Accepts a JSON request to calculate the area of a shape with its parameters.
Returns a unique process_id immediately without waiting for the computation to complete.

*GET /shape/{process_id}:* -
Retrieves the result of the computation for a given process_id.
If the result is not ready, it excludes the result field.

*GET /shapes:* -
Returns a list of all shape computations, including their input data and computed results (if available).



**Database Integration:**
Stores the requests (process_id and input data) and the results of computations in a database.



**Asynchronous Processing:**
Simulates a long-running task by introducing a random delay (1–10 seconds) before returning the result.


**Technology Stack:**
- FastAPI: For API development.

- SQLite: For database storage.

- Alembic: For database migrations

- Docker Compose: For containerized deployment.

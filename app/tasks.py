import asyncio
from app.db import SessionLocal, ShapeResult
from app.services import calculate_area
from celery import Celery

celery_app = Celery("tasks", broker="redis://localhost:6379/0")


@celery_app.task
def process_area(process_id: str, shape_data: dict):
    db = SessionLocal()

    try:
        result = asyncio.run(calculate_area(shape_data["type"], shape_data["areaValues"]))
        shape_result = ShapeResult(process_id=process_id, result=result)
        db.add(shape_result)
        db.commit()

    except Exception as e:
        print(f"Error processing area for {process_id}: {e}")

    finally:
        db.close()

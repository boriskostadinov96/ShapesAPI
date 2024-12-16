from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from app.models import ShapeRequestModel, ShapeResponseModel, AllShapesResponseModel
from app.db import SessionLocal, ShapeRequest, ShapeResult
from app.tasks import process_area

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the Shapes API!"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/shapes", response_model=ShapeResponseModel)
async def create_shape(request: ShapeRequestModel, db: Session = Depends(get_db)):
    process_id = str(uuid4())

    shape_request = ShapeRequest(
        process_id=process_id,
        shape_type=request.type,
        area_values=request.areaValues
    )
    db.add(shape_request)
    db.commit()

    process_area.delay(process_id, request.dict())

    return ShapeResponseModel(
        process_id=process_id,
        shapeRequest=request
    )


@app.get("/shape/{process_id}", response_model=ShapeResponseModel)
async def get_shape_result(process_id: str, db: Session = Depends(get_db)):
    shape_request = db.query(ShapeRequest).filter(ShapeRequest.process_id == process_id).first()

    if not shape_request:
        raise HTTPException(status_code=404, detail="Process ID not found")

    shape_result = db.query(ShapeResult).filter(ShapeResult.process_id == process_id).first()

    return ShapeResponseModel(
        process_id=process_id,
        shapeRequest=ShapeRequestModel(type=shape_request.shape_type, areaValues=shape_request.area_values),
        result=shape_result.result if shape_result else None
    )


@app.get("/shapes", response_model=AllShapesResponseModel)
async def get_all_shapes(db: Session = Depends(get_db)):
    shape_requests = db.query(ShapeRequest).all()
    computations = []

    for shape_request in shape_requests:
        shape_result = db.query(ShapeResult).filter(ShapeResult.process_id == shape_request.process_id).first()
        computations.append(
            ShapeResponseModel(
                process_id=shape_request.process_id,
                shapeRequest=ShapeRequestModel(type=shape_request.shape_type, areaValues=shape_request.area_values),
                result=shape_result.result if shape_result else None
            )
        )

    return AllShapesResponseModel(computations=computations)

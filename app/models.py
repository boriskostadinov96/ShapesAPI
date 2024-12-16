from pydantic import BaseModel, field_validator
from typing import Dict, Optional


class ShapeRequestModel(BaseModel):
    type: str
    areaValues: Dict[str, float]

    @field_validator("type")
    def validate_type(cls, value: str) -> str:
        if value not in {"circle", "rectangle", "trapezoid"}:
            raise ValueError("Invalid shape type. Must be 'circle', 'rectangle', or 'trapezoid'.")

        return value

    @field_validator("areaValues", mode="before")
    def validate_area_values(cls, values: Dict[str, float], info) -> Dict[str, float]:
        shape_type = info.data.get("type")
        if shape_type == "circle" and "radius" not in values:
            raise ValueError("Circle requires 'radius' in areaValues.")

        if shape_type == "rectangle" and not {"width", "height"}.issubset(values):
            raise ValueError("Rectangle requires 'width' and 'height' in areaValues.")

        if shape_type == "trapezoid" and not {"base1", "base2", "height"}.issubset(values):
            raise ValueError("Trapezoid requires 'base1', 'base2', and 'height' in areaValues.")

        return values


class ShapeResponseModel(BaseModel):
    process_id: str
    shapeRequest: ShapeRequestModel
    result: Optional[float] = None


class AllShapesResponseModel(BaseModel):
    computations: list[ShapeResponseModel]

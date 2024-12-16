import asyncio
import random


async def calculate_area(shape_type: str, area_values: dict) -> float:
    await asyncio.sleep(random.randint(1, 10))

    if shape_type == "circle":
        radius = area_values.get("radius")
        return 3.14159 * radius ** 2 if radius else 0

    elif shape_type == "rectangle":
        width = area_values.get("width")
        height = area_values.get("height")
        return width * height if width and height else 0

    elif shape_type == "trapezoid":
        base1 = area_values.get("base1")
        base2 = area_values.get("base2")
        height = area_values.get("height")
        return 0.5 * (base1 + base2) * height if base1 and base2 and height else 0

    return 0

import os
import pandas as pd

from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import FileResponse

from scripts.log import logger
from scripts.api.model_connector import ModelConnector


# Contains End_Points that are exposed externally

router = APIRouter()

model_connector_obj = ModelConnector()


@router.post("/get_expenses", tags=["split"])
def get_expenses(image: UploadFile = File(...)):
    result = {}
    result["expenses"] = []
    result["error"] = ""
    try:
        content = image.file.read()
        image_path = "temp_image.png"
    
        # Write the content of the image to a file
        with open(image_path, "wb") as img_file:
            img_file.write(content)

        result["expenses"] = model_connector_obj.expenses(image_path)
    except Exception as e:
        logger.error(str(e))
        result["error"] = str(e)
    return result

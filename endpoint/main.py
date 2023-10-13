import json
import uuid

from fastapi import FastAPI
from ffmodel.core.inference_endpoint import InferenceEndpoint
from ffmodel.core.environment_config import EnvironmentConfigs
from ffmodel.core.inference_endpoint import InferenceEndpoint
from ffmodel.data_models.inference import UserInferenceResponse
from ffmodel.utils.ffmodel_logger import FFModelLogger
from pydantic import BaseModel

class Prompt(BaseModel):
    user_nl: str

class Response(BaseModel):
    user_nl:str
    completion:str
    session_id:str
    sequence:str
    request_id:str

# Read Config
solution_config_path = EnvironmentConfigs.get_config("SOLUTION_CONFIG_PATH")
environment_config_path = EnvironmentConfigs.get_config("ENVIRONMENT_CONFIG_PATH")

# Initialize logger
logger = FFModelLogger().get_logger("app")

# Create Web App
app = FastAPI()
endpoint = InferenceEndpoint(solution_config_path, environment_config_path)

@app.get("/")
async def root():
    return {"message": "Pizza"}

@app.post("/inference/",response_model=Response)
def run_inference(prompt:Prompt) -> Response:
    request_id = uuid.uuid4()
    logger.info(f"Received request: {request_id}")
    result = endpoint.execute(str(prompt))
    logger.info(f"Inference completed: {request_id}")

    return Response(
        user_nl=result.request.user_nl,
        completion=result.model_output.completions[0],
        session_id=str(result.request.session_id),
        sequence=str(result.request.sequence),
        request_id=str(request_id),
    )


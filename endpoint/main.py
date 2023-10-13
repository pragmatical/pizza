import json
import uuid

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from ffmodel.core.inference_endpoint import InferenceEndpoint
from ffmodel.core.environment_config import EnvironmentConfigs
from ffmodel.core.inference_endpoint import InferenceEndpoint
from ffmodel.utils.ffmodel_logger import FFModelLogger
from pydantic import BaseModel

class Prompt(BaseModel):
    user_nl: str

class Response(BaseModel):
    user_nl:str
    completion:object
    request_id:str

# Read Config
solution_config_path = EnvironmentConfigs.get_config("SOLUTION_CONFIG_PATH")
environment_config_path = EnvironmentConfigs.get_config("ENVIRONMENT_CONFIG_PATH")

# Initialize logger
logger = FFModelLogger().get_logger("app")

def set_openapi_schema(app: FastAPI)->None:
    openapi_schema = get_openapi(
        title="PizzAI Order Generator",
        version="0.0.1",
        description="This inference endpoint will take natural language and produce a pizza order.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema


# Create Web App
app = FastAPI()

endpoint = InferenceEndpoint(solution_config_path, environment_config_path)

@app.get("/")
async def root():
    return {"message": "Pizza"}

@app.post("/inference/")
def run_inference(prompt:Prompt = {"user_nl":"I want a large pepperoni pie and a 2 liter of coke"}) -> Response:
    request_id = uuid.uuid4()
    logger.info(f"Received request: {request_id}")
    result = endpoint.execute(prompt.user_nl)
    logger.info(f"Inference completed: {request_id}")
    try:
        completion=json.loads(result.model_output.completions[0])
    except Exception as e:
        completion=result.model_output.completions[0]
        logger.info("Completion is not json for request id:"+str(request_id))
    
    return Response(
        user_nl=result.request.user_nl,
        completion=completion,
        request_id=str(request_id),
    )

set_openapi_schema(app)

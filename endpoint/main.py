import json
import uuid
import typing

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse
from ffmodel.core.inference_endpoint import InferenceEndpoint
from ffmodel.core.environment_config import EnvironmentConfigs
from ffmodel.core.inference_endpoint import InferenceEndpoint
from ffmodel.utils.ffmodel_logger import FFModelLogger
from ffmodel.data_models.inference import UserInferenceResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

class CompletionPair(BaseModel):
    user_nl:str
    completion:object

class UserSession(BaseModel):
    session_id:str
    prior_responses:list[CompletionPair]
    sequence: typing.Optional[int]


class ChatRequest(BaseModel):
    user_nl:str
    session:UserSession
    

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

@app.get("/",include_in_schema=False)
async def root():
    return RedirectResponse(url='/docs')

@app.post("/inference/")
def run_inference(chat_request:ChatRequest) -> object:
    request_id = uuid.uuid4()
    logger.info(f"Received request: {request_id}")
    payload=json.dumps(jsonable_encoder(chat_request))
    result = endpoint.execute(payload) 
    response = UserInferenceResponse(
        user_nl=result.request.user_nl,
        completion=result.model_output.completions[0],
        session_id=result.request.session_id,
        sequence=result.request.sequence,
        request_id=str(request_id),
    ) 
    return response

set_openapi_schema(app)

# pizza

This repo contains an FFModel based implementation of an endpoint that takes in a natural language prompt and returns a structured json object for an order at a pizza/wings/drinks restaurant.
There are 3 main directories:
- endpoint - contains a fastapi rest endpoint for the ffmodel inference endpoint
- notebooks - contains jupyter notebooks to work with endpoint locally both inference and experiment, a notebook that does analysis on experiment results, and also contains a notebook that immplements a chatbot
- solution - contains the ffmodel solution

## Running the notebooks
Notebooks run and use one of 2 .env files.  There is .ffmodel.env, and .chatbot.env

.ffmodel.env
```
OPENAI_API_KEY=<your key>
OPENAI_ENDPOINT=<your opeai base url>
```

.chatbot.env - we turn off logging so that the notebook has clean "chatbot" conversation
```
OPENAI_API_KEY=<your key>
OPENAI_ENDPOINT=<your opeai base url>
FFMODEL_METRICS_ENABLED='false'
FFMODEL_LOGGING_LEVEL='ERROR'
```

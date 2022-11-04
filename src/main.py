from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.constants import FRONTEND_HOST, HOST, PORT
from src.workflow_manager import WorkflowManager
import uvicorn

# app
app = FastAPI()


# sanity
@app.get("/")
def root():
    return {"message": "Hello World from backend service :-)"}


# get from db
@app.get("/get_all")
def get_all():
    # start workflow manager
    workflow_manager = WorkflowManager()

    # get links
    links = workflow_manager.get_links()

    return links


@app.get("/get_by_id/{id}")
def get_by_id(id: str):
    # start workflow manager
    workflow_manager = WorkflowManager()

    # get links
    links = workflow_manager.get_links_by_id(id)

    return links


if __name__ == "__main__":

    # start app
    uvicorn.run("src.main:app", host=HOST, port=PORT, reload=True)
    print("backend started.")

    # update db
    from src.db.db import db
    from src.db.redis import redis_client

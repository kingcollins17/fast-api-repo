#fast api imports
from fastapi import  FastAPI,Response
from .src import models,db,routes
from sqlalchemy.orm import Session

# fast api tutorial for python
models.Base.metadata.create_all(bind=db.engine)
app = FastAPI()
# app instance
@app.get('/')
def handler():
     return Response(content={"detail":"FASTAPI Tutorial project"}, status_code=200)


app.include_router(router=routes.router)


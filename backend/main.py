from fastapi import FastAPI, APIRouter
from api import user_routes, todo_routes
app = FastAPI()
from api.base_router import base_router

# Include API route 
app.include_router(base_router)
app.include_router(user_routes.router,prefix="/users")
app.include_router(todo_routes.router,prefix="/todos")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

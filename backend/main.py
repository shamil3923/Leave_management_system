from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import auth_router
from routes.leave import leave_router
from models.user_table import create_users_table  # Import the function
from models.leave_table import create_leave_requests_table  # Import the function

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    create_users_table()
    create_leave_requests_table()
    
# Include the auth_router for the routes
app.include_router(auth_router)
app.include_router(leave_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # Import StaticFiles to serve images

from auth import router as auth_router
from projects import router as projects_router
from auth import get_current_user
from contact_me import router as contact_router

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for your frontend in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all the routes
app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(contact_router)

# Serve static files (images) from the 'uploads' directory
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Serve static files (images) from the 'Website/assets' directory
app.mount("/assets", StaticFiles(directory="../Website/assets"), name="assets")

# Protect Dashboard route
@app.get("/dashboard")
def dashboard(current_user: str = Depends(get_current_user)):
    # If the user is authenticated, show the dashboard
    return {"message": f"Welcome to the dashboard, {current_user}"}

# Redirect to home page if not logged in
@app.get("/dashboard")
def dashboard_redirect(current_user: str = Depends(get_current_user)):
    raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, detail="Redirecting to home page")

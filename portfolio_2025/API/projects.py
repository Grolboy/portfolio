from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from typing import List, Optional
import os
import shutil
import uuid  # Import UUID for unique filenames
from database import get_db_connection
from auth import get_current_user

router = APIRouter()

UPLOAD_FOLDER = "uploads"  # Temporary storage location
PROJECT_IMAGES_FOLDER = "../Website/assets/project_images"  # Path where images will be saved for frontend
UPLOAD_DIRECTORY = "project_images"  # Directory where images are stored
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the uploads folder exists

def save_image(project_id: int, image: UploadFile) -> str:
    """
    Save an uploaded image to the Website/assets/project_images folder and return its relative path.
    """
    # Define the base directory for project images in the Website folder
    base_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Website", "assets", "project_images")

    # Create a subdirectory for the project ID
    project_directory = os.path.join(base_directory, str(project_id))
    os.makedirs(project_directory, exist_ok=True)  # Ensure the directory exists

    # Generate a unique filename
    unique_filename = f"{uuid.uuid4().hex}_{image.filename}"
    file_path = os.path.join(project_directory, unique_filename)

    # Save the file to the project directory
    try:
        with open(file_path, "wb") as f:
            f.write(image.file.read())
    except Exception as e:
        print(f"Error saving image: {e}")
        raise HTTPException(status_code=500, detail="Failed to save image")

    # Return the relative path to be stored in the database
    relative_path = os.path.join("assets", "project_images", str(project_id), unique_filename)
    return relative_path

# CREATE PROJECT (Requires Login)
@router.post("/projects", dependencies=[Depends(get_current_user)])
async def create_project(
    title: str = Form(...),
    description: str = Form(...),
    link: Optional[str] = Form(None),
    images: Optional[List[UploadFile]] = File(None)
):
    slug = title.lower().replace(" ", "-")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert project into the projects table
        cursor.execute(
            "INSERT INTO projects (title, slug, description) VALUES (%s, %s, %s)",
            (title, slug, description)
        )
        project_id = cursor.lastrowid

        # Insert the link into the project_links table (if provided)
        if link:
            cursor.execute(
                "INSERT INTO project_links (project_id, name, url) VALUES (%s, %s, %s)",
                (project_id, "Main Link", link)
            )

        # Handle image uploads
        image_urls = []
        if images:
            for image in images:
                try:
                    # Save the image and get its relative path
                    image_path = save_image(project_id, image)
                    image_urls.append(image_path)
                    cursor.execute(
                        "INSERT INTO project_images (project_id, image_path) VALUES (%s, %s)",
                        (project_id, image_path)
                    )
                except Exception as e:
                    print(f"Error saving image {image.filename}: {e}")
                    raise HTTPException(status_code=500, detail=f"Failed to save image {image.filename}")

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving project: {str(e)}")
    finally:
        cursor.close()
        conn.close()

    return {"message": "Project created successfully", "project_id": project_id, "images": image_urls}

# GET ALL PROJECTS (Public)
@router.get("/projects")
def get_projects():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
    projects = cursor.fetchall()

    for project in projects:
        cursor.execute("SELECT image_path FROM project_images WHERE project_id = %s", (project["id"],))
        project["images"] = [img["image_path"] for img in cursor.fetchall()]

    cursor.close()
    conn.close()

    return projects

# GET A SINGLE PROJECT (Public)
@router.get("/projects/{slug}")
def get_project(slug: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM projects WHERE slug = %s", (slug,))
    project = cursor.fetchone()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    cursor.execute("SELECT image_path FROM project_images WHERE project_id = %s", (project["id"],))
    project["images"] = [img["image_path"] for img in cursor.fetchall()]

    cursor.close()
    conn.close()

    return project

# UPDATE PROJECT (Requires Login)
@router.put("/projects/{project_id}", dependencies=[Depends(get_current_user)])
def update_project(project_id: int, title: str = Form(...), description: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE projects SET title = %s, description = %s WHERE id = %s", (title, description, project_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating project: {str(e)}")
    finally:
        cursor.close()
        conn.close()

    return {"message": "Project updated successfully"}

# DELETE PROJECT (Requires Login)
@router.delete("/projects/{project_id}", dependencies=[Depends(get_current_user)])
def delete_project(project_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Delete images linked to the project
        cursor.execute("SELECT image_url FROM project_images WHERE project_id = %s", (project_id,))
        images = cursor.fetchall()

        for image in images:
            image_path = image["image_url"]
            if os.path.exists(image_path):
                os.remove(image_path)  # Remove file from storage

        cursor.execute("DELETE FROM project_images WHERE project_id = %s", (project_id,))
        cursor.execute("DELETE FROM projects WHERE id = %s", (project_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting project: {str(e)}")
    finally:
        cursor.close()
        conn.close()

    return {"message": "Project deleted successfully"}

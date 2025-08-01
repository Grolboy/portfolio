from fastapi import APIRouter, Depends, HTTPException, Security, Form
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from database import get_db_connection
import random
import smtplib
from email.mime.text import MIMEText
from email_config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT  # Import email credentials
import string
import json

# Load the configuration file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# JWT Config
SECRET_KEY = "Temp_test"  # Change this to an environment variable in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token expiration time in minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

# Temporary storage for registration codes (use a database in production)
REGISTRATION_CODES = {}

# Load the admin password from the configuration file
ADMIN_PASSWORD = config.get("admin_password", "default_password")

# Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str

# Password hashing
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# JWT Token generation
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Request a registration code
@router.post("/request-registration-code")
def request_registration_code(password: str = Form(...)):
    # Validate the password
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Invalid password")

    # Generate a random alphanumeric registration code (6 characters)
    registration_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    # Save the code with an expiration time (e.g., 10 minutes)
    expiration_time = datetime.utcnow() + timedelta(minutes=10)
    REGISTRATION_CODES[registration_code] = expiration_time

    # Send the code to your email
    sender_email = EMAIL_ADDRESS
    recipient_email = EMAIL_ADDRESS
    subject = "Your Registration Code"
    body = f"Your registration code is: {registration_code}\n\nThis code will expire in 10 minutes."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(sender_email, recipient_email, msg.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")

    return {"message": "Registration code sent to your email"}

# Register new user (requires a registration code)
@router.post("/register")
def create_user(
    username: str = Form(...),
    password: str = Form(...),
    registration_code: str = Form(...)
):
    # Verify the registration code
    if registration_code not in REGISTRATION_CODES:
        raise HTTPException(status_code=403, detail="Invalid registration code")

    # Check if the code has expired
    if datetime.utcnow() > REGISTRATION_CODES[registration_code]:
        del REGISTRATION_CODES[registration_code]  # Remove expired code
        raise HTTPException(status_code=403, detail="Registration code has expired")

    # Remove the code after successful validation
    del REGISTRATION_CODES[registration_code]

    # Proceed with user registration
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if username already exists
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Username already taken")

    # Hash the password before storing it
    hashed_password = hash_password(password)

    # Insert into database
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "User registered successfully"}

# Login route
@router.post("/login", response_model=Token)
def login(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username = %s", (user.username,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if not result or not verify_password(user.password, result["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    return {"access_token": access_token, "token_type": "bearer"}

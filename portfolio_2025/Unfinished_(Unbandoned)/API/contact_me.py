from fastapi import APIRouter, Form, HTTPException
from email.mime.text import MIMEText
import smtplib
from email_config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT, CUSTOM_FROM_ADDRESS

router = APIRouter()

@router.post("/contact")
def send_contact_email(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    message: str = Form(...)
):
    subject_to_self = f"New Contact Form Submission from {name}"
    body_to_self = f"""
    Name: {name}
    Email: {email}
    Phone: {phone}
    Message: {message}
    """

    subject_to_user = "Thank you for contacting us!"
    body_to_user = f"""
    Hi {name},

    Thank you for reaching out! We have received your message and will get back to you as soon as possible.

    Here is a copy of your message:
    ------------------------------
    {message}
    ------------------------------

    Best regards,
    Lucas Ingmar Veenstra
    """

    try:
        # Create email to yourself
        msg_to_self = MIMEText(body_to_self)
        msg_to_self["Subject"] = subject_to_self
        msg_to_self["From"] = CUSTOM_FROM_ADDRESS  # Show domain-based email
        msg_to_self["To"] = EMAIL_ADDRESS

        # Create confirmation email to the user
        msg_to_user = MIMEText(body_to_user)
        msg_to_user["Subject"] = subject_to_user
        msg_to_user["From"] = CUSTOM_FROM_ADDRESS
        msg_to_user["To"] = email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(CUSTOM_FROM_ADDRESS, EMAIL_ADDRESS, msg_to_self.as_string())
            server.sendmail(CUSTOM_FROM_ADDRESS, email, msg_to_user.as_string())

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")

    return {"message": "Your message has been sent successfully. A confirmation email has been sent to your email address."}

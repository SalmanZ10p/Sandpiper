import requests
import json
from typing import List, Dict, Any, Optional
from common.app_config import config
from common.app_logger import logger


class MailjetService:
    """
    Service for sending emails directly via Mailjet API.
    This bypasses the RabbitMQ queue for more reliable email delivery.
    """
    API_VERSION = "v3.1"
    BASE_URL = f"https://api.mailjet.com/{API_VERSION}"
    
    def __init__(self):
        self.api_key = config.MAILJET_API_KEY
        self.api_secret = config.MAILJET_API_SECRET
        self.source_email = "sample_project@ecortest.com"
        self.source_name = "Sandpiper"
        
        # Template IDs from config
        self.welcome_template_id = 6410451  # Verify Email template
        self.reset_password_template_id = 6410454  # Reset Password template
        
    def _send_email(self, to_email: str, template_id: int, variables: Dict[str, Any], 
                   subject: str, recipient_name: Optional[str] = None) -> bool:
        """
        Send an email using Mailjet API.
        
        Args:
            to_email: Recipient email address
            template_id: Mailjet template ID
            variables: Template variables
            subject: Email subject
            recipient_name: Optional recipient name
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        url = f"{self.BASE_URL}/send"
        
        # Prepare recipient data
        recipient = {
            "Email": to_email
        }
        if recipient_name:
            recipient["Name"] = recipient_name
            
                    # Prepare payload
        payload = {
            "Messages": [
                {
                    "From": {
                        "Email": self.source_email,
                        "Name": self.source_name
                    },
                    "To": [recipient],
                    "TemplateID": template_id,
                    "TemplateLanguage": True,
                    "Subject": subject,
                    "Variables": variables
                }
            ]
        }
        
        # Log the email request (without sensitive data)
        logger.info(f"Sending email to {to_email} using template {template_id}")
        
        logger.info(f"Payload: {payload}")
        try:
            response = requests.post(
                url,
                auth=(self.api_key, self.api_secret),
                json=payload
            )
            
            if response.status_code == 200:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email. Status code: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return False
                
        except Exception as e:
            logger.exception(f"Exception while sending email: {str(e)}")
            return False
    
    def send_welcome_email(self, to_email: str, confirmation_link: str, recipient_name: str) -> bool:
        """
        Send welcome email with verification link.
        
        Args:
            to_email: Recipient email address
            confirmation_link: Link for email verification
            recipient_name: Recipient's name
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        variables = {
            "confirmation_link": confirmation_link  # Template 6410451 uses confirmation_link variable
        }
        
        return self._send_email(
            to_email=to_email,
            template_id=self.welcome_template_id,
            variables=variables,
            subject="Welcome to Sandpiper",
            recipient_name=recipient_name
        )
    
    def send_password_reset_email(self, to_email: str, reset_password_link: str) -> bool:
        """
        Send password reset email.
        
        Args:
            to_email: Recipient email address
            reset_password_link: Link for password reset
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        variables = {
            "reset_password_link": reset_password_link  # Template 6410454 uses reset_password_link variable
        }
        
        return self._send_email(
            to_email=to_email,
            template_id=self.reset_password_template_id,
            variables=variables,
            subject="Reset your password"
        )

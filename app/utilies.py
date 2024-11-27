from django.core.mail import EmailMessage  # Import EmailMessage class from Django for sending emails
import os  # Import the os module to interact with environment variables

# Define a utility class with static method for sending emails
class Util:
    # Static method that sends an email using the provided data
    @staticmethod
    def send_email(data):
        """
        Sends an email based on the provided data.
        
        Args:
            data (dict): A dictionary containing email details such as:
                - 'subject': Subject of the email.
                - 'body': Body content of the email.
                - 'to_email': Recipient's email address.
                
        The email is sent using Django's EmailMessage class.
        """
        
        # Create an instance of EmailMessage with provided email details
        email = EmailMessage(
            subject=data['subject'],  # Set the subject of the email
            body=data['body'],  # Set the body/content of the email
            from_email=os.environ.get('EMAIL_FROM'),  # Get the sender email from environment variables
            to=[data['to_email']]  # Set the recipient's email address (passed in data)
        )
        
        # Send the email
        email.send()  # Calls the send() method to send the email


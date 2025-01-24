from twilio.rest import Client
from django.conf import settings
from django.core.mail import send_mail
from decouple import config
import logging

# Configure logger
logger = logging.getLogger(__name__)



def send_sms(phone_number, message):
    client = Client(config('TWILIO_ACCOUNT_SID'), config('TWILIO_AUTH_TOKEN'))
    client.messages.create(body=message,from_=config('TWILIO_PHONE_NUMBER'),to=phone_number)



CARRIER_EMAIL_GATEWAYS = {
    "airtel":"sms@{number}@ke.airtel.com",
    "telcom": "sms@{number}@sms.telkom.co.ke",
    "safaricom" :"{number}@sms.safaricom.co.ke",
    "at&t": "{number}@txt.att.net",
                
}

def get_carrier_from_number(phone_number):
    # Identify carrier by prefix
    safaricom_prefixes = ('070', '071', '072', '074', '079')
    airtel_prefixes = ('073', '075')
    telkom_prefixes = ('076', '077')
    att_prefixes = ('234', '235', '236', '237')

    cleaned_number = phone_number.replace('+', '').replace('-', '').replace(' ', '')


    if cleaned_number.startswith('1'):  # US country code
        prefix = cleaned_number[1:4]  # Get area code
        if prefix in att_prefixes:
            return "at&t"
    
  # Check local carriers
    prefix = phone_number[:3]
    if prefix in safaricom_prefixes:
        return "safaricom"
    elif prefix in airtel_prefixes:
        return "airtel"
    elif prefix in telkom_prefixes:
        return "telkom"
    return None  # Unknown carrier

def send_sms_via_email(phone_number, message):
    carrier = get_carrier_from_number(phone_number)
    if not carrier:
        raise ValueError(f"Could not determine carrier for phone number: {phone_number}")

    email_gateway = CARRIER_EMAIL_GATEWAYS.get(carrier)
    if not email_gateway:
        raise ValueError(f"Carrier {carrier} does not have an email-to-SMS gateway configured.")

    # Format the recipient email address
    cleaned_number = phone_number[-9:] if len(phone_number) > 9 else phone_number
    recipient_email = email_gateway.format(number=cleaned_number)
    try:
        send_mail(
        subject='',  # Subject not required for SMS
        message=message,
        from_email='mboaacademy@gmail.com',
        recipient_list=[recipient_email],
        fail_silently=False
    )
       
        logger.info(f"SMS sent successfully to {phone_number}")  # Log success
        return True
    except Exception as e:
        logger.error(f"Failed to send SMS to {phone_number}: {e}")  # Log failure
        return False  
        
    
        
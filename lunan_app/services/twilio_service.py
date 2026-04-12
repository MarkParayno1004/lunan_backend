from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
from django.conf import settings


class TwilioService:
    @staticmethod
    def generate_chat_access_token(identity, user_role):
        """Generates an access token for Twilio Conversations."""
        # Ensure your settings.py has these keys:
        # TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, TWILIO_CHAT_SERVICE_SID
        
        token = AccessToken(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_API_KEY,
            settings.TWILIO_API_SECRET,
            identity=identity
        )

        chat_grant = ChatGrant(service_sid=settings.TWILIO_CHAT_SERVICE_SID)
        token.add_grant(chat_grant)

        return {
            "token": token.to_jwt(),
            "identity": identity,
            "role": user_role
        }

    @staticmethod
    def create_conversation(unique_name, friendly_name):
        """Creates a new Twilio conversation."""
        # In a real app, you'd use the Twilio Client here.
        # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # conversation = client.conversations.v1.conversations.create(
        #     friendly_name=friendly_name, 
        #     unique_name=unique_name
        # )
        # return conversation.sid
        pass

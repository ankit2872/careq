import asyncio

async def send_notification(user_id: int, message: str):
    """
    Sends a notification message to a patient via web interface.
    For now, this logs the notification. In a real implementation,
    you could send email, SMS, or push notifications.
    """
    try:
        print(f"Notification sent to user {user_id}: {message}")
        # Here you could implement email, SMS, or push notification logic
        # For example:
        # await send_email_notification(user_id, message)
        # await send_sms_notification(user_id, message)
    except Exception as e:
        print(f"Failed to send notification to user {user_id}: {e}")

async def notify_patient_next(user_id: int, lang_code: str = "en"):
    # Placeholder for i18n, actual messages will come from app.py
    message = "It's your turn next! Please proceed to the clinic." # This will be translated
    await send_notification(user_id, message)

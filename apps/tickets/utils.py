import uuid

def generate_ticket_reference() -> str:
    return uuid.uuid4().hex
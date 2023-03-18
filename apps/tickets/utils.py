import uuid

def generate_ticket_reference() -> str:
    return uuid.uuid4().hex

def get_data_from_qrcode(qrcode) -> str:
    return ""


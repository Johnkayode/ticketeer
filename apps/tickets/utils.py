import uuid
from PIL import Image
from pyzbar import pyzbar



def generate_ticket_reference() -> str:
    return uuid.uuid4().hex

def get_data_from_qrcode(qrcode) -> str:
    # use pyzbar to decode image
    qrcode = Image.open(qrcode)
    decoded = pyzbar.decode(qrcode)[0]
    return decoded.data.decode('ascii')


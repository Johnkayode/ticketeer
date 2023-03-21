import uuid
from PIL import Image
from pyzbar import pyzbar



def generate_ticket_reference() -> str:
    return uuid.uuid4().hex

def get_data_from_qrcode(qrcode) -> str:
    # use pyzbar to decode image
    qrcode = Image.open(qrcode)
    try:
        decoded = pyzbar.decode(qrcode)
        if not decoded:
            return None, "Qrcode could not be decoded."
        return decoded[0].data.decode('ascii'), "Qrcode decoded."
    except Exception as err:
        return None, err


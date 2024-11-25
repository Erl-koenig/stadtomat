from typing import List
from model import QRCodeData


def export_csv(data: List[QRCodeData], output):
    """
    Export the QR code data to a CSV file.
    """
    try:
        with open(output, "w") as f:
            f.write("data,type,left,top,width,height,quality,orientation\n")
            for qr_code in data:
                f.write(
                    f"{qr_code.data},{qr_code.type},{qr_code.rect.left},{qr_code.rect.top},{qr_code.rect.width},{qr_code.rect.height},{qr_code.quality},{qr_code.orientation}\n"
                )
    except Exception as e:
        print(f"Error: {e}")
        return False
    return True

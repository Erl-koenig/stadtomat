from pyzbar.pyzbar import decode
import cv2
from pathlib import Path
import shutil


def get_x_y_of_qr(image_path: str):
    image = cv2.imread(image_path)
    codes = decode(image)
    print(f"QR Codes detected: {len(codes)}")
    code_dict = {}
    print(f"coordinates image: (0, 0) {image.shape[:-1]}")
    count = 0
    for code in codes:
        (x, y, w, h) = code.rect
        codeData = code.data.decode("utf-8")
        print(code)
        codeType = code.type
        code_dict[str(codeData) + f"{count}"] = [(x, y), (x + w, y + h)]
        count += 1

    return code_dict


def scan_img_folder():
    """
    Scan the img folder for images and get the QR code coordinates
    """
    folder_path = "img/"
    p = Path(folder_path)
    for file in p.iterdir():
        if file.is_file() and file.suffix == ".jpg":
            print(file)
            coordinates = get_x_y_of_qr(file)
            print(coordinates)
            move_file(file)


def move_file(original: Path):
    """
    Move the original file to a backup folder
    """
    dest_dir = Path("img/backup/")
    dest_file = Path(dest_dir, original.name)
    print(f"original: {original.as_posix()}")
    print(f"destination: {dest_dir.as_posix()}")
    if not dest_dir.exists():
        dest_dir.mkdir()
    shutil.move(original.as_posix(), dest_file.as_posix())

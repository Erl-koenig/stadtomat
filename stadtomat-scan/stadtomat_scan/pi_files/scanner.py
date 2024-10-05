from typing import List
from pyzbar.pyzbar import decode
import cv2
import argparse
import json
import sys
import logging
from dataclasses import dataclass, asdict

log = logging.getLogger(__name__)


@dataclass
class Rect:
    """
    A rectangle defined by its top-left corner and its width and height.
    
    Attributes:
        left: int  -> x coordinate of the top-left corner
        top: int  -> y coordinate of the top-left corner
        width: int -> width of the rectangle
        height: int -> height of the rectangle
    """
    left: int
    top: int
    width: int
    height: int

    def to_dict(self):
        return asdict(self)


@dataclass
class Point:
    x: int
    y: int

    def to_dict(self):
        return asdict(self)


@dataclass
class QRCodeData:
    data: str
    type: str
    rect: Rect
    polygon: List[Point]
    quality: int
    orientation: str

    def to_dict(self):
        return {
            "data": self.data,
            "type": self.type,
            "rect": self.rect.to_dict(),
            "polygon": [point.to_dict() for point in self.polygon],
            "quality": self.quality,
            "orientation": self.orientation,
        }


def get_x_y_of_qr(image_path: str):
    image = cv2.imread(image_path)
    codes = decode(image)
    print(f"QR Codes detected: {len(codes)}")
    code_dict = {}
    print(f"coordinates image: (0, 0) {image.shape[:-1]}")
    count = 0
    for code in codes:
        data = QRCodeData(
            data=code.data.decode("utf-8"),
            type=str(code.type),
            rect=Rect(code.rect[0], code.rect[1], code.rect[2], code.rect[3]),
            polygon=[Point(x, y) for x, y in code.polygon],
            quality=int(code.quality),
            orientation=str(code.orientation),
        )
        (x, y, w, h) = code.rect

        print(json.dumps(data.to_dict()))
        # print("[INFO] Found {} with code: {}".format(codeType, codeData))
        code_dict[str(data.data) + f"-{count}"] = data
        count += 1

    return code_dict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        help="path to the input folder containing all the image to be processed",
        required=True,
    )
    # parser.add_argument("--output", help="path to the output folder containing all output in the json format", required = True)
    args = parser.parse_args()

    print("x, y detection")
    coordinates = get_x_y_of_qr(args.input)
    print(json.dumps(coordinates))
    sys.stdout.flush()


if __name__ == "__main__":
    main()

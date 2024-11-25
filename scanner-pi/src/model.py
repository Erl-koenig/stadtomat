from dataclasses import asdict, dataclass
from typing import List


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

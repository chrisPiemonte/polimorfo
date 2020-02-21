
from typing import Tuple

class BoundingBox():
    """Bounding boxes representation.
        THe point (0,0) is in the top-left corner
        type of BBs:
        - PASCAL: (xMin, yMin, xMax, yMax) (Pascal-VOC format) (default)
        - COCO: (x top-left, y top-left, width, height) (COCO format) 
    """

    def __init__(self, x1: int, y1: int, x2: int, y2: int, label: str = None, 
                image_size: Tuple(int, int) = None, bb_format: str = 'PASCAL') -> None:
        """[summary]
        
        Arguments:
            x1 {int} -- [description]
            y1 {int} -- [description]
            x2 {int} -- [description]
            y2 {int} -- [description]
        
        Keyword Arguments:
            label {str} -- [description] (default: {None})
            image_size {Tuple} -- [description] (default: {None})
            bb_format {str} -- [description] (default: {'PASCAL'})
        """

        self.label = label
        self.image_size = image_size
        self.bb_format = bb_format
        if self.bb_format == 'COCO':
            self.xMin = x1
            self.yMin = y1
            self.xMax = x1 + x2
            self.yMax = y1 + y2

        elif self.bb_format == 'PASCAL':
            self.xMin = x1
            self.yMin = y1
            self.xMax = x2
            self.yMax = y2
        else:
            raise ValueError(f'{bb_format} is not a valid bounding box format.')

    @property
    def width(self) -> int:
        """[summary]
        
        Returns:
            [type] -- [description]
        """
        return self.xMax - self.xMin

    @property
    def height(self) -> int:
        """[summary]
        
        Returns:
            [type] -- [description]
        """
        return self.yMax - self.yMin

    
    @property
    def center_x(self) -> int:
        """Returns the  x-coord of the bounding box center.
        
        Returns:
            int -- x-coord of the bounding box center.
        """
        return (self.width / 2) + self.xMin


    @property
    def center_y(self) -> int:
        """Returns the y-coord of the bounding box center.
        
        Returns:
            int -- y-coord of the bounding box center.
        """
        return (self.height / 2) + self.yMin
    

    @property
    def area(self) -> int:
        """Computes the area of the bounding box
        
        Returns:
            int -- Area of the bounding box.
        """
        return self.width * self.height


    def intersection(self, other: BoundingBox) -> BoundingBox:
        """[summary]
        
        Arguments:
            other {BoundingBox} -- [description]
        
        Returns:
            BoundingBox -- [description]
        """
        new_xMin = max(self.xMin, other.xMin)
        new_yMin = max(self.yMin, other.yMin)
        new_xMax = min(self.xMax, other.xMax)
        new_yMax = min(self.yMax, other.yMax)
        if new_xMin > new_xMax or new_yMin > new_yMax:
            return None
        return BoundingBox(new_xMin, new_yMin, new_xMax, new_yMax)


    def intersection_area(self, other: BoundingBox) -> int:
        """[summary]
        
        Arguments:
            other {BoundingBox} -- [description]
        
        Returns:
            int -- Area of intersection between the two the bounding boxes.
        """
        intersection_bb = self.intersection(other)
        return intersection_bb.area if intersection_bb else None


    def union_area(self, other: BoundingBox) -> int:
        """[summary]
        
        Arguments:
            other {BoundingBox} -- [description]
        
        Returns:
            int -- [description]
        """
        intersection_bb = self.intersection(other)
        # TODO: check if logic is scorrect
        # return (self.area + other.area) - intersection_bb.area if intersection_bb else None
        return (self.area + other.area) - intersection_bb.area if intersection_bb else self.area + other.area


from  .baseparser import BaseParser
from .title import Title
from .image import Image
class ProductClass(BaseParser):
    def __init__(self, parserType, baseTagType, className, title: Title, image: Image, subTitle: Title):
        super().__init__(parserType=parserType, baseTagType=baseTagType)
        self.className = className
        self.title = title
        self.image = image
        self.subTitle = subTitle
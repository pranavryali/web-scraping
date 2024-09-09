from .baseitem import BaseItem

class Image(BaseItem):
    def __init__(self, tag = None, className = None):
        super().__init__(tag, className)
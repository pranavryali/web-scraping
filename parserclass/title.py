from .baseitem import BaseItem


class Title(BaseItem):
    def __init__(self, tag=None, className=None, subTag=None):
        super().__init__(tag=tag, className=className, subTag=subTag)

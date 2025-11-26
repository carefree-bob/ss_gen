



class HTMLNode:
    def __init__(self, tag:str|None=None, value: str|None=None, children:list[HTMLNode]|None=None, props:dict[str,str] | None=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("not implemented")

    def props_to_html(self):
        """
            support href, target, alt, 

        """
        if self.props:
            attr_list = [f'{x}="{y}"' for x,y in self.props.items()]
            return " ".join(attr_list).strip()
        else:
            return ""

    def __repr__(self):
        return f"(HTMLNODE)(tag: {self.tag}\n\tvalue: {self.value}\n\tchildren: {self.children}\n\tprops: {self.props}\n)"


class LeafNode(HTMLNode):
    def __init__(self, tag:str|None=None, value: str|None=None, children:list[HTMLNode]|None=None, props:dict[str,str] | None=None):
        if children:
            raise ValueError("No kids allowed in Leafland!!")
        if not value:
            raise ValueError("We have values at Leafland!!")
        super().__init__(tag, value, children, props)
    
    def to_html(self):
        if not self.tag:
            return self.value
        if not self.props:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        else:
            return f'<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>'





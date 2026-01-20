class HTMLNode:
    """docstring for HTMLNode."""

    def __init__(self, tag=None, value=None, children=None, props=None):
        super(HTMLNode, self).__init__()
        self.tag, self.value, self.children, self.props = tag, value, children, props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        str = ""
        if self.props is not None:
            for k, v in self.props.items():
                str += f' {k}="{v}"'
        return str

    def __repr__(self):
        return "HTMLNode({tag}, {value}, {children}, {props})".format(
            tag=self.tag, value=self.value, children=self.children, props=self.props
        )


class LeafNode(HTMLNode):
    """docstring for LeafNode"""

    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    """docstring for ParentNode"""

    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, value=None, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag not provided")

        if self.children is None:
            raise ValueError("No children provided")

        html_str = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_str += child.to_html()

        html_str += f"</{self.tag}>"
        return html_str

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

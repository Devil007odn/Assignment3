from datetime import datetime

class Post:
    """
    Represents a blog post with code, title, text, and timestamps.
    """

    def __init__(self, code: int, title: str, text: str):
        self.code = code
        self.title = title
        self.text = text
        self.creation = datetime.now()
        self.update = self.creation

    def update_timestamp(self):
        self.update = datetime.now()

    def __repr__(self):
        return f"Post(code={self.code}, title='{self.title}')"

    def __eq__(self, other):
        if not isinstance(other, Post):
            return False
        return (self.code == other.code and
                self.title == other.title and
                self.text == other.text)

    def __str__(self):
        return f"Post(code={self.code}, title='{self.title}', text='{self.text[:20]}...')"
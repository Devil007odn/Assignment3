from datetime import datetime

class Post:
    """
    Represents a blog post with code, title, text, and timestamps.
    """

    def __init__(self, code: int, title: str, text: str):
        """ Initializes a new post with a unique code, title, and text """
        self.code = code
        self.title = title
        self.text = text
        """ Automatically sets creation and update timestamps to current time """
        self.creation = datetime.now()
        self.update = self.creation

    def __repr__(self):
        """ String representation of the post, useful for developers """
        return f"Post(code={self.code}, title='{self.title}')"

    def update_timestamp(self):
        """ Refresh the update timestamp to the current time 
            Called whenever the post is modified """
        self.update = datetime.now()

    def __eq__(self, other):
        """ Compare the content of a post with another post 
            Returns true if the code, title, and text are the same """
        if not isinstance(other, Post):
            return False
        return (self.code == other.code and
                self.title == other.title and
                self.text == other.text)

    def __str__(self):
        """ String representation of the post, useful for users
            Returns a concise 20-character summary of the post """
        return f"Post(code={self.code}, title='{self.title}', text='{self.text[:20]}...')"
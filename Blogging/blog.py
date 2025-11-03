from datetime import datetime

class Blog:
    """
    Represents a blog with id, name, url, email, and a list of posts.
    """

    def __init__(self, blog_id: int, name: str, url: str, email: str):
        self.id = blog_id
        self.name = name
        self.url = url
        self.email = email
        self.posts = []  # List of Post objects
        self.next_post_code = 1  # Auto-increment post code



    def __eq__(self, other):
        """Two blogs are equal if all attributes match."""
        if not isinstance(other, Blog):
            return False
        return (self.id == other.id and
                self.name == other.name and
                self.url == other.url and
                self.email == other.email)

    def __str__(self):
        return f"Blog(id={self.id}, name='{self.name}', url='{self.url}', email='{self.email}')"
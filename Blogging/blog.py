from datetime import datetime
from blogging.post import Post
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

    def __repr__(self):
        return f"Blog(id={self.id}, name='{self.name}')"    

    def create_post(self, title: str, text: str):
        """Creates and returns a new Post with auto-incremented code."""

        post = Post(self.next_post_code, title, text)
        self.posts.append(post)
        self.next_post_code += 1
        return post

    def search_post(self, code: int):
        """Returns the post with the given code or None."""
        for post in self.posts:
            if post.code == code:
                return post
        return None

    def retrieve_posts(self, keyword: str):
        """Returns a list of posts where keyword is in title or text."""
        return [p for p in self.posts if keyword in p.title or keyword in p.text]

    def update_post(self, code: int, new_title: str, new_text: str):
        """Updates the post with the given code."""
        post = self.search_post(code)
        if post:
            post.title = new_title
            post.text = new_text
            post.update_timestamp()
            return True
        return False

    def delete_post(self, code: int):
        """Deletes the post with the given code."""
        post = self.search_post(code)
        if post:
            self.posts.remove(post)
            return True
        return False

    def list_posts(self):
        """Returns a list of posts from newest to oldest."""
        return list(reversed(self.posts))

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
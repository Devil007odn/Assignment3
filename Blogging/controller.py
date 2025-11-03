from blogging.blog import Blog

class Controller:
    """
    Handles user stories for the blogging system.
    """

    def __init__(self):
        self.logged_in = False
        self.blogs = {}  # id -> Blog
        self.current_blog = None

    def login(self, username: str, password: str) -> bool:
        if self.logged_in:
            return False
        if username == "user" and password == "blogging2025":
            self.logged_in = True
            return True
        return False

    def logout(self) -> bool:
        if not self.logged_in:
            return False
        self.logged_in = False
        self.current_blog = None
        return True

    def create_blog(self, blog_id: int, name: str, url: str, email: str):
        if not self.logged_in or blog_id in self.blogs:
            return None
        blog = Blog(blog_id, name, url, email)
        self.blogs[blog_id] = blog
        return blog


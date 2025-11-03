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
    

    def search_blog(self, blog_id: int):
        return self.blogs.get(blog_id)

    def retrieve_blogs(self, keyword: str):
        if not self.logged_in:
            return None
        return [b for b in self.blogs.values() if keyword in b.name]

    def update_blog(self, old_id: int, new_id: int, name: str, url: str, email: str):
        if not self.logged_in or old_id not in self.blogs:
            return False
        if new_id != old_id and new_id in self.blogs:
            return False
        if self.current_blog and self.current_blog.id == old_id:
            return False
        blog = self.blogs.pop(old_id)
        blog.id = new_id
        blog.name = name
        blog.url = url
        blog.email = email
        self.blogs[new_id] = blog
        if self.current_blog == blog:
            self.current_blog = blog
        return True

    def delete_blog(self, blog_id: int):
        if not self.logged_in or blog_id not in self.blogs:
            return False
        blog = self.blogs[blog_id]
        if blog == self.current_blog:
            return False
        del self.blogs[blog_id]
        return True
    
    def list_blogs(self):
        if not self.logged_in:
            return None
        return list(self.blogs.values())

    def set_current_blog(self, blog_id: int):
        if not self.logged_in or blog_id not in self.blogs:
            return
        self.current_blog = self.blogs[blog_id]

    def get_current_blog(self):
        if not self.logged_in:
            return None
        return self.current_blog

    def unset_current_blog(self):
        self.current_blog = None

    def create_post(self, title: str, text: str):
        if not self.logged_in or not self.current_blog:
            return None
        return self.current_blog.create_post(title, text)

    def search_post(self, code: int):
        if not self.current_blog:
            return None
        return self.current_blog.search_post(code)
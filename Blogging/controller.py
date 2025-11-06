from blogging.blog import Blog

class Controller:
    """
    Handles user stories for the blogging system.
    """

    def __init__(self):
        """ Initializes the controller with the default state """
        self.logged_in = False
        self.blogs = {}  # id -> Blog
        self.current_blog = None

    def login(self, username: str, password: str) -> bool:
        """ Log in a user if valid credentials are provided
            Must enter username and password """
        if self.logged_in:
            return False
        if username == "user" and password == "blogging2025":
            self.logged_in = True
            return True
        return False

    def logout(self) -> bool:
        """ If user is not logged in the logout fails 
            else the current user is logged out"""
        if not self.logged_in:
            return False
        self.logged_in = False
        self.current_blog = None
        return True

    def create_blog(self, blog_id: int, name: str, url: str, email: str):
        """ Create a new blog and add it to the controllers blog section 
            If the user is logged in and the blog ID does not exist, a 
            new blog is created """
        if not self.logged_in or blog_id in self.blogs:
            return None
        blog = Blog(blog_id, name, url, email)
        self.blogs[blog_id] = blog
        return blog
    

    def search_blog(self, blog_id: int):
        """ Search for a blog by it's ID (Will be unique to the specific blog) 
            Returns none if blog ID is not found """
        return self.blogs.get(blog_id)

    def retrieve_blogs(self, keyword: str):
        """ Retrieve all blogs that have the given keyword
            (searched name) in the blogs name.
            Checks to make sure user is logged in """
        if not self.logged_in:
            return None
        return [b for b in self.blogs.values() if keyword in b.name]

    def update_blog(self, old_id: int, new_id: int, name: str, url: str, email: str):
        """ Update the properties of an existing blog
            Returns true if update was successful and false if it wasn't """
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
        """ Delete a blog from the system if the blog exists and the user is logged in.
            If the blog is the current_blog, blog is not deleted """
        if not self.logged_in or blog_id not in self.blogs:
            return False
        blog = self.blogs[blog_id]
        if blog == self.current_blog:
            return False
        del self.blogs[blog_id]
        return True
    
    def list_blogs(self):
        """ Return all blogs currently stored in controller 
            Checks to see if the user is currently logged in """
        if not self.logged_in:
            return None
        return list(self.blogs.values())

    def set_current_blog(self, blog_id: int):
        """ Select a blog as the current working blog with the blog ID
            Checks to see if the user is currently logged in """
        if not self.logged_in or blog_id not in self.blogs:
            return
        self.current_blog = self.blogs[blog_id]

    def get_current_blog(self):
        """ Returns the currently selected blog
            Returns none if not logged in or no blog is selected """
        if not self.logged_in:
            return None
        return self.current_blog

    def unset_current_blog(self):
        """ Sets the currently selected blog to none """
        self.current_blog = None

    def create_post(self, title: str, text: str):
        """ Create a new post inside the current blog
            Checks to make sure the user is logged in and the
            user has a blog selected """
        if not self.logged_in or not self.current_blog:
            return None
        return self.current_blog.create_post(title, text)

    def search_post(self, code: int):
        """ Search for a post using its code inside current blog
            Checks to make sure we are in the current_blog """
        if not self.current_blog:
            return None
        return self.current_blog.search_post(code)
    
    def retrieve_posts(self, keyword: str):
        """ Retrieve all posts in the current blog containing the
            given keyword (string) in the title or text of the post """
        if not self.current_blog:
            return None
        return self.current_blog.retrieve_posts(keyword)
    
    def update_post(self, code: int, title: str, text: str):
        """ Update a post in the current blog 
            Checks to make sure user is logged in and user is in
            the current_blog """
        if not self.logged_in or not self.current_blog:
            return False
        return self.current_blog.update_post(code, title, text)

    def delete_post(self, code: int):
        """ Delete a post using its code from the current blog
            Checks to make sure user is logged in and inside of
            current_blog """
        if not self.logged_in or not self.current_blog:
            return False
        return self.current_blog.delete_post(code)
    
    def list_posts(self):
        """ Return all posts in the current blog
            posts are returned in newest to oldest order
            Checks if user is in the current_blog """
        if not self.current_blog:
            return None
        return self.current_blog.list_posts()
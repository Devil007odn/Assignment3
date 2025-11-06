import unittest
from blogging.blog import Blog
from blogging.post import Post

class BlogTest(unittest.TestCase):

    def setUp(self):
        self.blog = Blog(1, "Travel", "travel.com", "travel@mail.com")

    def test_create_post(self):
        post = self.blog.create_post("Title", "Text")
        self.assertEqual(post.title, "Title")
        self.assertEqual(post.text, "Text")
        self.assertEqual(post.code, 1)

    def test_search_post(self):
        self.blog.create_post("Title", "Text")
        post = self.blog.search_post(1)
        self.assertIsNotNone(post)
        self.assertEqual(post.title, "Title")

    def test_update_post(self):
        self.blog.create_post("Title", "Text")
        success = self.blog.update_post(1, "New Title", "New Text")
        self.assertTrue(success)
        post = self.blog.search_post(1)
        self.assertEqual(post.title, "New Title")
        self.assertEqual(post.text, "New Text")

    def test_delete_post(self):
        self.blog.create_post("Title", "Text")
        success = self.blog.delete_post(1)
        self.assertTrue(success)
        self.assertIsNone(self.blog.search_post(1))

    def test_list_posts(self):
        self.blog.create_post("A", "Text A")
        self.blog.create_post("B", "Text B")
        posts = self.blog.list_posts()
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0].title, "B")  # reversed order
        self.assertEqual(posts[1].title, "A")

    def test_blog_equality(self):
        blog1 = Blog(1, "Travel", "travel.com", "travel@mail.com")
        blog2 = Blog(1, "Travel", "travel.com", "travel@mail.com")
        blog3 = Blog(2, "Food", "food.com", "food@mail.com")
        self.assertEqual(blog1, blog2)
        self.assertNotEqual(blog1, blog3)

    def test_blog_str(self):
        blog = Blog(1, "Travel", "travel.com", "travel@mail.com")
        self.assertIn("Blog(id=1, name='Travel'", str(blog))

if __name__ == '__main__':
    unittest.main()
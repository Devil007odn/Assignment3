import unittest
from blogging.post import Post

class PostTest(unittest.TestCase):

    def test_post_creation(self):
        post = Post(1, "Title", "Text")
        self.assertEqual(post.code, 1)
        self.assertEqual(post.title, "Title")
        self.assertEqual(post.text, "Text")
        self.assertIsNotNone(post.creation)
        self.assertEqual(post.creation, post.update)

    def test_post_update_timestamp(self):
        post = Post(1, "Title", "Text")
        old_update = post.update
        post.update_timestamp()
        self.assertNotEqual(old_update, post.update)

    def test_post_equality(self):
        post1 = Post(1, "Title", "Text")
        post2 = Post(1, "Title", "Text")
        post3 = Post(2, "Title", "Text")
        self.assertEqual(post1, post2)
        self.assertNotEqual(post1, post3)

if __name__ == '__main__':
    unittest.main()
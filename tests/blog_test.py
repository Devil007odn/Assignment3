import unittest
from blogging.blog import Blog
from blogging.post import Post

class BlogTest(unittest.TestCase):
    """
    Test cases for the Blog class functionality.
    Covers post creation, searching, updating, deletion, listing, and blog operations.
    """

    def setUp(self):
        """Set up a fresh Blog instance before each test."""
        self.blog = Blog(1, "Travel", "travel.com", "travel@mail.com")

    def test_create_post(self):
        """Test creating a post with auto-incremented code."""
        post = self.blog.create_post("Title", "Text")
        self.assertEqual(post.title, "Title")
        self.assertEqual(post.text, "Text")
        self.assertEqual(post.code, 1)

    def test_create_multiple_posts(self):
        """Test creating multiple posts with sequential codes."""
        post1 = self.blog.create_post("First", "Text1")
        post2 = self.blog.create_post("Second", "Text2")
        post3 = self.blog.create_post("Third", "Text3")
        
        self.assertEqual(post1.code, 1)
        self.assertEqual(post2.code, 2)
        self.assertEqual(post3.code, 3)

    def test_search_post(self):
        """Test searching for an existing post by code."""
        self.blog.create_post("Title", "Text")
        post = self.blog.search_post(1)
        self.assertIsNotNone(post)
        self.assertEqual(post.title, "Title")

    def test_search_nonexistent_post(self):
        """Test searching for a post that doesn't exist."""
        post = self.blog.search_post(999)
        self.assertIsNone(post)

    def test_update_post(self):
        """Test updating an existing post's title and text."""
        self.blog.create_post("Title", "Text")
        success = self.blog.update_post(1, "New Title", "New Text")
        self.assertTrue(success)
        post = self.blog.search_post(1)
        self.assertEqual(post.title, "New Title")
        self.assertEqual(post.text, "New Text")

    def test_update_nonexistent_post(self):
        """Test updating a post that doesn't exist."""
        success = self.blog.update_post(999, "New Title", "New Text")
        self.assertFalse(success)

    def test_delete_post(self):
        """Test deleting an existing post."""
        self.blog.create_post("Title", "Text")
        success = self.blog.delete_post(1)
        self.assertTrue(success)
        self.assertIsNone(self.blog.search_post(1))

    def test_delete_nonexistent_post(self):
        """Test deleting a post that doesn't exist."""
        success = self.blog.delete_post(999)
        self.assertFalse(success)

    def test_list_posts(self):
        """Test listing posts in reverse chronological order."""
        self.blog.create_post("A", "Text A")
        self.blog.create_post("B", "Text B")
        posts = self.blog.list_posts()
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0].title, "B")  # newest first
        self.assertEqual(posts[1].title, "A")  # oldest last

    def test_list_empty_posts(self):
        """Test listing posts when no posts exist."""
        posts = self.blog.list_posts()
        self.assertEqual(len(posts), 0)

    def test_retrieve_posts_by_keyword_in_title(self):
        """Test retrieving posts by keyword found in title."""
        self.blog.create_post("Python Programming", "Some text")
        self.blog.create_post("Java Tutorial", "Other text")
        self.blog.create_post("Advanced Python", "More text")
        
        python_posts = self.blog.retrieve_posts("Python")
        self.assertEqual(len(python_posts), 2)
        self.assertEqual(python_posts[0].title, "Python Programming")
        self.assertEqual(python_posts[1].title, "Advanced Python")

    def test_retrieve_posts_by_keyword_in_text(self):
        """Test retrieving posts by keyword found in text content."""
        self.blog.create_post("First", "I love Python programming")
        self.blog.create_post("Second", "Java is also good")
        self.blog.create_post("Third", "Python is versatile")
        
        python_posts = self.blog.retrieve_posts("Python")
        self.assertEqual(len(python_posts), 2)

    def test_retrieve_posts_no_matches(self):
        """Test retrieving posts when no matches found."""
        self.blog.create_post("First", "Some content")
        self.blog.create_post("Second", "Other content")
        
        no_posts = self.blog.retrieve_posts("Nonexistent")
        self.assertEqual(len(no_posts), 0)

    def test_retrieve_posts_case_sensitive(self):
        """Test that post retrieval is case-sensitive."""
        self.blog.create_post("Python", "text")
        self.blog.create_post("python", "text")
        
        uppercase_posts = self.blog.retrieve_posts("Python")
        lowercase_posts = self.blog.retrieve_posts("python")
        
        self.assertEqual(len(uppercase_posts), 1)
        self.assertEqual(len(lowercase_posts), 1)

    def test_blog_equality(self):
        """Test blog equality based on all attributes."""
        blog1 = Blog(1, "Travel", "travel.com", "travel@mail.com")
        blog2 = Blog(1, "Travel", "travel.com", "travel@mail.com")
        blog3 = Blog(2, "Food", "food.com", "food@mail.com")
        self.assertEqual(blog1, blog2)
        self.assertNotEqual(blog1, blog3)

    def test_blog_equality_different_types(self):
        """Test blog equality with non-Blog objects."""
        blog = Blog(1, "Travel", "travel.com", "travel@mail.com")
        self.assertNotEqual(blog, "not a blog")
        self.assertNotEqual(blog, None)

    def test_blog_str_representation(self):
        """Test string representation of Blog."""
        blog = Blog(1, "Travel", "travel.com", "travel@mail.com")
        blog_str = str(blog)
        self.assertIn("Blog(id=1, name='Travel'", blog_str)
        self.assertIn("url='travel.com'", blog_str)
        self.assertIn("email='travel@mail.com'", blog_str)

    def test_blog_initial_state(self):
        """Test that blog is initialized with correct attributes and empty posts."""
        self.assertEqual(self.blog.id, 1)
        self.assertEqual(self.blog.name, "Travel")
        self.assertEqual(self.blog.url, "travel.com")
        self.assertEqual(self.blog.email, "travel@mail.com")
        self.assertEqual(len(self.blog.posts), 0)
        self.assertEqual(self.blog.next_post_code, 1)

    def test_post_auto_increment_after_deletion(self):
        """Test that post codes continue auto-incrementing after deletions."""
        post1 = self.blog.create_post("First", "Text")
        post2 = self.blog.create_post("Second", "Text")
        self.blog.delete_post(1)
        post3 = self.blog.create_post("Third", "Text")
        
        self.assertEqual(post2.code, 2)
        self.assertEqual(post3.code, 3)  # Should be 3, not reusing deleted code 1

    def test_multiple_operations_integration(self):
        """Integration test with multiple blog operations."""
        # Create posts
        post1 = self.blog.create_post("First Post", "Initial content")
        post2 = self.blog.create_post("Second Post", "More content")
        
        # Verify creation
        self.assertEqual(len(self.blog.list_posts()), 2)
        
        # Update a post
        self.blog.update_post(1, "Updated First", "Updated content")
        updated_post = self.blog.search_post(1)
        self.assertEqual(updated_post.title, "Updated First")
        
        # Delete a post
        self.blog.delete_post(2)
        self.assertEqual(len(self.blog.list_posts()), 1)
        
        # Create another post
        post3 = self.blog.create_post("Third Post", "Final content")
        self.assertEqual(post3.code, 3)

if __name__ == '__main__':
    unittest.main()
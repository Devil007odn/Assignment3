import unittest
from blogging.post import Post
from datetime import datetime
from blogging.blog import Blog

class PostTest(unittest.TestCase):
    def test_post_init_stores_all_fields_exactly(self):
        """Verify all fields are stored with exact values."""
        post = Post(42, "Exact Title", "Exact Text")
        self.assertEqual(post.code, 42)
        self.assertEqual(post.title, "Exact Title")
        self.assertEqual(post.text, "Exact Text")

    def test_post_timestamps_are_datetime_objects(self):
        """Test that timestamps are datetime instances."""
        post = Post(1, "Title", "Text")
        self.assertIsInstance(post.creation, datetime)
        self.assertIsInstance(post.update, datetime)

    def test_post_timestamps_initially_equal(self):
        """Test creation and update are equal upon initialization."""
        post = Post(1, "Title", "Text")
        self.assertEqual(post.creation, post.update)

    # ===== update_timestamp tests =====
    def test_update_timestamp_changes_update_only(self):
        """Verify update_timestamp modifies update but not creation."""
        post = Post(1, "Title", "Text")
        original_creation = post.creation
        original_update = post.update
        
        import time
        time.sleep(0.001)  # Ensure measurable time difference
        post.update_timestamp()
        
        self.assertEqual(post.creation, original_creation)
        self.assertNotEqual(post.update, original_update)
        self.assertGreater(post.update, original_update)

    def test_multiple_calls_to_update_timestamp(self):
        """Test successive updates keep increasing the timestamp."""
        post = Post(1, "Title", "Text")
        timestamps = [post.update]
        
        for _ in range(3):
            import time
            time.sleep(0.001)
            post.update_timestamp()
            timestamps.append(post.update)
        
        # Verify each timestamp is greater than the previous
        for i in range(len(timestamps) - 1):
            self.assertGreater(timestamps[i + 1], timestamps[i])

    # ===== __eq__ tests =====
    def test_post_equality_requires_all_three_fields(self):
        """Test equality requires code, title, and text to all match."""
        base = Post(1, "Title", "Text")
        self.assertEqual(base, Post(1, "Title", "Text"))
        self.assertNotEqual(base, Post(2, "Title", "Text"))  # Different code
        self.assertNotEqual(base, Post(1, "Different", "Text"))  # Different title
        self.assertNotEqual(base, Post(1, "Title", "Different"))  # Different text

    def test_post_equality_with_none_and_other_types(self):
        """Test equality with None and non-Post objects."""
        post = Post(1, "Title", "Text")
        self.assertNotEqual(post, None)
        self.assertNotEqual(post, "not a post")
        self.assertNotEqual(post, 123)
        self.assertNotEqual(post, Blog(1, "Name", "url", "email"))

    def test_post_equality_ignores_timestamps(self):
        """Test that equality comparison ignores timestamp differences."""
        post1 = Post(1, "Title", "Text")
        post2 = Post(1, "Title", "Text")
        post1.update_timestamp()  # Only post1's update changes
        self.assertEqual(post1, post2)  # Should still be equal

    # ===== __str__ tests =====
    def test_post_str_includes_all_fields(self):
        """Test string representation includes code, title, and truncated text."""
        post = Post(99, "My Title", "This is the post content")
        s = str(post)
        self.assertIn("code=99", s)
        self.assertIn("title='My Title'", s)
        self.assertIn("text=", s)

    def test_post_str_truncates_long_text(self):
        """Test that text longer than 20 characters gets truncated."""
        long_text = "A" * 50  # 50 characters
        post = Post(1, "Title", long_text)
        s = str(post)
        # Should contain first 20 chars followed by ...
        self.assertIn("A" * 20 + "...", s)
        self.assertLess(len(s), len(long_text) + 30)  # Much shorter than full text

    def test_post_str_with_empty_text(self):
        """Test string representation with empty text."""
        post = Post(1, "Title", "")
        s = str(post)
        self.assertIn("text=''", s)

    def test_post_str_with_special_characters(self):
        """Test string representation handles special characters."""
        post = Post(1, "Title!@#$%^&*()", "Text with\nnewlines\tand\ttabs")
        s = str(post)
        self.assertIn("Title!@#$%^&*()", s)

    # ===== __repr__ tests =====
    def test_post_repr_exact_format(self):
        """Test repr returns exact expected format (no text field)."""
        post = Post(42, "Test Title", "This text is ignored in repr")
        self.assertEqual(repr(post), "Post(code=42, title='Test Title')")

    def test_post_repr_with_quotes_in_title(self):
        """Test repr handles quotes in title correctly."""
        post = Post(1, "Title with 'apostrophe'", "Text")
        repr_str = repr(post)
        # Should contain escaped or maintained quotes
        self.assertIn("title='Title with 'apostrophe''", repr_str)

if __name__ == '__main__':
    unittest.main()

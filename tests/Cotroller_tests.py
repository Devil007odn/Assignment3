from unittest import TestCase
from unittest import main
from blogging.controller import Controller
from blogging.blog import Blog
from blogging.post import Post

class ControllerTest(TestCase):

	def setUp(self):
		self.controller = Controller()

	def test_login_logout(self):

		self.assertFalse(self.controller.logout(), "log out only after being logged in")

		self.assertFalse(self.controller.login("theuser", "blogging2025"), "login in with incorrect username")

		self.assertFalse(self.controller.login("user", "123456"), "login in with incorrect password")

		self.assertTrue(self.controller.login("user", "blogging2025"), "login correctly")

		self.assertFalse(self.controller.login("user", "blogging2025"), "cannot login again while still logged in")

		self.assertTrue(self.controller.logout(), "log out correctly")

		self.assertTrue(self.controller.login("user", "blogging2025"), "can login again")

		self.assertTrue(self.controller.logout(), "can log out again")

	def test_create_search_blog(self):
		# some blogs that will be created
		expected_blog_1 = Blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		expected_blog_2 = Blog(1111115555, "Long Journey", "long_journey", "long.journey@gmail.com")
		expected_blog_3 = Blog(1111112000, "Long Trip", "long_trip", "long.trip@gmail.com")

		# cannot do operation without logging in
		self.assertIsNone(self.controller.create_blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com"), 
			"cannot create blog without logging in")

		# add one blog
		self.assertTrue(self.controller.login("user", "blogging2025"), "login correctly")
		actual_blog = self.controller.create_blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		self.assertIsNotNone(actual_blog, "blog created cannot be null")

		# implement __eq__(self, other) in Blog to compare blogs based on its attributes
		self.assertEqual(expected_blog_1, actual_blog, "Short Journey blog was created and their data are correct")

		# after creating the blog, one should be able to search it
		actual_blog = self.controller.search_blog(1111114444)
		self.assertIsNotNone(actual_blog, "blog created and retrieved cannot be null")
		self.assertEqual(expected_blog_1, actual_blog, "Short Journey blog was created, retrieved and its data are correct")

		# should not allow to create another blog with same id
		actual_blog = self.controller.create_blog(1111114444, "Long Journey", "long_journey", "long.journey@gmail.com")
		self.assertIsNone(actual_blog, "cannot create blog with same id as from an existing blog")

		# add a second blog
		actual_blog = self.controller.create_blog(1111115555, "Long Journey", "long_journey", "long.journey@gmail.com")
		self.assertIsNotNone(actual_blog, "second blog created cannot be null")
		self.assertEqual(expected_blog_2, actual_blog, "second blog, Long Journey, was created and its data are correct")
		actual_blog = self.controller.search_blog(1111115555)
		self.assertIsNotNone(actual_blog, "blog created and retrieved cannot be null")
		self.assertEqual(expected_blog_2, actual_blog, "second blog, Long Journey, was created, retrieved and its data are correct")

		# add a third blog
		actual_blog = self.controller.create_blog(1111112000, "Long Trip", "long_trip", "long.trip@gmail.com")
		self.assertIsNotNone(actual_blog, "blog created cannot be null")
		self.assertEqual(expected_blog_3, actual_blog, "Long Trip blog was created and its data are correct")
		actual_blog = self.controller.search_blog(1111112000)
		self.assertIsNotNone(actual_blog, "blog created and retrieved cannot be null")
		self.assertEqual(expected_blog_3, actual_blog, "third blog, Long Trip, was created, retrieved and its data are correct")

		# creating new blogs should not affect previous blogs
		actual_blog = self.controller.search_blog(1111115555)
		self.assertIsNotNone(actual_blog, "blog created and retrieved cannot be null, regardless of search order")
		self.assertEqual(expected_blog_2, actual_blog, "Long Journey blog was created, retrieved and its data are correct regardless of search order")
		actual_blog = self.controller.search_blog(1111114444)
		self.assertIsNotNone(actual_blog, "blog created and retrieved cannot be null, regardless of search order")
		self.assertEqual(expected_blog_1, actual_blog, "Short Journey blog was created, retrieved and its data are correct regardless of search order")


	def test_retrieve_blogs(self):
		# some blogs that will be retrieved
		expected_blog_1 = Blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		expected_blog_2 = Blog(1111115555, "Long Journey", "long_journey", "long.journey@gmail.com")
		expected_blog_3 = Blog(1111112000, "Long Trip", "long_trip", "long.trip@gmail.com")
		expected_blog_4 = Blog(1111116666, "Short Trip", "short_trip", "short.trip@gmail.com")
		expected_blog_5 = Blog(1111117777, "Boring Blog", "boring_blog", "boring.blog@gmail.com")

		# cannot do operation without logging in
		self.assertIsNone(self.controller.retrieve_blogs("Short Journey"), "cannot retrieve blogs without logging in")

		# login and create some blogs
		self.assertTrue(self.controller.login("user", "blogging2025"), "login correctly")
		self.controller.create_blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		self.controller.create_blog(1111115555, "Long Journey", "long_journey", "long.journey@gmail.com")
		self.controller.create_blog(1111112000, "Long Trip", "long_trip", "long.trip@gmail.com")
		self.controller.create_blog(1111116666, "Short Trip", "short_trip", "short.trip@gmail.com")
		self.controller.create_blog(1111117777, "Boring Blog", "boring_blog", "boring.blog@gmail.com")

		# retrieve one blog
		retrieved_list = self.controller.retrieve_blogs("Long Journey")
		self.assertEqual(1, len(retrieved_list), "retrieved list of blogs has size 1")
		actual_blog = retrieved_list[0]
		self.assertEqual(expected_blog_2, actual_blog, "retrieved blog in the list is Long Journey")

		# retrieve two blogs
		retrieved_list = self.controller.retrieve_blogs("Journey")
		self.assertEqual(2, len(retrieved_list), "retrieved list of blogs with Journey keyword has size 2")
		self.assertEqual(expected_blog_1, retrieved_list[0], "first blog in the retrieved list is Short Journey")
		self.assertEqual(expected_blog_2, retrieved_list[1], "second blog in the retrieved list is Long Journey")

		# retrieve zero blogs
		retrieved_list = self.controller.retrieve_blogs("Travel")
		self.assertEqual(0, len(retrieved_list))

	def test_update_blog(self):
		# some blogs that may be updated
		expected_blog_1 = Blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		expected_blog_2 = Blog(1111115555, "Long Journey", "long_journey", "long.journey@gmail.com")
		expected_blog_3 = Blog(1111112000, "Long Trip", "long_trip", "long.trip@gmail.com")
		expected_blog_4 = Blog(1111116666, "Short Trip", "short_trip", "short.trip@gmail.com")
		expected_blog_5 = Blog(1111117777, "Boring Blog", "boring_blog", "boring.blog@gmail.com")

		# cannot do operation without logging in
		self.assertFalse(self.controller.update_blog(1111114444, 1111114444, "Short Travel", "short_travel", "short.travel@gmail.com"), 
			"cannot update blog without logging in")

		# login
		self.assertTrue(self.controller.login("user", "blogging2025"), "login correctly")

		# try to update a blog when there are no blogs in the system
		self.assertFalse(self.controller.update_blog(1111114444, 1111114444, "Short Travel", "short_travel", "short.travel@gmail.com"),
			"cannot update blog when there are no blogs in the system")

		# create some blogs
		self.controller.create_blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		self.controller.create_blog(1111115555, "Long Journey", "long_journey", "long.journey@gmail.com")
		self.controller.create_blog(1111112000, "Long Trip", "long_trip", "long.trip@gmail.com")
		self.controller.create_blog(1111116666, "Short Trip", "short_trip", "short.trip@gmail.com")
		self.controller.create_blog(1111117777, "Boring Blog", "boring_blog", "boring.blog@gmail.com")

		# update one blog, but keep the Blog key (id) unchanged
		self.assertTrue(self.controller.update_blog(1111114444, 1111114444, "Short Travel", "short_travel", "short.travel@gmail.com"), 
			"update blog data and keep the id unchanged")
		actual_blog = self.controller.search_blog(1111114444)
		self.assertNotEqual(expected_blog_1, actual_blog, "blog has updated data, cannot be equal to the original data")
		expected_blog_3a = Blog(1111114444, "Short Travel", "short_travel", "short.travel@gmail.com")
		self.assertEqual(expected_blog_3a, actual_blog, "blog was updated, its data have to be updated and correct")

		# update one blog, and change the Blog key (id) as well
		self.assertTrue(self.controller.update_blog(1111117777, 1111118888, "Cool Blog", "cool_blog", "cool.blog@gmail.com"), 
			"update blog data and also change the id")
		actual_blog = self.controller.search_blog(1111118888)
		self.assertNotEqual(expected_blog_5, actual_blog, "blog has updated data, cannot be equal to the original data")
		expected_blog_5a = Blog(1111118888, "Cool Blog", "cool_blog", "cool.blog@gmail.com")
		self.assertEqual(expected_blog_5a, actual_blog, "blog was updated, its data have to be updated and correct")

		# update one blog with a conflicting existing id
		self.assertFalse(self.controller.update_blog(1111114444, 1111112000, "Short Travel", "short_travel", "short.travel@gmail.com"), 
			"cannot update blog and give it a registered id")

	def test_delete_blog(self):
		# some blogs that may be deleted
		expected_blog_1 = Blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		expected_blog_2 = Blog(1111115555, "Long Journey", "long_journey", "long.journey@gmail.com")
		expected_blog_3 = Blog(1111112000, "Long Trip", "long_trip", "long.trip@gmail.com")
		expected_blog_4 = Blog(1111116666, "Short Trip", "short_trip", "short.trip@gmail.com")
		expected_blog_5 = Blog(1111117777, "Boring Blog", "boring_blog", "boring.blog@gmail.com")

		# cannot do operation without logging in
		self.assertFalse(self.controller.delete_blog(1111114444), "cannot delete blog without logging in")

		# login
		self.assertTrue(self.controller.login("user", "blogging2025"), "login correctly")

		# try to delete a blog when there are no blogs in the system
		self.assertFalse(self.controller.delete_blog(1111114444), "cannot delete blog when there are no blogs in the system")

		# add some blogs
		self.controller.create_blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		self.controller.create_blog(1111115555, "Long Journey", "long_journey", "long.journey@gmail.com")
		self.controller.create_blog(1111112000, "Long Trip", "long_trip", "long.trip@gmail.com")
		self.controller.create_blog(1111116666, "Short Trip", "short_trip", "short.trip@gmail.com")
		self.controller.create_blog(1111117777, "Boring Blog", "boring_blog", "boring.blog@gmail.com")

		# delete one blog at the start of the collection
		self.assertTrue(self.controller.delete_blog(1111114444), "delete blog from the start of the collection")
		self.assertIsNone(self.controller.search_blog(1111114444), "deleted blog cannot be found in the system")

		# delete one blog at the middle of the collection
		self.assertTrue(self.controller.delete_blog(1111112000), "delete blog from the middle of the collection")
		self.assertIsNone(self.controller.search_blog(1111112000), "deleted blog cannot be found in the system")

		# delete one blog at the end of the collection
		self.assertTrue(self.controller.delete_blog(1111117777), "delete blog from the end of the collection")
		self.assertIsNone(self.controller.search_blog(1111117777), "deleted blog cannot be found in the system")

	def test_list_blogs(self):
		# some blogs that may be listed
		expected_blog_1 = Blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		expected_blog_2 = Blog(1111115555, "Long Journey", "long_journey", "long.journey@gmail.com")
		expected_blog_3 = Blog(1111112000, "Long Trip", "long_trip", "long.trip@gmail.com")
		expected_blog_4 = Blog(1111116666, "Short Trip", "short_trip", "short.trip@gmail.com")
		expected_blog_5 = Blog(1111117777, "Boring Blog", "boring_blog", "boring.blog@gmail.com")

		# cannot do operation without logging in
		self.assertIsNone(self.controller.list_blogs(), "cannot list blogs without logging in")

		# login
		self.assertTrue(self.controller.login("user", "blogging2025"), "login correctly")

		# listing blogs when there are no blogs in the system
		blogs_list = self.controller.list_blogs()
		self.assertEqual(0, len(blogs_list), "list of blogs has size 0")

		# add one blog
		self.controller.create_blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")

		# listing blogs in a singleton list
		blogs_list = self.controller.list_blogs()
		self.assertEqual(1, len(blogs_list), "list of blogs has size 1")
		self.assertEqual(expected_blog_1, blogs_list[0], "Short Journey blog is the only one in the list of blogs")

		# add some more blogs
		self.controller.create_blog(1111115555, "Long Journey", "long_journey", "long.journey@gmail.com")
		self.controller.create_blog(1111112000, "Long Trip", "long_trip", "long.trip@gmail.com")
		self.controller.create_blog(1111116666, "Short Trip", "short_trip", "short.trip@gmail.com")
		self.controller.create_blog(1111117777, "Boring Blog", "boring_blog", "boring.blog@gmail.com")


		# listing blogs in a larger list
		blogs_list = self.controller.list_blogs()
		self.assertEqual(5, len(blogs_list), "list of blogs has size 5")
		self.assertEqual(expected_blog_1, blogs_list[0], "blog 1 is the first in the list of blogs")
		self.assertEqual(expected_blog_2, blogs_list[1], "blog 2 is the second in the list of blogs")
		self.assertEqual(expected_blog_3, blogs_list[2], "blog 3 is the third in the list of blogs")
		self.assertEqual(expected_blog_4, blogs_list[3], "blog 4 is the fourth in the list of blogs")
		self.assertEqual(expected_blog_5, blogs_list[4], "blog 5 is the fifth in the list of blogs")

		# deleting some blogs
		self.controller.delete_blog(1111114444)
		self.controller.delete_blog(1111112000)
		self.controller.delete_blog(1111117777)

		# listing blogs after deleting some blogs
		blogs_list = self.controller.list_blogs()
		self.assertEqual(2, len(blogs_list), "list of blogs has size 2")
		self.assertEqual(expected_blog_2, blogs_list[0], "blog 2 is the first in the list of blogs")
		self.assertEqual(expected_blog_4, blogs_list[1], "blog 4 is the second in the list of blogs")

	def test_set_get_current_blog(self):
		# one of these blogs will be set as the current blog
		expected_blog_1 = Blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		expected_blog_2 = Blog(1111115555, "Long Journey", "long_journey", "long.journey@gmail.com")
		expected_blog_3 = Blog(1111112000, "Long Trip", "long_trip", "long.trip@gmail.com")
		expected_blog_4 = Blog(1111116666, "Short Trip", "short_trip", "short.trip@gmail.com")
		expected_blog_5 = Blog(1111117777, "Boring Blog", "boring_blog", "boring.blog@gmail.com")

		# cannot do operation without logging in
		self.assertIsNone(self.controller.get_current_blog(), "cannot get current blog without logging in")

		# login
		self.assertTrue(self.controller.login("user", "blogging2025"), "login correctly")

		# add some blogs
		self.controller.create_blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		self.controller.create_blog(1111115555, "Long Journey", "long_journey", "long.journey@gmail.com")
		self.controller.create_blog(1111112000, "Long Trip", "long_trip", "long.trip@gmail.com")
		self.controller.create_blog(1111116666, "Short Trip", "short_trip", "short.trip@gmail.com")
		self.controller.create_blog(1111117777, "Boring Blog", "boring_blog", "boring.blog@gmail.com")

		# cannot get current blog without setting it first
		self.assertIsNone(self.controller.get_current_blog(), "cannot get current blog without setting them first")

		# cannot set a non-existent blog to be the current blog
		self.controller.set_current_blog(1111110001)
		self.assertIsNone(self.controller.get_current_blog(), "cannot get non-existent blog as current blog")

		# set one blog to be the current blog
		self.controller.set_current_blog(1111112000)
		actual_current_blog = self.controller.get_current_blog()
		self.assertIsNotNone(actual_current_blog)
		self.assertEqual(expected_blog_3, actual_current_blog, "expected current blog is blog 3")

		# cannot delete the current blog, unset current blog first
		self.assertFalse(self.controller.delete_blog(1111112000), "cannot delete the current blog")

		# cannot update the current blog, unset current blog first
		self.assertFalse(self.controller.update_blog(1111112000, 1111112000, "Short Travel", "short_travel", "short.travel@gmail.com"), 
			"cannot update the current blog")

		# unset current blog
		self.controller.unset_current_blog()
		actual_current_blog = self.controller.get_current_blog()
		self.assertIsNone(actual_current_blog)

		# handle log out
		self.controller.set_current_blog(1111112000)
		self.controller.logout()
		actual_current_blog = self.controller.get_current_blog()
		self.assertIsNone(actual_current_blog)

	def test_create_post(self):
		# some posts that may be created
		expected_post_1 = Post(1, "Starting my journey", "Once upon a time\nThere was a kid...")
		expected_post_2 = Post(2, "Continuing my journey", "Along the way...\nThere were challenges.")
		expected_post_3 = Post(3, "Finishing my journey", "And that was it.\nEnd of story.")

		# cannot do operation without logging in
		self.assertIsNone(self.controller.create_post("Starting my journey", "Once upon a time\nThere was a kid..."), "cannot add post without logging in")

		# login
		self.assertTrue(self.controller.login("user", "blogging2025"), "login correctly")

		# cannot do operation without a valid current blog
		self.assertIsNone(self.controller.create_post("Starting my journey", "Once upon a time\nThere was a kid..."), "cannot add post without a valid current blog")

		# add one blog and make it the current blog
		self.controller.create_blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		self.controller.set_current_blog(1111114444)

		# add one post
		actual_post = self.controller.create_post("Starting my journey", "Once upon a time\nThere was a kid...")
		self.assertIsNotNone(actual_post, "post 1 was created and is valid")

		# implement __eq__(self, other) in Post to compare posts based on their code, title and text
		self.assertEqual(expected_post_1, actual_post, "post 1 was created and its data are correct")

		# after creating the post, one should be able to search it
		actual_post = self.controller.search_post(1)
		self.assertIsNotNone(actual_post, "post created and retrieved cannot be null")
		self.assertEqual(expected_post_1, actual_post, "post 1 was created, retrieved and its data are correct")

		# add a second post
		actual_post = self.controller.create_post("Continuing my journey", "Along the way...\nThere were challenges.")
		self.assertIsNotNone(actual_post, "post 2 was created and is valid")
		self.assertEqual(expected_post_2, actual_post, "post 2 was created and its data are correct")

		# after creating the post, one should be able to search it
		actual_post = self.controller.search_post(2)
		self.assertIsNotNone(actual_post, "post created and retrieved cannot be null")
		self.assertEqual(expected_post_2, actual_post, "post 2 was created, retrieved and its data are correct")

		# add a third post
		actual_post = self.controller.create_post("Finishing my journey", "And that was it.\nEnd of story.")
		self.assertIsNotNone(actual_post, "post 3 was created and is valid")
		self.assertEqual(expected_post_3, actual_post, "post 3 was created and its data are correct")

		# after creating the post, one should be able to search it
		actual_post = self.controller.search_post(3)
		self.assertIsNotNone(actual_post, "post created and retrieved cannot be null")
		self.assertEqual(expected_post_3, actual_post, "post 3 was created, retrieved and its data are correct")

		# creating new posts should not affect previous posts
		actual_post = self.controller.search_post(2)
		self.assertIsNotNone(actual_post, "post created and retrieved cannot be null regardless of search order")
		self.assertEqual(expected_post_2, actual_post, "post 2 was created, retrieved and its data are correct regardless of search order")
		actual_post = self.controller.search_post(1)
		self.assertIsNotNone(actual_post, "post created and retrieved cannot be null regardless of search order")
		self.assertEqual(expected_post_1, actual_post, "post 1 was created, retrieved and its data are correct regardless of search order")

	def test_retrieve_posts(self):
		# some posts that may be retrieved
		expected_post_1 = Post(1, "Starting my journey", "Once upon a time\nThere was a kid...")
		expected_post_2 = Post(2, "Second step", "Before one could think,\nA storm stroke.")
		expected_post_3 = Post(3, "Continuing my journey", "Along the way...\nThere were challenges.")
		expected_post_4 = Post(4, "Fourth step", "When less expected,\nAll worked fine.")
		expected_post_5 = Post(5, "Finishing my journey", "And that was it.\nEnd of story.")

		# cannot do operation without logging in
		self.assertIsNone(self.controller.retrieve_posts("journey"), "cannot retrieve posts without logging in")

		# login
		self.assertTrue(self.controller.login("user", "blogging2025"), "login correctly")

		# cannot do operation without a valid current blog
		self.assertIsNone(self.controller.retrieve_posts("journey"), "cannot retrieve posts without a valid current blog")

		# add one blog and make it the current blog
		self.controller.create_blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		self.controller.set_current_blog(1111114444)

		# add some posts
		self.controller.create_post("Starting my journey", "Once upon a time\nThere was a kid...")
		self.controller.create_post("Second step", "Before one could think,\nA storm stroke.")
		self.controller.create_post("Continuing my journey", "Along the way...\nThere were challenges.")
		self.controller.create_post("Fourth step", "When less expected,\nAll worked fine.")
		self.controller.create_post("Finishing my journey", "And that was it.\nEnd of story.")

		# retrieve one post
		retrieved_list = self.controller.retrieve_posts("think")
		self.assertEqual(1, len(retrieved_list), "retrieved list of posts has size 1")
		actual_post = retrieved_list[0]
		self.assertEqual(expected_post_2, actual_post, "retrieved post in the list is post 2")

		# retrieve three posts
		retrieved_list = self.controller.retrieve_posts("journey")
		self.assertEqual(3, len(retrieved_list), "retrieved list of journey posts from Short Journey blog has size 3")
		self.assertEqual(expected_post_1, retrieved_list[0], "first retrieved post in the list is post 1")
		self.assertEqual(expected_post_3, retrieved_list[1], "second retrieved post in the list is post 2")
		self.assertEqual(expected_post_5, retrieved_list[2], "third retrieved post in the list is post 4")

		# retrieve zero posts
		retrieved_list = self.controller.retrieve_posts("travel")
		self.assertEqual(0, len(retrieved_list))

	def test_update_post(self):
		# some posts that may be updated
		expected_post_1 = Post(1, "Starting my journey", "Once upon a time\nThere was a kid...")
		expected_post_2 = Post(2, "Second step", "Before one could think,\nA storm stroke.")
		expected_post_3 = Post(3, "Continuing my journey", "Along the way...\nThere were challenges.")
		expected_post_4 = Post(4, "Fourth step", "When less expected,\nAll worked fine.")
		expected_post_5 = Post(5, "Finishing my journey", "And that was it.\nEnd of story.")

		# cannot do operation without logging in
		self.assertFalse(self.controller.update_post(3, "Continuing the journey", "Along the way...\nThere were new challenges."), 
			"cannot update posts without logging in")

		# login
		self.assertTrue(self.controller.login("user", "blogging2025"), "login correctly")

		# cannot do operation without a valid current blog
		self.assertFalse(self.controller.update_post(3, "Continuing the journey", "Along the way...\nThere were new challenges."), 
			"cannot update posts without a valid current blog")

		# add one blog and make it the current blog
		self.controller.create_blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		self.controller.set_current_blog(1111114444)

		# try to update a post when there are no posts taken for that blog in the system
		self.assertFalse(self.controller.update_post(3, "Continuing the journey", "Along the way...\nThere were new challenges."),
			"cannot update post when there are no posts for that blog in the system")

		# add some posts
		self.controller.create_post("Starting my journey", "Once upon a time\nThere was a kid...")
		self.controller.create_post("Second step", "Before one could think,\nA storm stroke.")
		self.controller.create_post("Continuing my journey", "Along the way...\nThere were challenges.")
		self.controller.create_post("Fourth step", "When less expected,\nAll worked fine.")
		self.controller.create_post("Finishing my journey", "And that was it.\nEnd of story.")

		# update one existing post
		self.assertTrue(self.controller.update_post(3, "Continuing the journey", "Along the way...\nThere were new challenges."), 
			"update blog's post")
		actual_post = self.controller.search_post(3)
		self.assertNotEqual(expected_post_3, actual_post, "post has updated data, cannot be equal to the original data")
		expected_post_3a = Post(3, "Continuing the journey", "Along the way...\nThere were new challenges.")
		self.assertEqual(expected_post_3a, actual_post, "blog was updated, their data has to be updated and correct")
		# Notice we have not checked the timestamps. 
		# You should check that manually.
		# Some parts of code are not simple to test (timing issues are an example).
		# How can anyone fix that in general?

		# update another existing post
		self.assertTrue(self.controller.update_post(5, "Finishing my travel", "And that was it.\nEnd of travel."), 
			"update blog's post")
		actual_post = self.controller.search_post(5)
		self.assertNotEqual(expected_post_5, actual_post, "post has updated data, cannot be equal to the original data")
		expected_post_5a = Post(5, "Finishing my travel", "And that was it.\nEnd of travel.")
		self.assertEqual(expected_post_5a, actual_post, "blog was updated, their data has to be updated and correct")

	def test_delete_post(self):
		# some posts that may be deleted
		expected_post_1 = Post(1, "Starting my journey", "Once upon a time\nThere was a kid...")
		expected_post_2 = Post(2, "Second step", "Before one could think,\nA storm stroke.")
		expected_post_3 = Post(3, "Continuing my journey", "Along the way...\nThere were challenges.")
		expected_post_4 = Post(4, "Fourth step", "When less expected,\nAll worked fine.")
		expected_post_5 = Post(5, "Finishing my journey", "And that was it.\nEnd of story.")

		# cannot do operation without logging in
		self.assertFalse(self.controller.delete_post(3), "cannot delete post without logging in")

		# login
		self.assertTrue(self.controller.login("user", "blogging2025"), "login correctly")

		# cannot do operation without a valid current blog
		self.assertFalse(self.controller.delete_post(3), "cannot delete post without a valid current blog")

		# add one blog and make it the current blog
		self.controller.create_blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		self.controller.set_current_blog(1111114444)

		# try to delete a post when there are no posts taken for that blog in the system
		self.assertFalse(self.controller.delete_post(3), "cannot delete post when there are no posts for that blog in the system")

		# add some posts
		self.controller.create_post("Starting my journey", "Once upon a time\nThere was a kid...")
		self.controller.create_post("Second step", "Before one could think,\nA storm stroke.")
		self.controller.create_post("Continuing my journey", "Along the way...\nThere were challenges.")
		self.controller.create_post("Fourth step", "When less expected,\nAll worked fine.")
		self.controller.create_post("Finishing my journey", "And that was it.\nEnd of story.")

		# delete one existing post
		self.assertTrue(self.controller.delete_post(3), "delete blog's post")
		self.assertIsNone(self.controller.search_post(3))

		# delete the remaining existing posts, regardless of deleting order
		self.assertTrue(self.controller.delete_post(1), "delete blog's post")
		self.assertIsNone(self.controller.search_post(1))
		self.assertTrue(self.controller.delete_post(5), "delete blog's post")
		self.assertIsNone(self.controller.search_post(5))
		self.assertTrue(self.controller.delete_post(4), "delete blog's post")
		self.assertIsNone(self.controller.search_post(4))
		self.assertTrue(self.controller.delete_post(2), "delete blog's post")
		self.assertIsNone(self.controller.search_post(2))

	def test_list_posts(self):
		# some posts that may be listed
		expected_post_1 = Post(1, "Starting my journey", "Once upon a time\nThere was a kid...")
		expected_post_2 = Post(2, "Second step", "Before one could think,\nA storm stroke.")
		expected_post_3 = Post(3, "Continuing my journey", "Along the way...\nThere were challenges.")
		expected_post_4 = Post(4, "Fourth step", "When less expected,\nAll worked fine.")
		expected_post_5 = Post(5, "Finishing my journey", "And that was it.\nEnd of story.")

		# cannot do operation without logging in
		self.assertIsNone(self.controller.list_posts(), "cannot list posts for a blog without logging in")

		# login
		self.assertTrue(self.controller.login("user", "blogging2025"), "login correctly")

		# listing posts when there are no blogs in the system
		self.assertIsNone(self.controller.list_posts(), "cannot list posts when there are no blogs in the system")

		# add one blog and make it the current blog
		self.controller.create_blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		self.controller.set_current_blog(1111114444)

		# listing posts when the current blog has no posts
		posts_list = self.controller.list_posts()
		self.assertEqual(0, len(posts_list), "list of posts for blog has size 0")

		# listing posts in a singleton list
		actual_post = self.controller.create_post("Starting my journey", "Once upon a time\nThere was a kid...")
		posts_list = self.controller.list_posts()
		self.assertEqual(1, len(posts_list), "list of posts for blog has size 1")
		self.assertEqual(expected_post_1, posts_list[0], "post 1 is the listed post.")

		# add some more posts
		self.controller.create_post("Second step", "Before one could think,\nA storm stroke.")
		self.controller.create_post("Continuing my journey", "Along the way...\nThere were challenges.")
		self.controller.create_post("Fourth step", "When less expected,\nAll worked fine.")
		self.controller.create_post("Finishing my journey", "And that was it.\nEnd of story.")

		# listing posts in a larger list
		posts_list = self.controller.list_posts()
		self.assertEqual(5, len(posts_list), "list of posts has size 5")
		self.assertEqual(expected_post_5, posts_list[0], "post 5 is the first in the list of blogs")
		self.assertEqual(expected_post_4, posts_list[1], "post 4 is the second in the list of blogs")
		self.assertEqual(expected_post_3, posts_list[2], "post 3 is the third in the list of blogs")
		self.assertEqual(expected_post_2, posts_list[3], "post 2 is the fourth in the list of blogs")
		self.assertEqual(expected_post_1, posts_list[4], "post 1 is the fifth in the list of blogs")

		# deleting some posts
		self.controller.delete_post(3)
		self.controller.delete_post(1)
		self.controller.delete_post(5)

		# listing posts for a blog with deleted posts
		posts_list = self.controller.list_posts()
		self.assertEqual(2, len(posts_list), "list of posts has size 2")
		self.assertEqual(expected_post_4, posts_list[0], "post 4 is the first in the list of posts")
		self.assertEqual(expected_post_2, posts_list[1], "post 2 is the second in the list of posts")


if __name__ == '__main__':
	unittest.main()
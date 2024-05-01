import unittest
from courses import image_load  # Import implementation based on file path


class TestImageDirs(unittest.TestCase):

    def test_avatar_dir_constant(self):
        self.assertEqual(image_load.ImageDirs.AVATAR_DIR, 'avatars/')

    def test_course_dir_constant(self):
        self.assertEqual(image_load.ImageDirs.COURSE_DIR, 'courses/')

    def test_answer_dir_constant(self):
        self.assertEqual(image_load.ImageDirs.ANSWER_DIR, 'answers/')

    def test_question_dir_constant(self):
        self.assertEqual(image_load.ImageDirs.QUESTION_DIR, 'questions/')

    def test_home_dir_constant(self):
        self.assertEqual(image_load.ImageDirs.HOME_DIR, 'home_images/')


if __name__ == "__main__":
    unittest.main()

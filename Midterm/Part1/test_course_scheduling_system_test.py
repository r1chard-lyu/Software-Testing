import unittest
from unittest.mock import Mock
from course_scheduling_system import CSS

class TestCSS(unittest.TestCase):
    def test_q1_1(self):
        # 使用 Mock 讓 check_course_exist 返回 True
        css = CSS()
        css.check_course_exist = Mock(return_value=True)

        # 試著添加一個課程
        course = ('Algorithms', 'Monday', 3, 4)
        result = css.add_course(course)

        # 檢查 add_course 的返回值
        self.assertTrue(result)

        # 驗證 get_course_list 的結果
        course_list = css.get_course_list()
        self.assertEqual(len(course_list), 1)
        self.assertEqual(course_list[0], course)

    def test_q1_2(self):
        css = CSS()
        css.check_course_exist = Mock(return_value=True)

        course1 = ('Algorithms', 'Monday', 3, 4)
        course2 = ('Data Structures', 'Monday', 4, 5)

        result1 = css.add_course(course1)
        result2 = css.add_course(course2)

        self.assertTrue(result1)
        self.assertFalse(result2)

        course_list = css.get_course_list()
        self.assertEqual(len(course_list), 1)
        self.assertEqual(course_list[0], course1)

    def test_q1_3(self):
        css = CSS()
        css.check_course_exist = Mock(return_value=False)

        course = ('Algorithms', 'Monday', 3, 4)
        result = css.add_course(course)

        self.assertFalse(result)

    def test_q1_4(self):
        css = CSS()
        css.check_course_exist = Mock(return_value=True)

        invalid_course = ('Algorithms', 'Monday', 4, 3)

        with self.assertRaises(TypeError):
            css.add_course(invalid_course)

    

    def test_q1_5(self):
        css = CSS()
        css.check_course_exist = Mock(return_value=True)

        course1 = ('Algorithms', 'Monday', 3, 4)
        course2 = ('Data Structures', 'Tuesday', 3, 4)
        course3 = ('Operating Systems', 'Wednesday', 3, 4)

        css.add_course(course1)
        css.add_course(course2)
        css.add_course(course3)

        css.remove_course(course2)

        course_list = css.get_course_list()
        self.assertEqual(len(course_list), 2)
        self.assertEqual(course_list[0], course1)
        self.assertEqual(course_list[1], course3)

        self.assertEqual(css.check_course_exist.call_count, 4)

        print(css)

        
    def test_q1_6_1(self):
        css = CSS()
        css.check_course_exist = Mock(return_value=True)

        invalid_course1 = ('Algorithms', 'Monday', 0, 3)
        invalid_course2 = ('Algorithms', 'Monday', 3, 9)
        invalid_course3 = ('Algorithms', 'InvalidDay', 3, 4)
        invalid_course4 = (123, 'Monday', 3, 4)

        with self.assertRaises(TypeError):
            css.add_course(invalid_course1)

        with self.assertRaises(TypeError):
            css.add_course(invalid_course2)

        with self.assertRaises(TypeError):
            css.add_course(invalid_course3)

        with self.assertRaises(TypeError):
            css.add_course(invalid_course4)

    def test_q1_6_2(self):
        css = CSS()
        css.check_course_exist = Mock(return_value=True)

        course1 = ('Algorithms', 'Monday', 3, 4)
        css.add_course(course1)

        invalid_course = ('Algorithms', 'Monday', 4, 3)
        with self.assertRaises(TypeError):
            css.remove_course(invalid_course)

    def test_q1_6_3(self):
        css = CSS()
        css.check_course_exist = Mock(return_value=True)

        # Test an invalid course format
        with self.assertRaises(TypeError):
            invalid_course = ('Algorithms', 'InvalidDay', 3, 4)
            css.add_course(invalid_course)

        # Test a case where check_course_exist is called
        course = ('Algorithms', 'Monday', 3, 4)
        css.add_course(course)

        # Test removal of a non-existent course
        non_existent_course = ('Data Structures', 'Tuesday', 3, 4)
        result = css.remove_course(non_existent_course)
        self.assertFalse(result)

        # Check the call count of check_course_exist
        css.check_course_exist.assert_called_with(non_existent_course)

        
        # Test a non-tuple input
        with self.assertRaises(TypeError):
            non_tuple_course = ['Algorithms', 'Monday', 3, 4]
            css.add_course(non_tuple_course)

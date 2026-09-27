import unittest
from stack import Stack


class TestStack(unittest.TestCase):

    def test_new_stack_is_empty(self):
        s = Stack()
        self.assertTrue(s.is_empty())
        self.assertEqual(s.size(), 0)

    def test_push_adds_item(self):
        s = Stack()
        s.push(1)
        self.assertFalse(s.is_empty())
        self.assertEqual(s.size(), 1)

    def test_pop_returns_last_pushed_item(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertEqual(s.pop(), 3)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.size(), 1)

    def test_peek_does_not_remove_item(self):
        s = Stack()
        s.push(10)
        self.assertEqual(s.peek(), 10)
        self.assertEqual(s.size(), 1)

    def test_pop_from_empty_stack_raises_error(self):
        s = Stack()
        with self.assertRaises(IndexError):
            s.pop()

    def test_peek_from_empty_stack_raises_error(self):
        s = Stack()
        with self.assertRaises(IndexError):
            s.peek()


if __name__ == "__main__":
    unittest.main()

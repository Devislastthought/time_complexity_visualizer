import unittest
from queue_ds import Queue


class TestQueue(unittest.TestCase):

    def test_new_queue_is_empty(self):
        q = Queue()
        self.assertTrue(q.is_empty())
        self.assertEqual(q.size(), 0)

    def test_enqueue_adds_item(self):
        q = Queue()
        q.enqueue(1)
        self.assertFalse(q.is_empty())
        self.assertEqual(q.size(), 1)

    def test_dequeue_returns_first_enqueued_item(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        self.assertEqual(q.dequeue(), 1)  # first in, first out
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.size(), 1)

    def test_peek_does_not_remove_item(self):
        q = Queue()
        q.enqueue(10)
        self.assertEqual(q.peek(), 10)
        self.assertEqual(q.size(), 1)  # still there

    def test_dequeue_from_empty_queue_raises_error(self):
        q = Queue()
        with self.assertRaises(IndexError):
            q.dequeue()

    def test_peek_from_empty_queue_raises_error(self):
        q = Queue()
        with self.assertRaises(IndexError):
            q.peek()


if __name__ == "__main__":
    unittest.main()

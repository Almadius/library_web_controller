import unittest
from library.member import Member

class TestMember(unittest.TestCase):

    def test_member_creation(self):
        member = Member("Alice", 1)
        self.assertEqual(member.name, "Alice")
        self.assertEqual(member.member_id, 1)

    def test_member_str(self):
        member = Member("Alice", 1)
        self.assertEqual(str(member), "Alice (ID: 1)")

if __name__ == '__main__':
    unittest.main()

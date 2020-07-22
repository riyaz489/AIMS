import unittest
from common.validations import Validation


class ValidationTest(unittest.TestCase):

    def test_is_phone(self):
        inputs = ['4534342312', '200', 'invalid_number', '123123qw12']
        self.assertEqual(True, Validation.is_phone(inputs[0]))
        self.assertEqual(False, Validation.is_phone(inputs[1]))
        self.assertEqual(False, Validation.is_phone(inputs[2]))
        self.assertEqual(False, Validation.is_phone(inputs[3]))

    def test_is_email(self):
        inputs = ['asd@gmai.com', '2020', 'invalid_id', 'asd.com']
        self.assertEqual(True, Validation.is_email(inputs[0]))
        self.assertEqual(False, Validation.is_email(inputs[1]))
        self.assertEqual(False, Validation.is_email(inputs[2]))
        self.assertEqual(False, Validation.is_email(inputs[3]))

    def test_password(self):
        inputs = ['Monty@123sgahRma', '1231', 'invalid_pass', '@#$%^^', 'ASDFDFGDG', 'sdf sdSASf', 'asASASAS',
                  'ASasd123213', 'Monty@123sgahRma asd']
        self.assertEqual(True, Validation.password(inputs[0]))
        self.assertEqual(False, Validation.password(inputs[1]))
        self.assertEqual(False, Validation.password(inputs[2]))
        self.assertEqual(False, Validation.password(inputs[3]))
        self.assertEqual(False, Validation.password(inputs[4]))
        self.assertEqual(False, Validation.password(inputs[5]))
        self.assertEqual(False, Validation.password(inputs[6]))
        self.assertEqual(False, Validation.password(inputs[7]))
        self.assertEqual(False, Validation.password(inputs[8]))


if __name__ == '__main__':
    unittest.main()

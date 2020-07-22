import unittest
import mock
from common.password_encryption import encrypt_pass, decrypt_pass


class PasswordEncrpytion(unittest.TestCase):

    @mock.patch('common.password_encryption.f.encrypt', return_value=b'dummy')
    def test_encrypt_pass(self, mock_encrypt):
        password = 'sample_password'
        result = encrypt_pass(password)
        mock_encrypt.assert_called_once()
        self.assertEqual('dummy', result)

    @mock.patch('common.password_encryption.f.decrypt', return_value=b'dummy')
    def test_decrypt_pass(self, mock_decrypt):
        result = decrypt_pass('sample_cipher')
        mock_decrypt.assert_called_once()
        self.assertEqual('dummy', result)


if __name__ == '__main__':
    unittest.main()

import unittest
from app.validators import *

class TestValidators(unittest.TestCase):

    # ////////////////////////////////////////////////////////////////////////////////////////////////////

    #TEST is_valid_name() function

    # Testing Valid names
    def test_valid_names(self):
        # Testing valid names within the given length constraints
        self.assertTrue(is_valid_name("Valid Name")) #pure char in range (default 1-100) with space
        self.assertTrue(is_valid_name("1234567890", 5, 20)) #pure int in range (not default 5 - 20)
        self.assertTrue(is_valid_name("a1-2d 3f4g5")) #mix char + int in range (default)
        # Test valid boundary length
        self.assertTrue(is_valid_name("a")) #range=1 (default)
        self.assertTrue(is_valid_name("dfasd--dafsdf 4535308DFEFBHFVf fgdf egjodfj fw3D0558f fcNbfgdfsg r85739204898f fdgdfgg s aq w xsDdfe")) #range=100 (default)
        self.assertTrue(is_valid_name("aBc ",length_from=4,length_to=6)) #range=4 (4-6)
        self.assertTrue(is_valid_name("a-c X1",length_from=4,length_to=6)) #range=4 (4-6)

    # Testing invalid names
    def test_invalid_names(self):
        #Test invalid boundary
        #min boundary
        self.assertFalse(is_valid_name(""))  # Empty name length = 0 (default)
        self.assertFalse(is_valid_name("aB ",4,6)) # length = 3 (4-6)
        self.assertFalse(is_valid_name("", 1, 50))  # Empty name length = 0 (1-50)
        #max boundary
        self.assertFalse(is_valid_name("dfasdfsdafsdf 4535308DFEFBHFVf fgdf egjodfj fw3d0558f fcnbfgdfsg r85739204898f fdgdfgg s aq w xsDdfeX"))  # Empty name length = 101 (default)
        self.assertFalse(is_valid_name("aB 4 67",4,6)) # length = 7 (4-6)
        #special character
        self.assertFalse(is_valid_name("Invalid!Name", 1, 100))  # Special characters
        self.assertFalse(is_valid_name("1.5"))  # Special characters (default)
        self.assertFalse(is_valid_name("P@s2w0rD", 1, 100))  # Special characters
        #edge case
        self.assertFalse(is_valid_name("A" * 1010))  # Too long (more than 1010 characters) (default)
        self.assertFalse(is_valid_name("a@:2" * 26))  # Too long + special characters (default)
        self.assertFalse(is_valid_name("a@:2" * 26,1,103))  # Too long + special characters
        self.assertFalse(is_valid_name("@@",3,18))  # Too short + special characters

    # ////////////////////////////////////////////////////////////////////////////////////////////////////

    #TEST is_valid_address() function

    # Testing Valid address
    def test_valid_address(self):
        # Testing valid names within the given length constraints
        self.assertTrue(is_valid_address("Valid Name")) #pure char in range (default 1-100) with space
        self.assertTrue(is_valid_address("1234567890", 5, 20)) #pure int in range (not default 5 - 20)
        self.assertTrue(is_valid_address("a1,-2d 3f,4g,5")) #mix char + int in range (default)
        # Test valid boundary length
        self.assertTrue(is_valid_address(",")) #range=1 (default)
        self.assertTrue(is_valid_address("dfasd--dafsdf 453,308DFEFf fgdf egjodfj fw3D05,8f fcNbfgdfsg r85739204898f fdgdfgg s aq w xsDdfedfasd--dafsdf 453,308DFEFBHFVf fgdf egjodfj fw3D05,8f fcNbfgdfsg r85739204898f fdgdfgg s aq w xsDdfedfasd--dafsdf 453,308DFEFBHFVf fgdf egjodfj fw3D05,8f fcNbfgdfsg r85739204898f fdgdfgg s aq w xsDdfedfasd--dafs,f 453,308DFEFBHFVf fgdf egjodfj fw3D05,8f fcNbfgdfsg r85739204898f fdgdfgg s aq w xsDdfe3")) #range=401 (default)
        self.assertTrue(is_valid_address("aB, ",length_from=4,length_to=6)) #range=4 (4-6)
        self.assertTrue(is_valid_address("a-c X1",length_from=4,length_to=6)) #range=4 (4-6)
    
    # Testing invalid address
    def test_invalid_names(self):
        #Test invalid boundary
        #min boundary
        self.assertFalse(is_valid_address(""))  # Empty name length = 0 (default)
        self.assertFalse(is_valid_address(",4 ",4,6)) # length = 3 (4-6)
        self.assertFalse(is_valid_address("", 1, 50))  # Empty name length = 0 (1-50)
        #max boundary
        self.assertFalse(is_valid_address("dfasd--dafsdf 453,308DFEFBHFVf fgdf egjodfj fw3D05,8f fcNbfgdfsg r85739204898f fdgdfgg s aq w xsDdfedfasd--dafsdf 453,308DFEFBHFVf fgdf egjodfj fw3D05,8f fcNbfgdfsg r85739204898f fdgdfgg s aq w xsDdfedfasd--dafsdf 453,308DFEFBHFVf fgdf egjodfj fw3D05,8f fcNbfgdfsg r85739204898f fdgdfgg s aq w xsDdfedfasd--dafs,f 453,308DFEFBHFVf fgdf egjodfj fw3D05,8f fcNbfgdfsg r85739204898f fdgdfgg s aq w xsDdfe3"))  # Empty name length = 401 (default)
        self.assertFalse(is_valid_address("aB 4 67",4,6)) # length = 7 (4-6)
        #special character
        self.assertFalse(is_valid_address("Invalid!Name", 1, 100))  # Special characters
        self.assertFalse(is_valid_address("1.5"))  # Special characters (default)
        self.assertFalse(is_valid_address("P@s2w0rD", 1, 100))  # Special characters
        #edge case
        self.assertFalse(is_valid_address("A" * 1010))  # Too long (more than 1010 characters) (default)
        self.assertFalse(is_valid_address("a@:," * 26))  # Too long + special characters (default)
        self.assertFalse(is_valid_address("a@:2" * 26,1,103))  # Too long + special characters
        self.assertFalse(is_valid_address(" @",3,18))  # Too short + special characters

    # ////////////////////////////////////////////////////////////////////////////////////////////////////

    #TEST is_valid_salary() function

    def test_valid_salaries(self):
        self.assertTrue(is_valid_salary(50000)) #interger
        self.assertTrue(is_valid_salary(999.99)) #float 2
        self.assertTrue(is_valid_salary(1000.0)) #float 1
        self.assertTrue(is_valid_salary(0.001)) #float 1 boundary

    def test_invalid_salaries(self):
        self.assertFalse(is_valid_salary(-1000))  # Negative salary
        self.assertFalse(is_valid_salary("50000"))  # Not a number (string)
        self.assertFalse(is_valid_salary(0))  # Salary must be greater than 0 boundary
        self.assertFalse(is_valid_salary(None))  # None type

    # ////////////////////////////////////////////////////////////////////////////////////////////////////

    #TEST is_valid_url() function

    # New Tests for is_valid_url
    def test_valid_urls(self):
        self.assertTrue(is_valid_url("http://www.example.com"))
        self.assertTrue(is_valid_url("https://www.example.com"))
        self.assertTrue(is_valid_url("http://localhost:8000"))
        self.assertTrue(is_valid_url("http://192.168.0.1"))

    def test_invalid_urls(self):
        self.assertFalse(is_valid_url("htp://invalid-url"))  # Invalid protocol
        self.assertFalse(is_valid_url("http://example"))  # Missing top-level domain
        self.assertFalse(is_valid_url("www.example.com"))  # Missing protocol
        self.assertFalse(is_valid_url("http://"))  # Incomplete URL
        self.assertFalse(is_valid_url("http://" + "a" * 2000 + ".com"))  # Exceeds length limit


if __name__ == '__main__':
    unittest.main()

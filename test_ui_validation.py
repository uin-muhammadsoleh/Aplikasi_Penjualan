import unittest
from streamlit.testing.v1 import AppTest


class TestStreamlitAppValidation(unittest.TestCase):
    def test_app_loads(self):
        at = AppTest.from_file("app.py", default_timeout=10)
        at.run()
        self.assertFalse(at.exception)

    def test_auth_login_empty_input_warning(self):
        at = AppTest.from_file("app.py", default_timeout=10)
        at.run()
        # Form login is on the first tab
        # Click login without typing username and password
        form_login = at.form[0]
        form_login.submit().run()
        # Should render errors
        self.assertGreater(len(at.error), 0)

    def test_auth_register_validation(self):
        at = AppTest.from_file("app.py", default_timeout=10)
        at.run()
        # Form register is at.form[1]
        form_register = at.form[1]
        # Fill mismatch passwords
        at.text_input(key="reg_nama").set_value("A").run()
        form_register.submit().run()
        self.assertGreater(len(at.error), 0)


if __name__ == "__main__":
    unittest.main()

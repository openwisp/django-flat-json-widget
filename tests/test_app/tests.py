from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from openwisp_utils.tests.selenium import SeleniumTestMixin
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .models import JsonDocument

ADD_ROW_BUTTON = "flat-json-add-row"
REMOVE_ROW_BUTTON = "flat-json-remove-row"
SAVE_BUTTON = ".submit-row .default"
TOGGLE_TEXTAREA_BUTTON = "flat-json-toggle-textarea"
TEST_JSON_CONTENT = {
    "first_key": "first_val",
    "second_key": "second_val",
    "third_key": "third_val",
}


class FrontendTests(SeleniumTestMixin, StaticLiveServerTestCase):
    """Functional tests for the flat JSON widget in Django admin using Selenium"""

    def _create_admin(self, username, password):
        User = get_user_model()
        return User.objects.create_superuser(
            username,
            "admin@admin.com",
            password,
        )

    # Overriding open() and _wait_until_page_ready() so that #main
    # is used instead of #main-content as CSS selector.
    def open(self, url, html_container="#main", driver=None, timeout=5):
        driver = driver or self.web_driver
        driver.get(f"{self.live_server_url}{url}")
        self._wait_until_page_ready(driver=driver, html_container=html_container)

    def _wait_until_page_ready(self, html_container="#main", timeout=5, driver=None):
        driver = driver or self.web_driver
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        self.wait_for_visibility(By.CSS_SELECTOR, html_container, timeout, driver)

    def test_add_row(self):
        """This test checks whether the add-row button works properly."""

        self.login()
        self.open("/admin/test_app/jsondocument/add")
        self.find_element(By.CLASS_NAME, ADD_ROW_BUTTON).click()
        self.wait_for_visibility(By.CSS_SELECTOR, ".flat-json-rows .form-row")
        rows = self.find_elements(By.CSS_SELECTOR, ".flat-json-rows .form-row")
        self.assertEqual(len(rows), 1)
        self.find_element(By.CSS_SELECTOR, ".field-name input").send_keys("TestJson")
        rows[0].find_element(By.CLASS_NAME, "flat-json-key").send_keys("test_key")
        rows[0].find_element(By.CLASS_NAME, "flat-json-value").send_keys("test_value")
        self.find_element(By.CSS_SELECTOR, SAVE_BUTTON).click()
        self.wait_for_presence(By.CSS_SELECTOR, ".messagelist .success")
        json = JsonDocument.objects.first()
        self.assertEqual(len(json.content), 1, "Expected 1 row")
        self.assertEqual(json.name, "TestJson")
        self.assertEqual(
            json.content,
            {"test_key": "test_value"},
        )

    def test_remove_row(self):
        """This test checks whether the remove-row button removes the desired row"""

        json_doc = JsonDocument.objects.create(
            name="test_json", content=TEST_JSON_CONTENT
        )
        self.login()
        self.open(f"/admin/test_app/jsondocument/{json_doc.pk}/change")
        self.wait_for_visibility(By.CLASS_NAME, "flat-json-remove-row")
        remove_buttons = self.find_elements(By.CLASS_NAME, REMOVE_ROW_BUTTON)
        second_row_remove_btn = remove_buttons[1]
        second_row_remove_btn.click()
        rows = self.find_elements(By.CSS_SELECTOR, ".flat-json-rows .form-row")
        self.assertEqual(
            len(rows), 2, "Error in display: Expected 2 rows after removing one"
        )
        self.find_element(By.CSS_SELECTOR, SAVE_BUTTON).click()
        self.wait_for_presence(By.CSS_SELECTOR, ".messagelist .success")
        json = JsonDocument.objects.first().content
        self.assertEqual(
            len(json), 2, "Error in saving: Expected 2 rows after removing one."
        )
        self.assertEqual(
            json,
            {
                "first_key": "first_val",
                "third_key": "third_val",
            },
        )

    def test_toggle_textarea(self):
        """Tests whether the toggle button toggles between widgets and textarea"""

        self.login()
        self.open("/admin/test_app/jsondocument/add/")
        toggle_btn = self.find_element(By.CLASS_NAME, TOGGLE_TEXTAREA_BUTTON)
        toggle_btn.click()
        self.wait_for_invisibility(By.CLASS_NAME, "flat-json-rows")
        self.wait_for_invisibility(By.CLASS_NAME, ADD_ROW_BUTTON)
        self.wait_for_visibility(By.CLASS_NAME, "flat-json-textarea")

    def test_edit_json_from_textarea(self):
        """Tests whether changes made in textarea updates the json document."""

        json_doc = JsonDocument.objects.create(
            name="test_json", content=TEST_JSON_CONTENT
        )
        self.login()
        self.open(f"/admin/test_app/jsondocument/{json_doc.pk}/change")
        toggle_btn = self.find_element(By.CLASS_NAME, TOGGLE_TEXTAREA_BUTTON)
        toggle_btn.click()
        textarea = self.find_element(By.CSS_SELECTOR, ".flat-json-textarea textarea")
        self.assertEqual(
            textarea.get_attribute("value"),
            '{"first_key": "first_val", '
            '"second_key": "second_val", '
            '"third_key": "third_val"}',
        )
        textarea.clear()
        textarea.send_keys('{"first_key": "first_val", "second_key": "second_val"}')
        save_btn = self.find_element(By.CSS_SELECTOR, SAVE_BUTTON)
        save_btn.click()
        self.assertEqual(
            JsonDocument.objects.first().content,
            {
                "first_key": "first_val",
                "second_key": "second_val",
            },
        )

    def test_textarea_edit_updates_widget(self):
        """Tests whether the changes made in textarea is visible in widget mode"""

        self.login()
        self.open("/admin/test_app/jsondocument/add")
        textarea_toggle_btn = self.find_element(By.CLASS_NAME, TOGGLE_TEXTAREA_BUTTON)
        textarea_toggle_btn.click()
        textarea = self.find_element(By.CSS_SELECTOR, ".flat-json-textarea textarea")
        textarea.clear()
        textarea.send_keys('{"key": "value"}')
        textarea_toggle_btn.click()
        key = self.find_element(By.CLASS_NAME, "flat-json-key").get_attribute("value")
        val = self.find_element(By.CLASS_NAME, "flat-json-value").get_attribute("value")
        self.assertEqual((key, val), ("key", "value"))

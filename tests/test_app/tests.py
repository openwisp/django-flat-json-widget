from time import sleep

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from openwisp_utils.tests.selenium import SeleniumTestMixin
from selenium.webdriver.common.by import By

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
        super().open(url, html_container, driver, timeout)

    def _wait_until_page_ready(self, html_container="#main", timeout=5, driver=None):
        super()._wait_until_page_ready(html_container, timeout, driver)

    def scroll_and_click(self, element):
        """Scrolls element into view and clicks it"""
        self.web_driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element,
        )
        element.click()

    def test_add_row(self):
        """This test checks whether the add-row button works properly."""

        self.login()
        self.open(reverse("admin:test_app_jsondocument_add"))
        self.wait_for_presence(By.CLASS_NAME, ADD_ROW_BUTTON)
        add_row_btn = self.find_element(By.CLASS_NAME, ADD_ROW_BUTTON)
        self.scroll_and_click(add_row_btn)
        self.wait_for_presence(By.CSS_SELECTOR, ".flat-json-rows .form-row")
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
        self.open(reverse("admin:test_app_jsondocument_change", args=[json_doc.pk]))
        self.wait_for_presence(By.CLASS_NAME, "flat-json-remove-row")
        remove_buttons = self.find_elements(By.CLASS_NAME, REMOVE_ROW_BUTTON)
        second_row_remove_btn = remove_buttons[1]
        sleep(0.25)  # workaround for random CI failures
        self.scroll_and_click(second_row_remove_btn)
        rows = self.find_elements(By.CSS_SELECTOR, ".flat-json-rows .form-row")
        self.assertEqual(
            len(rows), 2, "Error in display: Expected 2 rows after removing one"
        )
        save_btn = self.find_element(By.CSS_SELECTOR, SAVE_BUTTON)
        self.scroll_and_click(save_btn)
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
        self.open(reverse("admin:test_app_jsondocument_add"))
        self.wait_for_presence(By.CLASS_NAME, TOGGLE_TEXTAREA_BUTTON)
        toggle_btn = self.find_element(By.CLASS_NAME, TOGGLE_TEXTAREA_BUTTON)
        self.scroll_and_click(toggle_btn)
        textarea = self.find_element(By.CLASS_NAME, "flat-json-textarea")
        flat_json_rows = self.find_element(
            By.CLASS_NAME, "flat-json-rows", wait_for="presence"
        )
        add_row_btn = self.find_element(
            By.CLASS_NAME, ADD_ROW_BUTTON, wait_for="presence"
        )
        self.assertFalse(flat_json_rows.is_displayed())
        self.assertFalse(add_row_btn.is_displayed())
        self.assertIsNotNone(textarea)

    def test_edit_json_from_textarea(self):
        """Tests whether changes made in textarea updates the json document."""

        json_doc = JsonDocument.objects.create(
            name="test_json", content=TEST_JSON_CONTENT
        )
        self.login()
        self.open(reverse("admin:test_app_jsondocument_change", args=[json_doc.pk]))
        self.wait_for_presence(By.CLASS_NAME, TOGGLE_TEXTAREA_BUTTON)
        toggle_btn = self.find_element(By.CLASS_NAME, TOGGLE_TEXTAREA_BUTTON)
        self.scroll_and_click(toggle_btn)
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
        self.scroll_and_click(save_btn)
        self.wait_for_presence(By.CSS_SELECTOR, ".messagelist .success")
        json = JsonDocument.objects.first().content
        self.assertEqual(
            json,
            {
                "first_key": "first_val",
                "second_key": "second_val",
            },
        )

    def test_textarea_edit_updates_widget(self):
        """Tests whether the changes made in textarea is visible in widget mode"""

        self.login()
        self.open(reverse("admin:test_app_jsondocument_add"))
        self.wait_for_presence(By.CLASS_NAME, TOGGLE_TEXTAREA_BUTTON)
        textarea_toggle_btn = self.find_element(By.CLASS_NAME, TOGGLE_TEXTAREA_BUTTON)
        self.scroll_and_click(textarea_toggle_btn)
        textarea = self.find_element(By.CSS_SELECTOR, ".flat-json-textarea textarea")
        textarea.clear()
        textarea.send_keys('{"key": "value"}')
        self.scroll_and_click(textarea_toggle_btn)
        key = self.find_element(By.CLASS_NAME, "flat-json-key").get_attribute("value")
        val = self.find_element(By.CLASS_NAME, "flat-json-value").get_attribute("value")
        self.assertEqual((key, val), ("key", "value"))

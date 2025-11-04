"""
Base Page Object Model - Parent class for all page objects.
"""
from playwright.sync_api import Page, Locator, expect
from typing import Optional
#... other required imports
import logging

class BasePage:
    """Base page class with common methods for all pages."""
    
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging #this need to be fine tuned
    
    def navigate(self, path: str = "/") -> None:
        """
        Navigate to a specific path.
        
        Args:
            path: URL path to navigate to (default: "/")
        """
        url = f"{config.base_url}{path}"
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url, timeout=config.navigation_timeout)
        self.wait_for_page_load()
    
    def wait_for_page_load(self) -> None:
        """Wait for page to fully load."""
        self.page.wait_for_load_state("networkidle", timeout=config.navigation_timeout)
        self.logger.debug("Page loaded successfully")
    
    def click_element(self, locator: Locator, description: str = "") -> None:
        """
        Click an element with logging.
        
        Args:
            locator: Playwright locator object
            description: Description of element being clicked
        """
        self.logger.info(f"Clicking element: {description or locator}")
        locator.click(timeout=config.action_timeout)
    
    def fill_input(self, locator: Locator, text: str, description: str = "") -> None:
        """
        Fill input field with text.
        
        Args:
            locator: Playwright locator object
            text: Text to fill
            description: Description of input field
        """
        self.logger.info(f"Filling input '{description}' with: {text}")
        locator.fill(text, timeout=config.action_timeout)
    
    def get_text(self, locator: Locator) -> str:
        """
        Get text content of an element.
        
        Args:
            locator: Playwright locator object
            
        Returns:
            Text content of the element
        """
        text = locator.text_content(timeout=config.action_timeout)
        self.logger.debug(f"Retrieved text: {text}")
        return text or ""
    
    def get_element_count(self, locator: Locator) -> int:
        """
        Get count of elements matching locator.
        
        Args:
            locator: Playwright locator object
            
        Returns:
            Number of matching elements
        """
        count = locator.count()
        self.logger.debug(f"Element count: {count}")
        return count
    
    def is_visible(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        """
        Check if element is visible.
        
        Args:
            locator: Playwright locator object
            timeout: Custom timeout in milliseconds
            
        Returns:
            True if visible, False otherwise
        """
        try:
            locator.wait_for(state="visible", timeout=timeout or config.action_timeout)
            return True
        except Exception:
            return False
    
    def is_enabled(self, locator: Locator) -> bool:
        """
        Check if element is enabled.
        
        Args:
            locator: Playwright locator object
            
        Returns:
            True if enabled, False otherwise
        """
        return locator.is_enabled()
    
    def take_screenshot(self, name: str) -> str:
        """
        Take screenshot and save to reports.
        
        Args:
            name: Screenshot filename (without extension)
            
        Returns:
            Path to saved screenshot
        """
        screenshot_path = config.screenshots_dir / f"{name}.png"
        self.page.screenshot(path=str(screenshot_path))
        self.logger.info(f"Screenshot saved: {screenshot_path}")
        return str(screenshot_path)
    
    def wait_for_element(self, locator: Locator, state: str = "visible", timeout: Optional[int] = None) -> None:
        """
        Wait for element to reach specific state.
        
        Args:
            locator: Playwright locator object
            state: State to wait for (visible, hidden, attached, detached)
            timeout: Custom timeout in milliseconds
        """
        self.logger.debug(f"Waiting for element to be {state}")
        locator.wait_for(state=state, timeout=timeout or config.action_timeout)
    
    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.page.url
    
    def reload_page(self) -> None:
        """Reload the current page."""
        self.logger.info("Reloading page")
        self.page.reload()

"""
API request/response interceptor and validator.
"""
from playwright.sync_api import Page, Route, Request, Response
from typing import List, Dict, Any, Optional
from utils.logger import test_logger
import json


class APIInterceptor:
    """Intercept and validate API requests/responses."""
    
    def __init__(self):
        self.logger = test_logger
        self.requests: List[Dict[str, Any]] = []
        self.responses: List[Dict[str, Any]] = []
    
    def setup_interception(self, page: Page, url_pattern: str = "**/api.themoviedb.org/**") -> None:
        """
        Setup API interception for specific URL pattern.
        
        Args:
            page: Playwright page object
            url_pattern: URL pattern to intercept
        """
        self.logger.info(f"Setting up API interception for: {url_pattern}")
        
        page.route(url_pattern, self._handle_route)
    
    def _handle_route(self, route: Route) -> None:
        """
        Handle intercepted route.
        
        Args:
            route: Playwright route object
        """
        request = route.request
        
        # Capture request details
        request_data = {
            "url": request.url,
            "method": request.method,
            "headers": request.headers,
            "post_data": request.post_data,
            "timestamp": self._get_timestamp()
        }
        self.requests.append(request_data)
        self.logger.debug(f"Captured request: {request.method} {request.url}")
        
        # Continue request and capture response
        response = route.fetch()
        
        # Capture response details
        try:
            body = response.text()
            response_data = {
                "url": request.url,
                "status": response.status,
                "status_text": response.status_text,
                "headers": response.headers,
                "body": body,
                "timestamp": self._get_timestamp()
            }
            self.responses.append(response_data)
            self.logger.debug(f"Captured response: {response.status} {request.url}")
        except Exception as e:
            self.logger.error(f"Error capturing response: {str(e)}")
        
        # Fulfill the route with original response
        route.fulfill(response=response)
    
    def get_requests(self, filter_url: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all captured requests, optionally filtered by URL.
        
        Args:
            filter_url: Optional URL substring to filter by
            
        Returns:
            List of request dictionaries
        """
        if filter_url:
            return [req for req in self.requests if filter_url in req["url"]]
        return self.requests
    
    def get_responses(self, filter_url: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all captured responses, optionally filtered by URL.
        
        Args:
            filter_url: Optional URL substring to filter by
            
        Returns:
            List of response dictionaries
        """
        if filter_url:
            return [resp for resp in self.responses if filter_url in resp["url"]]
        return self.responses
    
    def get_last_request(self) -> Optional[Dict[str, Any]]:
        """Get the most recent request."""
        return self.requests[-1] if self.requests else None
    
    def get_last_response(self) -> Optional[Dict[str, Any]]:
        """Get the most recent response."""
        return self.responses[-1] if self.responses else None
    
    def validate_request_contains(self, url_substring: str, expected_params: Dict[str, Any]) -> bool:
        """
        Validate that a request contains expected parameters.
        
        Args:
            url_substring: Substring to identify the request
            expected_params: Expected parameters in URL
            
        Returns:
            True if validation passes, False otherwise
        """
        matching_requests = self.get_requests(filter_url=url_substring)
        
        if not matching_requests:
            self.logger.error(f"No requests found matching: {url_substring}")
            return False
        
        last_request = matching_requests[-1]
        url = last_request["url"]
        
        for param, value in expected_params.items():
            if f"{param}={value}" not in url:
                self.logger.error(f"Expected parameter not found: {param}={value}")
                return False
        
        self.logger.info(f"Request validation passed for: {url_substring}")
        return True
    
    def validate_response_status(self, url_substring: str, expected_status: int) -> bool:
        """
        Validate response status code.
        
        Args:
            url_substring: Substring to identify the response
            expected_status: Expected HTTP status code
            
        Returns:
            True if validation passes, False otherwise
        """
        matching_responses = self.get_responses(filter_url=url_substring)
        
        if not matching_responses:
            self.logger.error(f"No responses found matching: {url_substring}")
            return False
        
        last_response = matching_responses[-1]
        actual_status = last_response["status"]
        
        if actual_status != expected_status:
            self.logger.error(f"Status mismatch. Expected: {expected_status}, Actual: {actual_status}")
            return False
        
        self.logger.info(f"Response status validation passed: {expected_status}")
        return True
    
    def validate_response_json_schema(self, url_substring: str, expected_keys: List[str]) -> bool:
        """
        Validate that response JSON contains expected keys.
        
        Args:
            url_substring: Substring to identify the response
            expected_keys: List of expected keys in JSON response
            
        Returns:
            True if validation passes, False otherwise
        """
        matching_responses = self.get_responses(filter_url=url_substring)
        
        if not matching_responses:
            self.logger.error(f"No responses found matching: {url_substring}")
            return False
        
        last_response = matching_responses[-1]
        
        try:
            response_json = json.loads(last_response["body"])
            
            for key in expected_keys:
                if key not in response_json:
                    self.logger.error(f"Expected key not found in response: {key}")
                    return False
            
            self.logger.info("Response JSON schema validation passed")
            return True
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON response: {str(e)}")
            return False
    
    def clear_history(self) -> None:
        """Clear all captured requests and responses."""
        self.requests.clear()
        self.responses.clear()
        self.logger.info("API interception history cleared")
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()

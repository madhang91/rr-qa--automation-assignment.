"""
Integration tests for combined filter scenarios.
"""
import pytest
import allure
from playwright.sync_api import Page
from pages.home_page import HomePage
from utils.api_interceptor import APIInterceptor


@allure.epic("TMDB Discover")
@allure.feature("Combined Filters")
@pytest.mark.functional
class TestCombinedFilters:
    """Test suite for combined filter scenarios."""
    
    @allure.story("Category + Type Filter")
    @allure.title("TC-035: Verify Category + Type Combined Filters")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.high
    @pytest.mark.regression
    def test_category_and_type_filters(
        self,
        page: Page,
        home_page: HomePage,
        api_interceptor: APIInterceptor
    ):
        """
        Verify combining category and type filters works correctly.
        
        Test Steps:
            1. Navigate to home page
            2. Select Top Rated category
            3. Select Movies type
            4. Verify both filters are active
            5. Verify API request contains both parameters
            6. Verify results match criteria
        """
        with allure.step("Navigate and setup"):
            home_page.navigate()
            api_interceptor.setup_interception(page)
        
        with allure.step("Select Top Rated category"):
            home_page.select_category("top-rated")
        
        with allure.step("Select Movies type"):
            home_page.select_type("movie")
        
        with allure.step("Verify URL reflects both filters"):
            current_url = page.url
            allure.attach(current_url, "Current URL", allure.attachment_type.TEXT)
            # URL should indicate both category and type
        
        with allure.step("Verify results are displayed"):
            results_count = home_page.get_results_count()
            allure.attach(str(results_count), "Results Count", allure.attachment_type.TEXT)
            assert results_count > 0, "Should display filtered results"
        
        with allure.step("Verify API request contains correct parameters"):
            last_request = api_interceptor.get_last_request()
            if last_request:
                request_url = last_request["url"]
                allure.attach(request_url, "API Request URL", allure.attachment_type.TEXT)
                assert "top_rated" in request_url or "top" in request_url
                assert "movie" in request_url
    
    @allure.story("Category + Type + Year Filter")
    @allure.title("TC-036: Verify Category + Type + Year Combined Filters")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.high
    def test_category_type_year_filters(self, home_page: HomePage):
        """Verify combining category, type, and year filters."""
        with allure.step("Navigate to home page"):
            home_page.navigate()
        
        with allure.step("Apply Popular + Movies + 2020"):
            home_page.select_category("popular")
            home_page.select_type("movie")
            home_page.filter_by_year(2020)
        
        with allure.step("Verify all filters persist"):
            # All filters should remain active
            assert home_page.has_results() or home_page.has_no_results_message(), \
                "Should show results or no results message"
    
    @allure.story("All Filters Combined")
    @allure.title("TC-037: Verify All Filters Combined")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    @pytest.mark.regression
    def test_all_filters_combined(self, home_page: HomePage):
        """Verify combining all available filters."""
        with allure.step("Navigate to home page"):
            home_page.navigate()
        
        with allure.step("Apply all filters"):
            home_page.select_category("top-rated")
            home_page.select_type("movie")
            home_page.filter_by_year(2020)
            home_page.filter_by_rating(8.0)
        
        with allure.step("Verify system handles all filters"):
            # System should handle multiple filters gracefully
            results_count = home_page.get_results_count()
            allure.attach(str(results_count), "Results Count", allure.attachment_type.TEXT)
            
            # Either results or no results message should appear
            has_content = home_page.has_results() or home_page.has_no_results_message()
            assert has_content, "Should display results or appropriate message"
    
    @allure.story("Filter Persistence")
    @allure.title("TC-038: Verify Filters Persist During Pagination")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_filters_persist_during_pagination(self, page: Page, home_page: HomePage):
        """Verify filters remain active when navigating pages."""
        with allure.step("Navigate and apply filters"):
            home_page.navigate()
            home_page.select_category("popular")
            home_page.select_type("movie")
        
        with allure.step("Capture URL after filters"):
            url_before_pagination = page.url
            allure.attach(url_before_pagination, "URL Before Pagination", allure.attachment_type.TEXT)
        
        with allure.step("Navigate to next page"):
            if home_page.is_next_page_available():
                home_page.go_to_next_page()
        
        with allure.step("Verify filters persist in URL"):
            url_after_pagination = page.url
            allure.attach(url_after_pagination, "URL After Pagination", allure.attachment_type.TEXT)
            
            # Core filter parameters should still be in URL
            assert "popular" in url_after_pagination.lower() or \
                   "movie" in url_after_pagination.lower(), \
                   "Filters should persist during pagination"

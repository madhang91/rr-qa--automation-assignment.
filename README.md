# rr-qa--automation-assignment.
This is a test assignment repo

## **Testing Strategy**

### **Test Coverage**
- **Total Test Cases:** 55+
  - 40 Functional tests
  - 15 Negative/Edge case tests
- **Browsers:** Chromium, Firefox, WebKit

### **Test Design Techniques**
1. ✅ **Equivalence Partitioning** - Year ranges, rating values
2. ✅ **Boundary Value Analysis** - Min/max years (1900-2026), ratings (0-10)
3. ✅ **Decision Table Testing** - Filter combinations
4. ✅ **State Transition** - Navigation flows
5. ✅ **Error Guessing** - Known issues (slug URLs, pagination limits)

### **Features Tested**
- ✅ Category Filters (Popular, Trending, Newest, Top Rated)
- ✅ Type Selection (Movies vs TV Shows)
- ✅ Year Filtering (with boundary testing)
- ✅ Rating Filtering
- ✅ Genre Selection
- ✅ Pagination (including edge cases)
- ✅ Combined Filter Scenarios
- ✅ API Request/Response Validation
- ✅ Browser Console Error Monitoring

### **Known Defects Tested**
- ❌ **DEF-001:** Direct slug URL navigation fails
- ❌ **DEF-002:** Last pagination pages broken

---

## 🚀 **Setup & Installation**

### **Prerequisites**
- Python 3.10 or higher
- pip (Python package manager)
- Git

### **Installation Steps**
1. Clone repository
git clone <repository-url>
cd tmdb-test-automation

2. Create virtual environment (recommended)
python -m venv venv

Activate virtual environment:
Windows:
venv\Scripts\activate

macOS/Linux:
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt (this is to be defined when the complete project is done)

4. Install Playwright browsers
playwright install

Or install specific browser:
playwright install chromium


## ▶️ **Running Tests**

### **All Tests (Default)**
pytest

### **Specific Test Categories**
Functional tests only
pytest tests/functional -v

Negative tests only
pytest tests/negative -v

API validation tests
pytest tests/api -v

Run by markers
pytest -m smoke # Smoke tests
pytest -m high # High priority tests
pytest -m regression # Full regression suite


### **Browser Selection**
Specific browser
pytest --browser=chromium
pytest --browser=firefox
pytest --browser=webkit

### **With Detailed Reporting**
pytest -v --html=reports/html/report.html --self-contained-html


## 📊 **Viewing Reports**

### **1. HTML Report (Pytest-HTML)**
Report auto-generated at:
reports/html/report.html

Open in browser:
reports/html/report.html


**Features:**
- Test pass/fail summary
- Execution time
- Failure screenshots (automatically attached)
- Console logs

Alternatively we can opt for allure as well.

### **3. Console Output**
Real-time test results displayed in terminal during execution.

### **4. Logs**
All logs
cat reports/logs/test_execution.log

Errors only
cat reports/logs/errors.log

## 📝 **Logging**

The framework uses **Loguru** for comprehensive logging.

**Log Levels:**
- `DEBUG` - Detailed diagnostic information
- `INFO` - General informational messages
- `WARNING` - Warning messages
- `ERROR` - Error messages with stack traces

**Log Locations:**
- `reports/logs/test_execution.log` - All logs (DEBUG level)
- `reports/logs/errors.log` - Errors only
- Console - INFO level (color-coded)

## 🏗️ **Design Patterns & Architecture**

### **1. Page Object Model (POM)**
Separation of test logic and page interactions.

pages/home_page.py
class HomePage(BasePage):
def select_category(self, category):
"""Select category filter."""
# Implementation

tests/functional/test_category_filters.py
def test_popular_category(home_page):
home_page.select_category("popular")
assert home_page.get_results_count() > 0


## 🔧 **Configuration**

### **Environment Variables**
Create `.env` file for custom configuration:

BASE_URL=https://tmdb-discover.surge.sh
BROWSER=chromium
HEADLESS=true
PARALLEL_WORKERS=4

### **Command Line Override**
pytest --browser=firefox --headed

### **pytest.ini**
Core pytest configuration in `pytest.ini` file.

---

## 🔄 **CI/CD Integration**

### **GitHub Actions Pipeline**

The framework includes a complete CI/CD pipeline (`.github/workflows/ci-tests.yml`).

**Pipeline Stages:**
1. ✅ Code checkout
2. ✅ Python & dependency setup
3. ✅ Multi-browser parallel execution
4. ✅ Report generation (HTML / Allure)
5. ✅ Artifact upload (reports, screenshots, logs)
6. ✅ GitHub Pages deployment (Allure report)
7. ✅ Slack notifications

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests
- Daily scheduled run (2 AM UTC)
- Manual workflow dispatch

**Viewing CI Results:**
- GitHub Actions tab in repository
- Allure report: `https://YOUR_USERNAME.github.io/tmdb-test-automation`
- Download artifacts from Actions run

## 🐛 **Known Issues & Defects**

### **DEF-001: Direct Slug URL Navigation Fails**
- **Severity:** High
- **Status:** Open (Known Issue)
- **Impact:** Users cannot bookmark/share category URLs
- **Test Cases:** TC-ID XX
- **Workaround:** Navigate via UI, not direct URL

### **DEF-002: Last Pagination Pages Broken**
- **Severity:** Medium
- **Status:** Open (Known Issue)
- **Impact:** Poor UX on last few pages
- **Test Cases:** TC-ID XX
- **Behavior:** Loading spinner hangs or empty results

**Detailed defect reports with screenshots available in:**
- `reports/defects/` directory (post-execution)
- Allure report (Defects section)

---

## 📚 **Framework Libraries**

| Library | Version | Purpose |
|---------|---------|---------|
| pytest | 7.4.3 | Test framework |
| playwright | 1.40.0 | Browser automation |
| pytest-html | 4.1.1 | HTML reporting |
| faker | 20.1.0 | Test data generation |

---

## 📈 **Test Metrics & Quality Gates**

**Success Criteria:**
- ✅ Functional tests: ≥95% pass rate
- ✅ Negative tests: 100% (expected failures marked with `xfail`)
- ✅ Execution time: <10 minutes (full suite)
- ✅ Critical console errors: <5

**CI/CD Quality Gates:**
- ❌ Block merge if functional tests <90%
- ❌ Fail build on new critical defects
- ✅ Auto-create GitHub issues for failures

## 🙏 **Acknowledgments**

- TMDB API for demo application
- Playwright team for excellent Python bindings
- Pytest community for robust testing framework
- Allure team for beautiful reporting

---

**Last Updated:** November 2025  
**Framework Version:** 1.0.0  
**Python Version:** 3.11+  
**Playwright Version:** 1.40.0
📦 DELIVERABLE 17: How to Run Commands Summary
Create a file QUICK_START.md:

# Quick Start Guide

## Installation (One-Time Setup)
Install Python dependencies
pip install -r requirements.txt

Install Playwright browsers
playwright install

## Running Tests

### Basic Execution
All tests
pytest

With detailed output
pytest -v

Specific test file
pytest tests/functional/test_category_filters.py

Specific test function
pytest tests/functional/test_category_filters.py::TestCategoryFilters::test_popular_category_filter


### Browser Selection
pytest --browser=chromium
pytest --browser=firefox --headed # See browser UI

### Test Categories
pytest tests/functional # Positive scenarios
pytest tests/negative # Known bugs & edge cases
pytest tests/api # API validation
pytest -m smoke # Smoke tests only
pytest -m high # High priority only


### Generate Reports
HTML report
pytest --html=reports/html/my-report.html --self-contained-html

## Viewing Results
Open HTML report
open reports/html/report.html

Check logs
tail -f reports/logs/test_execution.log


## Debugging
Run in headed mode with verbose output
pytest -v --headed --browser=chromium tests/functional/test_category_filters.py

Run single test
pytest -v --headed tests/functional/test_category_filters.py::TestCategoryFilters::test_popular_category_filter



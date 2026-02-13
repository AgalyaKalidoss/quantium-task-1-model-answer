# test_app.py
import pytest
from dash.testing.application_runners import import_app
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def dash_app():
    # Setup Chrome options for headless testing
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Start driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    # Import the Dash app
    app = import_app("app")  # your app.py filename without .py
    from dash.testing.application_runners import DashThreaded
    dash_server = DashThreaded(app)
    dash_server.start()
    
    yield driver, dash_server
    driver.quit()
    dash_server.stop()

# --- Test 1: Check header exists ---
def test_header_present(dash_app):
    driver, server = dash_app
    driver.get(server.url)
    header = driver.find_element("tag name", "h1")
    assert "Pink Morsels Sales Visualiser" in header.text

# --- Test 2: Check graph is present ---
def test_graph_present(dash_app):
    driver, server = dash_app
    driver.get(server.url)
    graph = driver.find_element("id", "sales-line-chart")
    assert graph is not None

# --- Test 3: Check region picker is present ---
def test_region_picker_present(dash_app):
    driver, server = dash_app
    driver.get(server.url)
    region_picker = driver.find_element("id", "region-selector")
    assert region_picker is not None

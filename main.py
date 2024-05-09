import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import time

# Keywords to search for in lowercase
keywords = [
    "ai", "asset", "backup", "ci/cd", "cloud",
    "debugging", "devops", "devtool", "elt", "finops", "idp", "infrastructure", "integration",
    "kubernetes", "llm", "ml", "monitoring", "operations", "orchestration", "pipelines", "platform",
    "response", "saas", "scaling", "security", "services", "snowflake", "storage", "terraform",
    "testing", "workflow", "analytics", "architecture", "automation", "cluster",
    "containerization", "deployment", "development", "engineering", "governance", "hosting",
    "learning", "management", "migration", "microservices", "networking", "observability",
    "recovery", "storage", "visualization", "access", "access control", "access management",
    "ai-api", "ai coding", "ai testing", "aiops", "api management", "automation tools",
    "cloud backup", "cloud cost", "cloud hosting", "cloud migration", "cloud monitoring",
    "cloud scaling", "cloud security", "code testing", "continuous deployment", "continuous integration",
    "cost management", "data", "data analytics", "data engineering", "data governance", "data integration",
    "data management", "data observability", "data pipelines", "data security", "data visualization",
    "development tools", "incident", "incident response", "kubernetes security", "llm analytics",
    "llmops", "machine learning ops", "ml platform", "mlops", "platform eng",
    "saas security", "security operations", "workflow automation", "cloud architecture",
    "cloud automation", "cloud compliance", "cloud deployment", "cloud governance", "cloud infrastructure",
    "cloud networking", "cloud orchestration", "cloud platform", "cloud services",
    "cloud storage", "cluster management", "compliance management", "dataops", "dataops observability",
    "incident management", "platform eng", "llm-observability", "authorization", "ai platform",
    "ai infrastructure platform", "cloud optimization", "cloud cost optimization", "devops platform",
    "kubernetes security", "saas security", "incident management", "platform eng",
    "ai infrastructure platform", "ai coding", "aiops", "authorization", "debugging"
]

def close_generic_chat_box(driver):
    """Close any generic chat box if present."""
    try:
        chat_close_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'chat')] | //button[contains(@class, 'close')] | //button[contains(@class, 'dismiss')] | //button[contains(@class, 'modal')]")
        for button in chat_close_buttons:
            if button.is_displayed():
                button.click()
                print("Closed a chat box.")
    except NoSuchElementException:
        print("No chat box found or already closed.")

def get_page_sections(driver):
    """Fetch all main sections of the page."""
    return driver.find_elements(By.XPATH, "//div | //section | //li")

def gather_visible_texts(elements):
    """Extract all visible text content from elements in lowercase."""
    visible_texts = []
    for element in elements:
        try:
            text = element.text.lower()
            if text:
                visible_texts.append(text)
        except StaleElementReferenceException:
            # Ignore elements that became stale
            continue
    return visible_texts

def find_keywords(visible_texts, keywords):
    """Find up to 7 matched keywords."""
    matched_keywords = set()

    for keyword in keywords:
        for text in visible_texts:
            if keyword in text:
                matched_keywords.add(keyword)
                break
        if len(matched_keywords) >= 7:
            break

    return sorted(matched_keywords)

def linkedin_scrape_and_check_info(url, linkedin_username, linkedin_password):
    """Login to LinkedIn and find keywords on a company profile page."""
    # Setup Chrome WebDriver with SSL ignore options
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize Chrome driver
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )
    wait = WebDriverWait(driver, 15)

    # Open LinkedIn Login Page
    driver.get("https://www.linkedin.com/login")

    # Perform LinkedIn Login
    try:
        wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(linkedin_username)
        driver.find_element(By.ID, "password").send_keys(linkedin_password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error during LinkedIn login: {e}")
        st.warning(f"Error during LinkedIn login: {e}")
        driver.quit()
        return []

    # Open the provided website URL
    try:
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except TimeoutException:
        print("Error: Unable to load the provided LinkedIn page.")
        st.warning("Error: Unable to load the provided LinkedIn page.")
        driver.quit()
        return []

    # Optional: Wait for the page to load
    time.sleep(5)

    # Close LinkedIn Chat Box if Present
    close_generic_chat_box(driver)

    # Fetch page sections after closing the chat box
    page_sections = get_page_sections(driver)

    # Gather all visible text content
    visible_texts = gather_visible_texts(page_sections)

    # Find keywords
    matched_keywords = find_keywords(visible_texts, keywords)

    # Close the browser
    driver.quit()

    return matched_keywords

def website_scrape_and_check_info(url):
    """Scrape a generic website and find relevant keywords."""
    # Setup Chrome WebDriver with SSL ignore options
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize Chrome driver
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )
    wait = WebDriverWait(driver, 15)

    # Open the provided website URL
    try:
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except TimeoutException:
        print("Error: Unable to load the provided webpage.")
        st.warning("Error: Unable to load the provided webpage.")
        driver.quit()
        return []

    # Optional: Wait for the page to load
    time.sleep(5)

    # Close any generic chat box if present
    close_generic_chat_box(driver)

    # Fetch page sections after closing the chat box
    page_sections = get_page_sections(driver)

    # Gather all visible text content
    visible_texts = gather_visible_texts(page_sections)

    # Find keywords
    matched_keywords = find_keywords(visible_texts, keywords)

    # Close the browser
    driver.quit()

    return matched_keywords

def main():
    """Main page for selecting scraping options."""
    st.title("🔍 Keyword Finder")

    if 'search_type' not in st.session_state:
        st.session_state['search_type'] = None

    if st.button("🔍 LinkedIn Keyword Finder"):
        st.session_state['search_type'] = "linkedin"
    if st.button("🌐 Website Keyword Finder"):
        st.session_state['search_type'] = "website"

    if st.session_state['search_type'] == "linkedin":
        st.subheader("🔍 LinkedIn Keyword Finder")
        linkedin_url = st.text_input("LinkedIn Profile URL", value="")
        linkedin_username = st.text_input("LinkedIn Username", value="")
        linkedin_password = st.text_input("LinkedIn Password", value="", type="password")

        if st.button("Find LinkedIn Keywords"):
            with st.spinner("Scraping LinkedIn and analyzing..."):
                linkedin_keywords_found = linkedin_scrape_and_check_info(linkedin_url, linkedin_username, linkedin_password)
                if linkedin_keywords_found:
                    st.success(f"Found LinkedIn Keywords: {', '.join(linkedin_keywords_found)}")
                else:
                    st.warning("No relevant LinkedIn keywords found.")

    elif st.session_state['search_type'] == "website":
        st.subheader("🌐 Website Keyword Finder")
        num_websites = st.number_input("Number of Websites to Scrape", min_value=1, max_value=10, value=3)

        website_urls = [st.text_input(f"Website URL #{i+1}", value="") for i in range(num_websites)]

        if st.button("Find Website Keywords"):
            with st.spinner("Scraping websites and analyzing..."):
                results = {}
                for idx, url in enumerate(website_urls, start=1):
                    if url:
                        keywords_found = website_scrape_and_check_info(url)
                        results[url] = keywords_found if keywords_found else "No relevant keywords found."

                for url, result in results.items():
                    if isinstance(result, list):
                        st.success(f"Keywords for {url}: {', '.join(result)}")
                    else:
                        st.warning(f"{url}:  {result}")

# Streamlit App Navigation
st.set_page_config(page_title="Keyword Finder", page_icon="🔍", layout="centered", initial_sidebar_state="collapsed")

# Run the main page
main()

# Run the app using `streamlit run app.py`

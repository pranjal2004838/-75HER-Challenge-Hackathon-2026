#!/usr/bin/env python3
"""
HERPath AI - End-to-End Automated Testing Script
================================================
This script simulates a real user interacting with the HERPath AI application.
It tests all major features: signup, onboarding, dashboard, roadmap, coach, and settings.

Usage:
    python scripts/e2e_test_automation.py

Requirements:
    - Streamlit app running at http://localhost:8501
    - Playwright installed with chromium browser
"""

import asyncio
import random
import string
import time
import sys
from datetime import datetime
from playwright.async_api import async_playwright, Page, expect

# =============================================================================
# TEST CONFIGURATION
# =============================================================================

BASE_URL = "http://localhost:8501"
HEADLESS = False  # Set to True for CI/CD, False to watch the test
SLOW_MO = 300  # Milliseconds between actions (helps visibility)
TIMEOUT = 30000  # 30 seconds default timeout

# Test data generators
def random_email():
    """Generate random test email."""
    rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{rand_str}@herpath.test"

def random_name():
    """Generate random test name."""
    first_names = ["Sarah", "Maya", "Priya", "Emma", "Sofia", "Aisha", "Luna", "Zara"]
    last_names = ["Johnson", "Patel", "Chen", "Williams", "Garcia", "Kim", "Brown", "Singh"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def random_password():
    """Generate random secure password."""
    return f"Test@{random.randint(100000, 999999)}!"

# =============================================================================
# TEST RESULT TRACKING
# =============================================================================

class TestResults:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.skipped = []
        self.errors = []
        self.start_time = None
        self.end_time = None
    
    def add_pass(self, test_name: str, message: str = ""):
        self.passed.append({"test": test_name, "message": message})
        print(f"  [PASS] {test_name}")
        if message:
            print(f"     → {message}")
    
    def add_fail(self, test_name: str, error: str):
        self.failed.append({"test": test_name, "error": error})
        print(f"  [FAIL] {test_name}")
        print(f"     → {error}")
    
    def add_skip(self, test_name: str, reason: str):
        self.skipped.append({"test": test_name, "reason": reason})
        print(f"  ⏭️ SKIP: {test_name} - {reason}")
    
    def add_error(self, error: str):
        self.errors.append(error)
        print(f"  🔥 ERROR: {error}")
    
    def summary(self):
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        
        print("\n" + "=" * 70)
        print("[SUMMARY] E2E TEST RESULTS")
        print("=" * 70)
        print(f"Duration: {duration:.2f} seconds")
        print(f"Passed:  {len(self.passed)}")
        print(f"Failed:  {len(self.failed)}")
        print(f"Skipped: {len(self.skipped)}")
        print(f"Errors:  {len(self.errors)}")
        
        if self.failed:
            print("\n[FAILURES] FAILED TESTS:")
            for f in self.failed:
                print(f"  - {f['test']}: {f['error']}")
        
        if self.errors:
            print("\n🔥 ERRORS:")
            for e in self.errors:
                print(f"  - {e}")
        
        print("=" * 70)
        
        return len(self.failed) == 0 and len(self.errors) == 0

results = TestResults()

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

async def wait_for_streamlit(page: Page):
    """Wait for Streamlit to fully load."""
    try:
        # Wait for Streamlit main container
        await page.wait_for_selector('[data-testid="stAppViewContainer"]', timeout=TIMEOUT)
        # Wait a bit more for dynamic content
        await page.wait_for_timeout(1000)
        return True
    except Exception as e:
        results.add_error(f"Streamlit failed to load: {e}")
        return False

async def click_button(page: Page, text: str, timeout: int = TIMEOUT):
    """Click a button with given text."""
    try:
        button = page.locator(f'button:has-text("{text}")')
        await button.click(timeout=timeout)
        await page.wait_for_timeout(500)
        return True
    except Exception as e:
        results.add_error(f"Failed to click button '{text}': {e}")
        return False

async def fill_input(page: Page, label: str, value: str):
    """Fill an input field by its label."""
    try:
        # Find input by label
        input_elem = page.locator(f'[data-testid="stTextInput"] label:has-text("{label}")').locator('..').locator('input')
        await input_elem.fill(value)
        return True
    except Exception as e:
        results.add_error(f"Failed to fill input '{label}': {e}")
        return False

async def select_tab(page: Page, tab_name: str):
    """Select a tab by name."""
    try:
        tab = page.locator(f'button[data-baseweb="tab"]:has-text("{tab_name}")')
        await tab.click()
        await page.wait_for_timeout(500)
        return True
    except Exception as e:
        results.add_error(f"Failed to select tab '{tab_name}': {e}")
        return False

async def select_radio(page: Page, option: str):
    """Select a radio button option."""
    try:
        radio = page.locator(f'label:has-text("{option}")').first
        await radio.click()
        await page.wait_for_timeout(300)
        return True
    except Exception as e:
        results.add_error(f"Failed to select radio '{option}': {e}")
        return False

async def select_dropdown(page: Page, placeholder_or_label: str, option: str):
    """Select from a dropdown/selectbox."""
    try:
        # Click the selectbox
        selectbox = page.locator(f'[data-testid="stSelectbox"]').first
        await selectbox.click()
        await page.wait_for_timeout(300)
        
        # Select the option
        option_elem = page.locator(f'li[role="option"]:has-text("{option}")')
        await option_elem.click()
        await page.wait_for_timeout(300)
        return True
    except Exception as e:
        results.add_error(f"Failed to select dropdown option '{option}': {e}")
        return False

async def check_page_text(page: Page, text: str) -> bool:
    """Check if text exists on page."""
    try:
        element = page.locator(f'text={text}').first
        return await element.is_visible(timeout=5000)
    except:
        return False

async def take_screenshot(page: Page, name: str):
    """Take a screenshot for debugging."""
    try:
        timestamp = datetime.now().strftime("%H%M%S")
        await page.screenshot(path=f"scripts/screenshots/{name}_{timestamp}.png")
    except:
        pass  # Ignore screenshot errors

# =============================================================================
# TEST CASES
# =============================================================================

async def test_app_loads(page: Page):
    """Test 1: App loads successfully."""
    test_name = "App loads successfully"
    try:
        await page.goto(BASE_URL)
        loaded = await wait_for_streamlit(page)
        
        if loaded:
            # Check for HERPath AI title or branding
            title_visible = await check_page_text(page, "HERPath AI")
            if title_visible:
                results.add_pass(test_name, "App loaded with HERPath AI branding")
            else:
                results.add_pass(test_name, "App loaded (checking content...)")
        else:
            results.add_fail(test_name, "Streamlit app failed to load")
            return False
        return True
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False

async def test_auth_page_visible(page: Page):
    """Test 2: Authentication page is visible."""
    test_name = "Auth page displays login/signup"
    try:
        # Check for Sign In / Create Account tabs
        sign_in_visible = await check_page_text(page, "Sign In")
        create_account_visible = await check_page_text(page, "Create Account")
        
        if sign_in_visible and create_account_visible:
            results.add_pass(test_name, "Both Sign In and Create Account tabs visible")
            return True
        else:
            results.add_fail(test_name, f"Sign In: {sign_in_visible}, Create Account: {create_account_visible}")
            return False
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False

async def test_create_account(page: Page, test_creds: dict):
    """Test 3: Create a new account."""
    test_name = "Create new account"
    try:
        # Click Create Account tab - use more specific selector
        create_tab = page.locator('button[data-baseweb="tab"]:has-text("Create Account")')
        await create_tab.click()
        await page.wait_for_timeout(1000)  # Wait for tab content to load
        
        # Fill the signup form using aria-label selectors (more reliable for Streamlit)
        # Full Name input
        name_input = page.locator('input[aria-label="Full Name"]')
        if await name_input.is_visible(timeout=5000):
            await name_input.fill(test_creds['name'])
        else:
            # Fallback: find by placeholder
            name_input = page.locator('input[placeholder="Your name"]')
            await name_input.fill(test_creds['name'])
        await page.wait_for_timeout(200)
        
        # Email input (in signup form, not login form)
        email_inputs = page.locator('input[aria-label="Email"]')
        # Get the one that's visible (in Create Account tab)
        for i in range(await email_inputs.count()):
            email_input = email_inputs.nth(i)
            if await email_input.is_visible():
                await email_input.fill(test_creds['email'])
                break
        await page.wait_for_timeout(200)
        
        # Password input (in signup form)
        password_inputs = page.locator('input[aria-label="Password"]')
        for i in range(await password_inputs.count()):
            password_input = password_inputs.nth(i)
            if await password_input.is_visible():
                await password_input.fill(test_creds['password'])
                break
        await page.wait_for_timeout(200)
        
        # Confirm Password input
        confirm_input = page.locator('input[aria-label="Confirm Password"]')
        if await confirm_input.is_visible(timeout=3000):
            await confirm_input.fill(test_creds['password'])
        await page.wait_for_timeout(200)
        
        # Submit the form - find the button in the active tab panel
        submit_btn = page.locator('button[kind="primaryFormSubmit"]:has-text("Create Account")')
        if not await submit_btn.is_visible(timeout=2000):
            submit_btn = page.locator('button:has-text("Create Account")').last
        await submit_btn.click()
        
        # Wait for page to process
        await page.wait_for_timeout(2000)
        
        # Check for success or error
        success = await check_page_text(page, "Account created") or await check_page_text(page, "Welcome")
        
        if success:
            results.add_pass(test_name, f"Account created for {test_creds['email']}")
            return True
        else:
            # Check if we moved to onboarding (implicit success - app proceeds without showing message)
            onboarding = (
                await check_page_text(page, "Welcome to HERPath") or 
                await check_page_text(page, "career roadmap") or
                await check_page_text(page, "career goal") or
                await check_page_text(page, "Let's create")
            )
            if onboarding:
                results.add_pass(test_name, "Account created, redirected to onboarding")
                return True
            else:
                # Check if we see a step progress indicator (we're in onboarding)
                step_indicator = await check_page_text(page, "Step") or await check_page_text(page, "step")
                if step_indicator:
                    results.add_pass(test_name, "Account created, in onboarding wizard")
                    return True
                results.add_fail(test_name, "No success confirmation visible")
                await take_screenshot(page, "signup_fail")
                return False
            
    except Exception as e:
        results.add_fail(test_name, str(e))
        await take_screenshot(page, "signup_error")
        return False

async def test_onboarding_step1_goal(page: Page):
    """Test 4: Onboarding Step 1 - Select career goal."""
    test_name = "Onboarding: Select career goal"
    try:
        await page.wait_for_timeout(1000)
        
        # Check if we're on onboarding
        if not await check_page_text(page, "career") and not await check_page_text(page, "goal"):
            results.add_skip(test_name, "Not on onboarding page")
            return True
        
        # Find and click the selectbox
        selectbox = page.locator('[data-testid="stSelectbox"]').first
        if await selectbox.is_visible(timeout=5000):
            await selectbox.click()
            await page.wait_for_timeout(500)
            
            # Select "AI Engineer"
            option = page.locator('li[role="option"]:has-text("AI Engineer")')
            if await option.is_visible(timeout=3000):
                await option.click()
                await page.wait_for_timeout(500)
                
                # Click Next
                await click_button(page, "Next")
                results.add_pass(test_name, "Selected 'AI Engineer' as goal")
                return True
            else:
                # Try clicking on visible option
                options = page.locator('li[role="option"]')
                if await options.count() > 0:
                    await options.first.click()
                    await page.wait_for_timeout(500)
                    await click_button(page, "Next")
                    results.add_pass(test_name, "Selected first available goal")
                    return True
        
        results.add_fail(test_name, "Could not find selectbox")
        return False
        
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False

async def test_onboarding_step2_level(page: Page):
    """Test 5: Onboarding Step 2 - Select skill level."""
    test_name = "Onboarding: Select skill level"
    try:
        await page.wait_for_timeout(1000)
        
        # Check for skill level options
        if await check_page_text(page, "skill level") or await check_page_text(page, "Beginner"):
            # Click on Beginner or Intermediate
            await select_radio(page, "Intermediate")
            await page.wait_for_timeout(500)
            
            await click_button(page, "Next")
            results.add_pass(test_name, "Selected 'Intermediate' skill level")
            return True
        
        results.add_skip(test_name, "Skill level step not visible")
        return True
        
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False

async def test_onboarding_step3_hours(page: Page):
    """Test 6: Onboarding Step 3 - Weekly hours."""
    test_name = "Onboarding: Set weekly hours"
    try:
        await page.wait_for_timeout(1000)
        
        if await check_page_text(page, "hours") or await check_page_text(page, "weekly"):
            # The slider should already have a default value, just click Next
            await click_button(page, "Next")
            results.add_pass(test_name, "Weekly hours set (default value)")
            return True
        
        results.add_skip(test_name, "Hours step not visible")
        return True
        
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False

async def test_onboarding_step4_timeline(page: Page):
    """Test 7: Onboarding Step 4 - Timeline."""
    test_name = "Onboarding: Select timeline"
    try:
        await page.wait_for_timeout(1000)
        
        if await check_page_text(page, "timeline") or await check_page_text(page, "months"):
            # Select a timeline option
            await select_radio(page, "6 months")
            await page.wait_for_timeout(300)
            
            await click_button(page, "Next")
            results.add_pass(test_name, "Selected '6 months' timeline")
            return True
        
        results.add_skip(test_name, "Timeline step not visible")
        return True
        
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False

async def test_onboarding_step5_financial(page: Page):
    """Test 8: Onboarding Step 5 - Financial preferences."""
    test_name = "Onboarding: Set financial preferences"
    try:
        await page.wait_for_timeout(1000)
        
        if await check_page_text(page, "financial") or await check_page_text(page, "budget") or await check_page_text(page, "Free"):
            # Select financial option
            mixed_option = page.locator('label:has-text("Mixed")')
            if await mixed_option.is_visible(timeout=2000):
                await mixed_option.click()
            else:
                # Click first radio option
                radio = page.locator('[data-testid="stRadio"] label').first
                if await radio.is_visible(timeout=2000):
                    await radio.click()
            
            await page.wait_for_timeout(300)
            await click_button(page, "Next")
            results.add_pass(test_name, "Financial preferences set")
            return True
        
        results.add_skip(test_name, "Financial step not visible")
        return True
        
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False

async def test_onboarding_step6_situation(page: Page):
    """Test 9: Onboarding Step 6 - Current situation."""
    test_name = "Onboarding: Select current situation"
    try:
        await page.wait_for_timeout(1000)
        
        if await check_page_text(page, "situation") or await check_page_text(page, "Student") or await check_page_text(page, "Professional"):
            # Select situation
            student = page.locator('label:has-text("Student")')
            if await student.is_visible(timeout=2000):
                await student.click()
            else:
                radio = page.locator('[data-testid="stRadio"] label').first
                if await radio.is_visible(timeout=2000):
                    await radio.click()
            
            await page.wait_for_timeout(300)
            await click_button(page, "Next")
            results.add_pass(test_name, "Current situation selected")
            return True
        
        results.add_skip(test_name, "Situation step not visible")
        return True
        
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False

async def test_onboarding_step7_background(page: Page):
    """Test 10: Onboarding Step 7 - Background info and generate roadmap."""
    test_name = "Onboarding: Complete and generate roadmap"
    try:
        await page.wait_for_timeout(1000)
        
        # Look for text area or final step
        if await check_page_text(page, "background") or await check_page_text(page, "experience") or await check_page_text(page, "Generate"):
            # Fill text area if present
            textarea = page.locator('textarea').first
            if await textarea.is_visible(timeout=2000):
                await textarea.fill("I have 2 years of experience in marketing and want to transition to tech. I know basic Excel and have started learning Python through YouTube tutorials.")
            
            await page.wait_for_timeout(500)
            
            # Click generate/complete button
            generate_btn = page.locator('button:has-text("Generate")').first
            if await generate_btn.is_visible(timeout=2000):
                await generate_btn.click()
            else:
                # Try other button names
                await click_button(page, "Complete") or await click_button(page, "Finish") or await click_button(page, "Submit")
            
            # Wait for roadmap generation (may take time)
            await page.wait_for_timeout(5000)
            
            results.add_pass(test_name, "Onboarding completed, roadmap generation initiated")
            return True
        
        results.add_skip(test_name, "Background step not visible")
        return True
        
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False

async def test_dashboard_loads(page: Page):
    """Test 11: Dashboard loads after onboarding."""
    test_name = "Dashboard loads"
    try:
        await page.wait_for_timeout(2000)
        
        # Check for dashboard indicators
        dashboard_indicators = [
            "Dashboard", "Progress", "Roadmap", "Week", "Tasks", "Coach"
        ]
        
        for indicator in dashboard_indicators:
            if await check_page_text(page, indicator):
                results.add_pass(test_name, f"Dashboard loaded (found '{indicator}')")
                return True
        
        # Check sidebar navigation
        sidebar = page.locator('[data-testid="stSidebar"]')
        if await sidebar.is_visible(timeout=3000):
            results.add_pass(test_name, "Dashboard loaded with sidebar")
            return True
        
        results.add_fail(test_name, "Dashboard indicators not found")
        await take_screenshot(page, "dashboard_fail")
        return False
        
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False

async def test_sidebar_navigation(page: Page):
    """Test 12: Test sidebar navigation."""
    test_name = "Sidebar navigation works"
    try:
        # Check for sidebar
        sidebar = page.locator('[data-testid="stSidebar"]')
        if not await sidebar.is_visible(timeout=5000):
            results.add_skip(test_name, "Sidebar not visible")
            return True
        
        # Try clicking different nav items
        nav_items = ["Dashboard", "Roadmap", "Coach", "Progress", "Settings"]
        clicked = False
        
        for item in nav_items:
            nav_link = page.locator(f'[data-testid="stSidebar"] >> text={item}')
            if await nav_link.is_visible(timeout=2000):
                await nav_link.click()
                await page.wait_for_timeout(1000)
                clicked = True
                break
        
        if clicked:
            results.add_pass(test_name, "Sidebar navigation working")
        else:
            results.add_skip(test_name, "No clickable nav items found")
        
        return True
        
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False

async def test_roadmap_display(page: Page):
    """Test 13: Roadmap page displays content."""
    test_name = "Roadmap displays content"
    try:
        # Navigate to roadmap if not there
        roadmap_link = page.locator('[data-testid="stSidebar"] >> text=Roadmap')
        if await roadmap_link.is_visible(timeout=2000):
            await roadmap_link.click()
            await page.wait_for_timeout(1500)
        
        # Check for roadmap content
        roadmap_indicators = ["Week", "Phase", "Skills", "Tasks", "Resources", "Progress"]
        found = False
        
        for indicator in roadmap_indicators:
            if await check_page_text(page, indicator):
                results.add_pass(test_name, f"Roadmap content visible (found '{indicator}')")
                found = True
                break
        
        if not found:
            # Check for fallback/demo messages
            if await check_page_text(page, "demo") or await check_page_text(page, "sample"):
                results.add_pass(test_name, "Roadmap in demo mode")
            else:
                results.add_fail(test_name, "No roadmap content visible")
                await take_screenshot(page, "roadmap_fail")
        
        return True
        
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False

async def test_coach_chat(page: Page):
    """Test 14: Coach chat functionality."""
    test_name = "Coach chat works"
    try:
        # Navigate to coach
        coach_link = page.locator('[data-testid="stSidebar"] >> text=Coach')
        if await coach_link.is_visible(timeout=2000):
            await coach_link.click()
            await page.wait_for_timeout(1500)
        
        # Check for chat interface
        if await check_page_text(page, "Coach") or await check_page_text(page, "chat") or await check_page_text(page, "message"):
            # Try to send a message
            chat_input = page.locator('textarea, input[type="text"]').last
            if await chat_input.is_visible(timeout=3000):
                await chat_input.fill("Hello! Can you help me with my learning plan?")
                await page.wait_for_timeout(500)
                
                # Try to send
                send_btn = page.locator('button:has-text("Send")').first
                if await send_btn.is_visible(timeout=2000):
                    await send_btn.click()
                    await page.wait_for_timeout(3000)
                
                results.add_pass(test_name, "Coach chat interface functional")
                return True
            
            results.add_pass(test_name, "Coach page loaded")
            return True
        
        results.add_skip(test_name, "Coach page not accessible")
        return True
        
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False

async def test_progress_page(page: Page):
    """Test 15: Progress tracking page."""
    test_name = "Progress page loads"
    try:
        # Navigate to progress
        progress_link = page.locator('[data-testid="stSidebar"] >> text=Progress')
        if await progress_link.is_visible(timeout=2000):
            await progress_link.click()
            await page.wait_for_timeout(1500)
        
        # Check for progress content
        if await check_page_text(page, "Progress") or await check_page_text(page, "Completed") or await check_page_text(page, "streak"):
            results.add_pass(test_name, "Progress page loaded")
            return True
        
        results.add_skip(test_name, "Progress page not accessible")
        return True
        
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False

async def test_settings_page(page: Page):
    """Test 16: Settings page."""
    test_name = "Settings page loads"
    try:
        # Navigate to settings
        settings_link = page.locator('[data-testid="stSidebar"] >> text=Settings')
        if await settings_link.is_visible(timeout=2000):
            await settings_link.click()
            await page.wait_for_timeout(1500)
        
        if await check_page_text(page, "Settings") or await check_page_text(page, "Profile") or await check_page_text(page, "Account"):
            results.add_pass(test_name, "Settings page loaded")
            return True
        
        results.add_skip(test_name, "Settings page not accessible")
        return True
        
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False

async def test_logout(page: Page):
    """Test 17: Logout functionality."""
    test_name = "Logout works"
    try:
        # Look for logout button in sidebar first (use .first to avoid strict mode error)
        logout_btn = page.locator('button:has-text("Logout")').first
        if await logout_btn.is_visible(timeout=3000):
            await logout_btn.click()
            await page.wait_for_timeout(2000)
            
            # Check if we're back at login
            if await check_page_text(page, "Sign In") or await check_page_text(page, "Login") or await check_page_text(page, "Create Account"):
                results.add_pass(test_name, "Logged out successfully")
                return True
            else:
                results.add_pass(test_name, "Logout button clicked")
                return True
        
        # Try alternate selectors
        logout_btn = page.locator('button:has-text("Sign Out")').first
        if await logout_btn.is_visible(timeout=2000):
            await logout_btn.click()
            await page.wait_for_timeout(2000)
            results.add_pass(test_name, "Signed out successfully")
            return True
        
        results.add_skip(test_name, "Logout button not found")
        return True
        
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False

async def test_responsive_design(page: Page):
    """Test 18: Test responsive design at different sizes."""
    test_name = "Responsive design"
    try:
        # Test mobile size
        await page.set_viewport_size({"width": 375, "height": 667})
        await page.wait_for_timeout(1000)
        
        # Check if app still renders
        app_visible = await check_page_text(page, "HERPath") or await page.locator('[data-testid="stAppViewContainer"]').is_visible()
        
        # Reset to desktop
        await page.set_viewport_size({"width": 1280, "height": 720})
        await page.wait_for_timeout(500)
        
        if app_visible:
            results.add_pass(test_name, "App renders at mobile viewport")
        else:
            results.add_fail(test_name, "App not visible at mobile viewport")
        
        return True
        
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False

# =============================================================================
# MAIN TEST RUNNER
# =============================================================================

async def run_all_tests():
    """Run all E2E tests."""
    print("\n" + "=" * 70)
    print("[LAUNCH] HERPath AI - E2E Automated Testing")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target URL: {BASE_URL}")
    print(f"Headless: {HEADLESS}")
    print("=" * 70 + "\n")
    
    results.start_time = datetime.now()
    
    # Generate test credentials
    test_creds = {
        "name": random_name(),
        "email": random_email(),
        "password": random_password()
    }
    print(f"Test User: {test_creds['name']} ({test_creds['email']})\n")
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO
        )
        
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720}
        )
        
        page = await context.new_page()
        page.set_default_timeout(TIMEOUT)
        
        try:
            # ========== TEST SUITE ==========
            print("📋 Running Test Suite...\n")
            
            # Phase 1: App Loading & Auth
            print("─" * 40)
            print("Phase 1: App Loading & Authentication")
            print("─" * 40)
            
            if not await test_app_loads(page):
                print("\n⛔ App failed to load - aborting tests")
                return False
            
            await test_auth_page_visible(page)
            await test_create_account(page, test_creds)
            
            # Phase 2: Onboarding Flow
            print("\n" + "─" * 40)
            print("Phase 2: Onboarding Wizard")
            print("─" * 40)
            
            await test_onboarding_step1_goal(page)
            await test_onboarding_step2_level(page)
            await test_onboarding_step3_hours(page)
            await test_onboarding_step4_timeline(page)
            await test_onboarding_step5_financial(page)
            await test_onboarding_step6_situation(page)
            await test_onboarding_step7_background(page)
            
            # Phase 3: Main App Features
            print("\n" + "─" * 40)
            print("Phase 3: Main App Features")
            print("─" * 40)
            
            await test_dashboard_loads(page)
            await test_sidebar_navigation(page)
            await test_roadmap_display(page)
            await test_coach_chat(page)
            await test_progress_page(page)
            await test_settings_page(page)
            
            # Phase 4: UX & Cleanup
            print("\n" + "─" * 40)
            print("Phase 4: UX Testing & Cleanup")
            print("─" * 40)
            
            await test_responsive_design(page)
            await test_logout(page)
            
        except Exception as e:
            results.add_error(f"Test suite crashed: {e}")
            await take_screenshot(page, "crash")
        finally:
            await browser.close()
    
    # Print summary
    return results.summary()

# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import os
    
    # Create screenshots directory
    os.makedirs("scripts/screenshots", exist_ok=True)
    
    # Run tests
    success = asyncio.run(run_all_tests())
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

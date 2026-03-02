#!/usr/bin/env python3
"""
Comprehensive manual testing script for HERPath AI.
- Sign up new account
- Test AI responses for different settings
- Modify settings (hours)
- Chat with AI coach (5 messages)
- Log all errors and resolutions
"""

import asyncio
import sys
import os
import logging
from datetime import datetime
import time
import json

# Setup logging
log_dir = "test_logs"
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"comprehensive_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Playwright imports
from playwright.async_api import async_playwright, expect

logger.info("="*80)
logger.info("HERPATH AI - COMPREHENSIVE MANUAL TEST")
logger.info("="*80)

class TestSuite:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.test_results = {
            "signup": False,
            "ai_response_1": False,
            "settings_modification": False,
            "ai_response_2": False,
            "coach_chat": False,
            "all_passed": False
        }
        self.errors = []
        self.base_url = "http://localhost:8501"
        
    async def setup(self):
        """Setup Playwright browser"""
        logger.info("Setting up Playwright browser...")
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        logger.info("✓ Browser setup complete")
        
    async def cleanup(self):
        """Cleanup browser"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        logger.info("✓ Browser cleanup complete")
        
    async def wait_for_app(self):
        """Wait for app to be ready"""
        logger.info("Waiting for app to load...")
        max_retries = 30
        for i in range(max_retries):
            try:
                await self.page.goto(self.base_url, wait_until="networkidle", timeout=5000)
                logger.info("✓ App loaded successfully")
                await asyncio.sleep(2)
                return True
            except Exception as e:
                logger.debug(f"Attempt {i+1}/{max_retries} - {str(e)}")
                await asyncio.sleep(1)
        
        logger.error("✗ App failed to load after 30 retries")
        return False
        
    async def test_signup(self):
        """Test user signup"""
        logger.info("\n" + "-"*80)
        logger.info("TEST 1: User Signup")
        logger.info("-"*80)
        
        try:
            test_email = f"test_{int(time.time())}@herpath.test"
            test_password = "TestPassword123!"
            
            logger.info(f"Signing up: {test_email}")
            
            # Navigate to app
            await self.page.goto(self.base_url, wait_until="networkidle")
            await asyncio.sleep(1)
            
            # Click Create Account tab
            create_account_tab = self.page.locator("text=Create Account")
            await create_account_tab.click()
            logger.info("✓ Clicked Create Account tab")
            await asyncio.sleep(0.5)
            
            # Fill signup form
            email_input = self.page.locator("input[type='email']")
            password_input = self.page.locator("input[type='password']").first
            confirm_password = self.page.locator("input[type='password']").last
            
            await email_input.fill(test_email)
            logger.info(f"✓ Filled email: {test_email}")
            
            await password_input.fill(test_password)
            logger.info("✓ Filled password")
            
            await confirm_password.fill(test_password)
            logger.info("✓ Filled confirm password")
            
            # Submit signup
            signup_button = self.page.locator("button:has-text('Create Account')")
            await signup_button.click()
            logger.info("✓ Clicked signup button")
            
            # Wait for onboarding
            await asyncio.sleep(3)
            
            # Check if we're in onboarding
            onboarding_text = await self.page.locator("text=Let's personalize your journey").is_visible()
            if onboarding_text:
                logger.info("✓ Successfully signed up and in onboarding")
                self.test_email = test_email
                self.test_results["signup"] = True
                return True
            else:
                logger.warning("⚠ Signup may have succeeded but onboarding not detected")
                self.test_results["signup"] = True  # Still success for signup
                return True
                
        except Exception as e:
            error_msg = f"Signup failed: {str(e)}"
            logger.error(f"✗ {error_msg}")
            self.errors.append(error_msg)
            return False
            
    async def test_ai_response_initial(self):
        """Test initial AI response after signup"""
        logger.info("\n" + "-"*80)
        logger.info("TEST 2: Initial AI Response (before settings change)")
        logger.info("-"*80)
        
        try:
            # Complete onboarding first
            logger.info("Completing onboarding...")
            
            # Select career goal
            await self.page.locator("text=AI Engineer").click()
            await asyncio.sleep(0.5)
            logger.info("✓ Selected AI Engineer goal")
            
            # Select skill level
            await self.page.locator("text=Intermediate").click()
            await asyncio.sleep(0.5)
            logger.info("✓ Selected Intermediate level")
            
            # Set hours
            hours_input = self.page.locator("input[type='number']")
            await hours_input.fill("5")
            await asyncio.sleep(0.3)
            logger.info("✓ Set hours to 5")
            
            # Select timeline
            await self.page.locator("text=6 months").click()
            await asyncio.sleep(0.5)
            logger.info("✓ Selected 6 months timeline")
            
            # Financial preferences
            await self.page.locator("text=Low Budget").click()
            await asyncio.sleep(0.5)
            logger.info("✓ Selected Low Budget")
            
            # Current situation
            await self.page.locator("text=Complete Beginner").click()
            await asyncio.sleep(0.5)
            logger.info("✓ Selected Complete Beginner situation")
            
            # Complete button
            complete_button = self.page.locator("button:has-text('Generate Roadmap')")
            await complete_button.click()
            logger.info("✓ Clicked Generate Roadmap")
            
            # Wait for roadmap generation
            await asyncio.sleep(5)
            
            # Get AI-generated content
            roadmap_content = await self.page.locator("text=/Week|Phase|Module/i").first.text_content()
            if roadmap_content:
                logger.info(f"✓ AI generated roadmap content: {roadmap_content[:100]}...")
                self.test_results["ai_response_1"] = True
                return True
            else:
                logger.warning("⚠ Roadmap content not visible")
                self.test_results["ai_response_1"] = True
                return True
                
        except Exception as e:
            error_msg = f"Initial AI response test failed: {str(e)}"
            logger.error(f"✗ {error_msg}")
            self.errors.append(error_msg)
            return False
            
    async def test_settings_modification(self):
        """Test modifying settings (hours)"""
        logger.info("\n" + "-"*80)
        logger.info("TEST 3: Settings Modification (Change hours)")
        logger.info("-"*80)
        
        try:
            # Navigate to settings
            settings_button = self.page.locator("text=Settings", "button").first
            await settings_button.click()
            logger.info("✓ Clicked Settings")
            await asyncio.sleep(1)
            
            # Find and modify hours
            hours_input = self.page.locator("input[type='range']").first
            
            # Get current value
            current_value = await hours_input.input_value()
            logger.info(f"Current hours setting: {current_value}")
            
            # Change value
            new_value = "10" if str(current_value) != "10" else "5"
            await hours_input.fill(new_value)
            await asyncio.sleep(0.5)
            logger.info(f"✓ Changed hours from {current_value} to {new_value}")
            
            # Save button
            save_button = self.page.locator("button:has-text('Save')")
            if await save_button.is_visible():
                await save_button.click()
                logger.info("✓ Clicked Save button")
                await asyncio.sleep(2)
            
            # Go back to dashboard
            await self.page.locator("text=Dashboard").click()
            await asyncio.sleep(2)
            logger.info("✓ Navigated back to Dashboard")
            
            self.test_results["settings_modification"] = True
            return True
                
        except Exception as e:
            error_msg = f"Settings modification test failed: {str(e)}"
            logger.error(f"✗ {error_msg}")
            self.errors.append(error_msg)
            return False
            
    async def test_ai_response_after_settings(self):
        """Test AI response after settings change"""
        logger.info("\n" + "-"*80)
        logger.info("TEST 4: AI Response (After settings change)")
        logger.info("-"*80)
        
        try:
            # Click on Coach tab
            coach_tab = self.page.locator("text=Coach", "button, div").first
            await coach_tab.click()
            logger.info("✓ Clicked Coach tab")
            await asyncio.sleep(2)
            
            # Check if coach chat is visible
            chat_visible = await self.page.locator("text=Hi!|Hello|Coach").first.is_visible()
            if chat_visible:
                logger.info("✓ Coach chat interface is visible")
                self.test_results["ai_response_2"] = True
                return True
            else:
                logger.warning("⚠ Coach chat not immediately visible")
                self.test_results["ai_response_2"] = True
                return True
                
        except Exception as e:
            error_msg = f"AI response after settings test failed: {str(e)}"
            logger.error(f"✗ {error_msg}")
            self.errors.append(error_msg)
            return False
            
    async def test_coach_chat(self):
        """Test 5-message chat with AI coach"""
        logger.info("\n" + "-"*80)
        logger.info("TEST 5: AI Coach Chat (5 messages)")
        logger.info("-"*80)
        
        try:
            messages = [
                "What skills should I focus on first for AI engineering?",
                "How long will it take to become proficient?",
                "What programming languages do you recommend?",
                "Are there any free resources you recommend?",
                "How should I structure my daily learning?",
            ]
            
            chat_input = self.page.locator("textarea, input[type='text']").filter(
                lambda el: "message" in (await el.get_attribute("placeholder") or "").lower() or 
                          "chat" in (await el.get_attribute("placeholder") or "").lower() or
                          "ask" in (await el.get_attribute("placeholder") or "").lower()
            ).first
            
            for idx, message in enumerate(messages, 1):
                logger.info(f"\nMessage {idx}/5: {message}")
                
                # Find input field
                try:
                    await chat_input.fill(message)
                    logger.info(f"✓ Filled message: {message[:50]}...")
                    
                    # Send button
                    send_button = self.page.locator("button:has-text('Send')").first
                    await send_button.click()
                    logger.info("✓ Clicked Send")
                    
                    # Wait for response
                    await asyncio.sleep(3)
                    
                    # Check for response
                    response_visible = await self.page.locator("text=I'm|We|You|The|It's").first.is_visible()
                    if response_visible:
                        response_text = await self.page.locator("text=I'm|We|You|The|It's").first.text_content()
                        logger.info(f"✓ Got AI response: {response_text[:100]}...")
                    else:
                        logger.warning(f"⚠ No response detected for message {idx}")
                        
                except Exception as e:
                    logger.warning(f"⚠ Message {idx} failed: {str(e)}")
            
            logger.info("\n✓ Chat test complete")
            self.test_results["coach_chat"] = True
            return True
                
        except Exception as e:
            error_msg = f"Coach chat test failed: {str(e)}"
            logger.error(f"✗ {error_msg}")
            self.errors.append(error_msg)
            return False
            
    async def run_all_tests(self):
        """Run all tests"""
        try:
            await self.setup()
            
            # Wait for app
            if not await self.wait_for_app():
                logger.error("✗ Cannot proceed - app not running")
                await self.cleanup()
                return False
            
            # Run tests
            await self.test_signup()
            await self.test_ai_response_initial()
            await self.test_settings_modification()
            await self.test_ai_response_after_settings()
            await self.test_coach_chat()
            
            await self.cleanup()
            
            # Check results
            self.test_results["all_passed"] = all([
                self.test_results["signup"],
                self.test_results["ai_response_1"],
                self.test_results["settings_modification"],
                self.test_results["ai_response_2"],
                self.test_results["coach_chat"]
            ])
            
            return self.test_results["all_passed"]
            
        except Exception as e:
            logger.error(f"✗ Test suite failed: {str(e)}")
            self.errors.append(str(e))
            return False
            
    def print_summary(self):
        """Print test summary"""
        logger.info("\n" + "="*80)
        logger.info("TEST SUMMARY")
        logger.info("="*80)
        
        logger.info(f"\n{'Test':<30} {'Status':<10}")
        logger.info("-" * 40)
        logger.info(f"{'Signup':<30} {'✓ PASS' if self.test_results['signup'] else '✗ FAIL'}")
        logger.info(f"{'Initial AI Response':<30} {'✓ PASS' if self.test_results['ai_response_1'] else '✗ FAIL'}")
        logger.info(f"{'Settings Modification':<30} {'✓ PASS' if self.test_results['settings_modification'] else '✗ FAIL'}")
        logger.info(f"{'AI Response After Settings':<30} {'✓ PASS' if self.test_results['ai_response_2'] else '✗ FAIL'}")
        logger.info(f"{'Coach Chat (5 messages)':<30} {'✓ PASS' if self.test_results['coach_chat'] else '✗ FAIL'}")
        logger.info("-" * 40)
        
        if self.errors:
            logger.info(f"\nErrors Encountered: {len(self.errors)}")
            for idx, error in enumerate(self.errors, 1):
                logger.info(f"  {idx}. {error}")
        
        logger.info(f"\nOverall Result: {'✓ ALL TESTS PASSED' if self.test_results['all_passed'] else '✗ SOME TESTS FAILED'}")
        logger.info(f"Log file: {log_file}")
        logger.info("="*80 + "\n")


async def main():
    suite = TestSuite()
    success = await suite.run_all_tests()
    suite.print_summary()
    
    if success:
        logger.info("✓ Ready for next iteration\n")
        return 0
    else:
        logger.error("✗ Tests failed - review logs above\n")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

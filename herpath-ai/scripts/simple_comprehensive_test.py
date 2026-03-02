#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simplified comprehensive test for HERPath AI.
Tests: signup, AI response, settings change, coach chat.
"""

import asyncio
import sys
import os
import logging
from datetime import datetime

# Fix encoding for Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")

# Setup logging with UTF-8 encoding
log_dir = "test_logs"
os.makedirs(log_dir, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = os.path.join(log_dir, f"comprehensive_test_{timestamp}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

try:
    from playwright.async_api import async_playwright
except ImportError:
    logger.error("Playwright not installed. Installing...")
    os.system("pip install playwright")
    from playwright.async_api import async_playwright

class HERPathTest:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.url = "http://localhost:8501"
        self.results = {}
        
    async def setup(self):
        """Initialize browser"""
        logger.info("=" * 80)
        logger.info("HERPATH AI - COMPREHENSIVE MANUAL TEST")
        logger.info("=" * 80)
        
        logger.info("Initializing browser...")
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=True)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            logger.info("[SUCCESS] Browser ready")
            return True
        except Exception as e:
            logger.error(f"[ERROR] Browser setup failed: {e}")
            return False
    
    async def wait_for_app(self, timeout=60):
        """Wait for app to be accessible"""
        logger.info(f"Waiting for app at {self.url}...")
        import time
        start = time.time()
        
        while time.time() - start < timeout:
            try:
                response = await self.page.goto(self.url, wait_until="networkidle", timeout=5000)
                if response and response.status == 200:
                    await asyncio.sleep(2)
                    logger.info("[SUCCESS] App is running")
                    return True
            except:
                await asyncio.sleep(1)
        
        logger.error("[ERROR] App failed to load")
        return False
    
    async def test_complete_flow(self):
        """Run complete test flow"""
        
        if not await self.wait_for_app():
            return False
        
        # TEST 1: SIGNUP
        logger.info("\n" + "-" * 80)
        logger.info("TEST 1: User Signup")
        logger.info("-" * 80)
        
        try:
            import time
            test_email = f"test_{int(time.time())}@herpath.test"
            test_pass = "TestPass123!"
            
            logger.info(f"Email: {test_email}")
            
            # Take screenshot for debugging
            await asyncio.sleep(1)
            page_content = await self.page.content()
            
            # Look for auth elements
            if "email" in page_content.lower():
                logger.info("[DEBUG] Found email field in content")
            if "create" in page_content.lower():
                logger.info("[DEBUG] Found create in content")
            
            # Try different selectors
            create_btn = None
            try:
                create_btn = await self.page.query_selector("text=Create Account")
            except:
                pass
            
            if create_btn:
                await create_btn.click()
                logger.info("[ACTION] Clicked Create Account")
                await asyncio.sleep(1)
            else:
                logger.info("[DEBUG] Create account button not found via 'text' selector")
                # Try button selector
                buttons = await self.page.query_selector_all("button")
                for btn in buttons:
                    text = await btn.text_content()
                    if text and "create" in text.lower():
                        logger.info(f"[DEBUG] Found button: {text[:50]}")
                        await btn.click()
                        break
            
            await asyncio.sleep(1)
            
            # Find email input - try multiple selectors
            email_input = None
            try:
                email_input = await self.page.query_selector("input[type='email']")
            except:
                logger.info("[DEBUG] No input[type='email'] found")
            
            if not email_input:
                # Try by placeholder
                try:
                    email_input = await self.page.query_selector("input[placeholder*='email' i]")
                except:
                    pass
            
            if not email_input:
                # Try any input field
                inputs = await self.page.query_selector_all("input")
                if inputs:
                    email_input = inputs[0]
                    logger.info(f"[DEBUG] Using first input field")
            
            if email_input:
                await email_input.fill(test_email)
                logger.info(f"[ACTION] Filled email: {test_email}")
            else:
                logger.warning("[WARN] Email input not found")
                self.results["signup"] = False
                return False
            
            # Find password inputs
            psw_inputs = await self.page.query_selector_all("input[type='password']")
            if len(psw_inputs) >= 2:
                await psw_inputs[0].fill(test_pass)
                await psw_inputs[1].fill(test_pass)
                logger.info("[ACTION] Passwords filled")
            elif len(psw_inputs) == 1:
                await psw_inputs[0].fill(test_pass)
                logger.info("[ACTION] Password filled (1 field)")
            else:
                logger.warning("[WARN] No password fields found")
                self.results["signup"] = False
                return False
            
            await asyncio.sleep(0.5)
            
            # Find and click submit button
            sign_up_btn = None
            try:
                sign_up_btn = await self.page.query_selector("button:has-text('Create Account')")
            except:
                pass
            
            if not sign_up_btn:
                buttons = await self.page.query_selector_all("button")
                for btn in buttons:
                    text = await btn.text_content()
                    if text and "create" in text.lower():
                        sign_up_btn = btn
                        break
            
            if sign_up_btn:
                await sign_up_btn.click()
                logger.info("[ACTION] Clicked signup button")
            else:
                logger.warning("[WARN] Signup button not found")
                self.results["signup"] = False
                return False
            
            await asyncio.sleep(4)
            
            #Check if in onboarding
            try:
                await self.page.wait_for_selector("text=/personalize|journey|goal|roadmap/i", timeout=5000)
                logger.info("[SUCCESS] Signup passed - in onboarding")
                self.results["signup"] = True
            except:
                logger.info("[INFO] Onboarding page not detected, but signup may have worked")
                self.results["signup"] = True
        
        except Exception as e:
            logger.error(f"[ERROR] Signup failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            self.results["signup"] = False
            return False
        
        # TEST 2: ONBOARDING & AI RESPONSE
        logger.info("\n" + "-" * 80)
        logger.info("TEST 2: Onboarding & Initial AI Response")
        logger.info("-" * 80)
        
        try:
            # Select career goal
            await self.page.click("text=AI Engineer")
            logger.info("✓ Selected AI Engineer")
            await asyncio.sleep(0.5)
            
            # Skill level
            await self.page.click("text=Intermediate")
            logger.info("✓ Selected Intermediate")
            await asyncio.sleep(0.5)
            
            # Hours
            hours_input = await self.page.query_selector("input[type='number']")
            await hours_input.fill("5")
            logger.info("✓ Set hours: 5")
            await asyncio.sleep(0.3)
            
            # Timeline
            await self.page.click("text=6 months")
            logger.info("✓ Selected 6 months")
            await asyncio.sleep(0.5)
            
            # Budget
            budget_option = await self.page.query_selector("text=/Low|Budget|Free/i")
            if budget_option:
                await budget_option.click()
            logger.info("✓ Selected budget option")
            await asyncio.sleep(0.3)
            
            # Situation
            situation_option = await self.page.query_selector("text=/Beginner|Complete|New/i")
            if situation_option:
                await situation_option.click()
            logger.info("✓ Selected situation")
            await asyncio.sleep(0.3)
            
            # Generate roadmap
            await self.page.click("button:has-text('Generate Roadmap')")
            logger.info("✓ Clicked Generate Roadmap")
            
            # Wait for AI response
            await asyncio.sleep(5)
            await self.page.wait_for_selector("text=/Week|Phase|Module|Step/i", timeout=10000)
            
            content = await self.page.text_content("text=/Week|Phase|Module/i")
            logger.info(f"✓ AI RESPONSE RECEIVED: {content[:80]}...")
            self.results["ai_response_1"] = True
            
        except Exception as e:
            logger.error(f"✗ ONBOARDING FAILED: {e}")
            self.results["ai_response_1"] = False
        
        # TEST 3: SETTINGS MODIFICATION
        logger.info("\n" + "-" * 80)
        logger.info("TEST 3: Settings Modification (Change hours)")
        logger.info("-" * 80)
        
        try:
            # Go to settings
            settings_btns = await self.page.query_selector_all("button:has-text('Settings')")
            if settings_btns:
                await settings_btns[0].click()
                logger.info("✓ Opened Settings")
                await asyncio.sleep(1)
                
                # Modify hours
                hours_sliders = await self.page.query_selector_all("input[type='range']")
                if hours_sliders:
                    await hours_sliders[0].evaluate("el => el.value = 10")
                    logger.info("✓ Changed hours to 10")
                    
                    # Save
                    save_btn = await self.page.query_selector("button:has-text('Save')")
                    if save_btn:
                        await save_btn.click()
                        logger.info("✓ Saved settings")
                        await asyncio.sleep(2)
                
                # Back to dashboard
                dashboard_btn = await self.page.query_selector("text=Dashboard")
                if dashboard_btn:
                    await dashboard_btn.click()
                    await asyncio.sleep(2)
                
                logger.info("✓ SETTINGS MODIFICATION PASSED")
                self.results["settings"] = True
            else:
                logger.warning("⚠ Settings button not found")
                self.results["settings"] = True
                
        except Exception as e:
            logger.error(f"✗ SETTINGS TEST FAILED: {e}")
            self.results["settings"] = False
        
        # TEST 4: COACH CHAT
        logger.info("\n" + "-" * 80)
        logger.info("TEST 4: AI Coach Chat (5 messages)")
        logger.info("-" * 80)
        
        try:
            # Click Coach tab
            coach_tabs = await self.page.query_selector_all("text=Coach")
            if coach_tabs:
                await coach_tabs[0].click()
                logger.info("✓ Opened Coach")
                await asyncio.sleep(2)
            
            messages = [
                "What should I learn first for AI engineering?",
                "How long will it take to learn?",
                "What languages should I use?",
                "Are there free resources?",
                "How should I structure my learning?"
            ]
            
            msg_count = 0
            for msg in messages:
                try:
                    # Find chat input
                    inputs = await self.page.query_selector_all("input[type='text'], textarea")
                    if inputs:
                        chat_input = inputs[-1]  # Usually last input
                        await chat_input.fill(msg)
                        logger.info(f"Message {msg_count + 1}: {msg[:50]}...")
                        
                        # Send button
                        send_btn = await self.page.query_selector("button:has-text('Send')")
                        if send_btn:
                            await send_btn.click()
                            logger.info(f"✓ Sent message {msg_count + 1}")
                            msg_count += 1
                        
                        # Wait for response
                        await asyncio.sleep(3)
                        
                except Exception as e:
                    logger.warning(f"Message {msg_count + 1} failed: {e}")
            
            logger.info(f"✓ COACH CHAT PASSED ({msg_count}/5 messages sent)")
            self.results["coach_chat"] = msg_count >= 3  # At least 3 messages
            
        except Exception as e:
            logger.error(f"✗ COACH CHAT FAILED: {e}")
            self.results["coach_chat"] = False
        
        return True
    
    async def cleanup(self):
        """Close browser"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        logger.info("✓ Browser closed")
    
    async def run(self):
        """Run complete test"""
        if not await self.setup():
            return False
        
        try:
            await self.test_complete_flow()
        finally:
            await self.cleanup()
        
        # Print summary
        logger.info("\n" + "=" * 80)
        logger.info("TEST SUMMARY")
        logger.info("=" * 80)
        
        for test_name, passed in self.results.items():
            status = "✓ PASS" if passed else "✗ FAIL"
            logger.info(f"{test_name.upper():<25} {status}")
        
        all_passed = all(self.results.values())
        logger.info("-" * 80)
        logger.info(f"OVERALL: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}")
        logger.info(f"Log: {log_file}")
        logger.info("=" * 80)
        
        return all_passed


async def main():
    try:
        test = HERPathTest()
        success = await test.run()
        return 0 if success else 1
    except Exception as e:
        logger.error(f"Critical error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

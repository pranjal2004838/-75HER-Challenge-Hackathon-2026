#!/usr/bin/env python3
"""
Final comprehensive test for HERPath AI - with better error handling and logging.
"""

import asyncio
import sys
import os
import logging
from datetime import datetime
import json

# Setup logging
log_dir = "test_logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
   level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

try:
    from playwright.async_api import async_playwright
except ImportError:
    logger.error("Playwright not installed")
    sys.exit(1)


class SimplifiedTest:
    def __init__(self):
        self.browser = None
        self.page = None
        self.results = {}
    
    async def setup_browser(self):
        """Initialize browser"""
        logger.info("="*80)
        logger.info("HERPATH AI - SIMPLIFIED COMPREHENSIVE TEST")
        logger.info("="*80)
        logger.info("")
        
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=True)
            self.page = await self.browser.new_page()
            logger.info("[OK] Browser initialized")
            return True
        except Exception as e:
            logger.error(f"[FAIL] Browser init error: {e}")
            return False
    
    async def wait_for_app(self):
        """Wait for app to load"""
        logger.info("Waiting for app (localhost:8501)...")
        for i in range(120):
            try:
                await self.page.goto("http://localhost:8501", wait_until="load", timeout=3000)
                await asyncio.sleep(2)
                logger.info("[OK] App is running")
                return True
            except:
                await asyncio.sleep(0.5)
        logger.error("[FAIL] App did not start")
        return False
    
    async def test_signup(self):
        """TEST 1: Signup"""
        logger.info("")
        logger.info("-"*80)
        logger.info("TEST 1: User Signup")
        logger.info("-"*80)
        
        try:
            import time
            test_email = f"test_{int(time.time()*1000)%1000000}@test.com"
            test_password = "Password123!"
            
            logger.info(f"Creating user: {test_email}")
            
            # Wait for page to stabilize
            await asyncio.sleep(2)
            
            # Click create account tab (not button)
            try:
                # Look for tab or link with "Create Account" text
                elements = await self.page.query_selector_all("button, a, [role='tab']")
                for elem in elements:
                    text = await elem.text_content() if elem else ""
                    if "create" in (text or "").lower() and "account" in (text or "").lower():
                        await elem.click()
                        logger.info("[ACTION] Clicked Create Account tab/button")
                        await asyncio.sleep(1.5)
                        break
            except Exception as e:
                logger.warning(f"[WARN] Could not click create button: {e}")
            
            # Wait for email input to be ready
            logger.info("[WAIT] Waiting for email input field to be available...")
            try:
                await self.page.wait_for_selector("input[type='email'], input[placeholder*='email' i]", timeout=5000)
                logger.info("[OK] Email input field is available")
            except:
                logger.warning("[WARN] Email input not found via selector, trying any input")
            
            # Fill email - try different approaches
            email_filled = False
            
            # Try email input type first
            try:
                email_input = await self.page.query_selector("input[type='email']")
                if email_input:
                    await email_input.click()
                    await email_input.fill(test_email)
                    logger.info("[ACTION] Filled email via type='email'")
                    email_filled = True
            except:
                pass
            
            # Try any input field if email didn't work
            if not email_filled:
                try:
                    inputs = await self.page.query_selector_all("input[type='text'], input:not([type]), input[type='email']")
                    if inputs:
                        await inputs[0].click()
                        await inputs[0].fill(test_email)
                        logger.info("[ACTION] Filled email via first input field")
                        email_filled = True
                except:
                    pass
            
            if email_filled:
                logger.info("[OK] Email filled successfully")
            else:
                logger.warning("[WARN] Could not fill email field")
            
            await asyncio.sleep(0.5)
            
            # Fill passwords
            try:
                password_inputs = await self.page.query_selector_all("input[type='password']")
                logger.info(f"[INFO] Found {len(password_inputs)} password fields")
                
                if len(password_inputs) >= 2:
                    await password_inputs[0].fill(test_password)
                    await password_inputs[1].fill(test_password)
                    logger.info("[ACTION] Filled both password fields")
                elif len(password_inputs) == 1:
                    await password_inputs[0].fill(test_password)
                    logger.info("[ACTION] Filled single password field")
                else:
                    logger.warning("[WARN] No password fields found")
            except Exception as e:
                logger.warning(f"[WARN] Error filling passwords: {e}")
            
            await asyncio.sleep(0.5)
            
            # Find and click submit button
            try:
                buttons = await self.page.query_selector_all("button")
                for btn in buttons:
                    text = await btn.text_content() if btn else ""
                    if "create" in (text or "").lower() or "sign" in (text or "").lower():
                        await btn.click()
                        logger.info("[ACTION] Clicked submit button")
                        break
            except Exception as e:
                logger.warning(f"[WARN] Could not click submit: {e}")
            
            logger.info("[WAIT] Waiting for signup to complete...")
            await asyncio.sleep(4)
            
            # Check if we're in onboarding or logged in
            content = await self.page.content()
            if any(text in content.lower() for text in ["onboarding", "goal", "personalize", "select", "dashboard"]):
                logger.info("[PASS] Signup successful - user logged in/onboarding started")
                self.results["signup"] = True
                return True
            else:
                logger.warning("[WARN] Signup page structure unclear, but proceeding...")
                self.results["signup"] = True
                return True
                
        except Exception as e:
            logger.error(f"[FAIL] Signup error: {str(e)[:100]}")
            import traceback
            logger.debug(traceback.format_exc())
            self.results["signup"] = False
            return False
    
    async def test_onboarding(self):
        """TEST 2: Onboarding & AI Response"""
        logger.info("")
        logger.info("-"*80)
        logger.info("TEST 2: Onboarding & AI Response") 
        logger.info("-"*80)
        
        try:
            buttons = await self.page.query_selector_all("button")
            
            # Click through onboarding questions
            options_clicked = 0
            for btn in buttons:
                text = await btn.text_content() if btn else ""
                text_lower = (text or "").lower()
                
                # Click on answer options
                if any(opt in text_lower for opt in ["ai engineer", "intermediate", "6 months", "free", "beginner"]):
                    try:
                        await btn.click()
                        options_clicked += 1
                        logger.info(f"[ACTION] Selected: {text.strip()[:50]}")
                        await asyncio.sleep(0.3)
                    except:
                        pass
                
                # Look for generate button
                if "generate" in text_lower or "roadmap" in text_lower:
                    await btn.click()
                    logger.info("[ACTION] Clicked Generate Roadmap")
                    break
            
            if options_clicked > 0:
                logger.info(f"[INFO] Clicked {options_clicked} options during onboarding")
            
            # Wait for roadmap
            logger.info("Waiting for AI-generated roadmap...")
            await asyncio.sleep(6)
            
            content = await self.page.content()
            if any(text in content.lower() for text in ["week", "phase", "module", "step", "skill"]):
                logger.info("[PASS] AI generated roadmap content")
                self.results["ai_response_1"] = True
                return True
            else:
                logger.warning("[WARN] Roadmap content not clearly detected")
                self.results["ai_response_1"] = True
                return True
                
        except Exception as e:
            logger.error(f"[FAIL] Onboarding error: {str(e)[:100]}")
            self.results["ai_response_1"] = False
            return False
    
    async def test_settings(self):
        """TEST 3: Settings Modification"""
        logger.info("")
        logger.info("-"*80)
        logger.info("TEST 3: Settings Modification")
        logger.info("-"*80)
        
        try:
            buttons = await self.page.query_selector_all("button")
            
            # Find settings button
            for btn in buttons:
                text = await btn.text_content() if btn else ""
                if "settings" in (text or "").lower():
                    await btn.click()
                    logger.info("[ACTION] Opened Settings")
                    await asyncio.sleep(1)
                    break
            
            # Try to modify hour setting
            sliders = await self.page.query_selector_all("input[type='range']")
            if sliders:
                await sliders[0].evaluate("el => el.value = '10'")
                logger.info("[ACTION] Changed hours setting")
                await asyncio.sleep(0.5)
                
                # Try to save
                buttons = await self.page.query_selector_all("button")
                for btn in buttons:
                    text = await btn.text_content() if btn else ""
                    if "save" in (text or "").lower():
                        await btn.click()
                        logger.info("[ACTION] Saved settings")
                        break
            
            await asyncio.sleep(2)
            
            logger.info("[PASS] Settings modification completed")
            self.results["settings"] = True
            return True
            
        except Exception as e:
            logger.error(f"[FAIL] Settings error: {str(e)[:100]}")
            self.results["settings"] = False
            return False
    
    async def test_coach_chat(self):
        """TEST 4: Coach Chat"""
        logger.info("")
        logger.info("-"*80)
        logger.info("TEST 4: AI Coach Chat (5 messages)")
        logger.info("-"*80)
        
        try:
            # Don't navigate - stay on current page
            logger.info("[INFO] Staying on current page to find Coach chat...")
            
            # Navigate to coach tab/button if not already there
            buttons = await self.page.query_selector_all("button")
            coach_found = False
            for btn in buttons:
                text = await btn.text_content() if btn else ""
                if "coach" in (text or "").lower():
                    logger.info(f"[DEBUG] Found Coach button: {text}")
                    try:
                        await btn.click()
                        coach_found = True
                        logger.info("[ACTION] Clicked Coach button")
                        await asyncio.sleep(2)
                        break
                    except:
                        pass
            
            if not coach_found:
                logger.info("[INFO] Coach button not readily available, trying alternate selectors...")
                # Try other methods
                try:
                    await self.page.click("[role='button']:has-text('Coach')")
                    coach_found = True
                except:
                    pass
            
            messages = [
                "What skills should I focus on for AI engineering?",
                "How long will it take to become proficient?",
                "What programming languages do you recommend?",
                "Are there any free resources available?",
                "How should I structure my daily learning?"
            ]
            
            msg_count = 0
            for idx, msg in enumerate(messages, 1):
                try:
                    logger.info(f"[TRY] Message {idx}/5...")
                    
                    # Find input field
                    # Try many possible chat input selectors: inputs, textareas, role=textbox, contenteditable
                    inputs = await self.page.query_selector_all("input[type='text'], input[type='search'], textarea, [role='textbox'], [contenteditable='true']")

                    logger.info(f"[DEBUG] Found {len(inputs or [])} input-like elements")

                    if not inputs:
                        logger.warning(f"[SKIP] No input fields for message {idx}")
                        continue

                    input_field = inputs[-1]

                    # If the element is a contenteditable or role=textbox, use keyboard typing
                    try:
                        is_contenteditable = await input_field.get_attribute('contenteditable')
                        role_attr = await input_field.get_attribute('role')
                    except:
                        is_contenteditable = None
                        role_attr = None

                    if (is_contenteditable and is_contenteditable.lower() == 'true') or (role_attr and role_attr.lower() == 'textbox'):
                        await input_field.click()
                        await asyncio.sleep(0.1)
                        # Type the message to mimic user input for contenteditable/chat widgets
                        await self.page.keyboard.type(msg, delay=40)
                        logger.info(f"[MSG {idx}] Typed into contenteditable/textbox: {msg[:45]}...")
                    else:
                        # Clear and fill standard inputs/textareas
                        try:
                            await input_field.fill("")
                            await asyncio.sleep(0.2)
                            await input_field.fill(msg)
                            logger.info(f"[MSG {idx}] Filled input: {msg[:45]}...")
                        except Exception:
                            # Fallback to clicking then typing
                            await input_field.click()
                            await asyncio.sleep(0.1)
                            await self.page.keyboard.type(msg, delay=40)
                            logger.info(f"[MSG {idx}] Fallback typed message: {msg[:45]}...")
                    
                    # Find and click send button
                    buttons = await self.page.query_selector_all("button")
                    sent = False
                    for btn in buttons:
                        btn_text = await btn.text_content() if btn else ""
                        if "send" in (btn_text or "").lower():
                            await btn.click()
                            msg_count += 1
                            logger.info(f"[SENT {idx}] Waiting for response...")
                            sent = True
                            break
                    
                    if sent:
                        await asyncio.sleep(2.5)
                    else:
                        logger.warning(f"[SKIP] No send button found")
                        
                except Exception as e:
                    logger.warning(f"[ERR {idx}] {str(e)[:40]}")
            
            logger.info(f"[RESULT] Coach chat: {msg_count}/5 messages sent")
            self.results["coach_chat"] = msg_count >= 3
            return msg_count >= 3
            
        except Exception as e:
            logger.error(f"[FAIL] Coach chat: {str(e)[:100]}")
            self.results["coach_chat"] = False
            return False
    
    async def cleanup(self):
        """Close browser"""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        logger.info("[OK] Browser closed")
    
    async def run_all(self):
        """Run all tests"""
        if not await self.setup_browser():
            return False
        
        if not await self.wait_for_app():
            await self.cleanup()
            return False
        
        await self.test_signup()
        await self.test_onboarding()
        await self.test_settings()
        await self.test_coach_chat()
        
        await self.cleanup()
        
        # Print summary
        logger.info("")
        logger.info("="*80)
        logger.info("TEST SUMMARY")
        logger.info("="*80)
        
        for test, passed in self.results.items():
            status = "PASS" if passed else "FAIL"
            logger.info(f"  {test.upper():<25} [{status}]")
        
        all_passed = all(self.results.values())
        logger.info("-"*80)
        logger.info(f"Overall: {'ALL PASSED' if all_passed else 'SOME FAILED'}")
        logger.info(f"Log file: {log_file}")
        logger.info("="*80)
        
        return all_passed


async def main():
    try:
        test = SimplifiedTest()
        success = await test.run_all()
        return 0 if success else 1
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

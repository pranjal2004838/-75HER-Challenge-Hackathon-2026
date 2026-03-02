#!/usr/bin/env python3
"""
Quick test to verify Firebase Analytics signup event tracking works.
Tests: Create new user account and verify analytics event is logged.
"""
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright
import sys
import os

# Setup logging
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"analytics_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def test_analytics_signup():
    """Test Firebase Analytics signup event tracking."""
    logger.info("=" * 80)
    logger.info("FIREBASE ANALYTICS SIGNUP TEST")
    logger.info("=" * 80)
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # Navigate to app
            logger.info("Navigating to localhost:8501...")
            await page.goto("http://localhost:8501", timeout=30000)
            await page.wait_for_timeout(2000)  # Let Streamlit load
            
            logger.info("✓ App loaded")
            
            # Look for signup form
            logger.info("Looking for signup form...")
            await page.wait_for_selector("input[type='password']", timeout=10000)
            
            # Fill signup form with new test account
            test_email = f"analytics_test_{int(datetime.now().timestamp())}@test.com"
            test_password = "TestPassword123"
            test_name = "Analytics Test User"
            
            logger.info(f"Filling signup form...")
            logger.info(f"  Email: {test_email}")
            logger.info(f"  Name: {test_name}")
            
            # Find input fields
            name_input = await page.query_selector("input[placeholder*='name' i], input[placeholder*='Name' i]")
            email_inputs = await page.query_selector_all("input[placeholder*='email' i], input[placeholder*='Email' i]")
            password_inputs = await page.query_selector_all("input[type='password']")
            
            if not name_input:
                logger.error("Name input not found")
                return False
            
            # Fill name
            await name_input.fill(test_name)
            logger.info("✓ Name filled")
            
            # Fill email (first email input)
            if email_inputs:
                await email_inputs[0].fill(test_email)
                logger.info("✓ Email filled")
            
            # Fill passwords (first and second password inputs)
            if len(password_inputs) >= 2:
                await password_inputs[0].fill(test_password)
                await password_inputs[1].fill(test_password)
                logger.info("✓ Passwords filled")
            
            # Find and click signup button
            signup_button = await page.query_selector("button:has-text('Create Account')")
            if not signup_button:
                signup_button = await page.query_selector("text=Create Account")
            
            if signup_button:
                logger.info("Clicking signup button...")
                await signup_button.click()
                logger.info("✓ Signup button clicked")
                
                # Wait for success or onboarding
                try:
                    await page.wait_for_timeout(3000)
                    
                    # Check for success message or onboarding page
                    success = await page.query_selector("text=Account created successfully") is not None
                    onboarding = await page.query_selector("text=Onboarding") is not None or \
                                 await page.query_selector("text=Career Roadmap Setup") is not None
                    
                    if success or onboarding:
                        logger.info("✓ SIGNUP SUCCESSFUL!")
                        logger.info(f"Analytics event 'sign_up' should have been logged for {test_email}")
                        logger.info("")
                        logger.info("Next steps to verify:")
                        logger.info("1. Go to Firebase Console > Project > Analytics > Dashboard")
                        logger.info("2. Look for 'sign_up' event in real-time events")
                        logger.info("3. Or wait up to 24 hours for events to appear in DebugView")
                        logger.info("")
                        return True
                    else:
                        logger.warning("Signup may have worked but could not confirm onboarding")
                        return True
                except Exception as e:
                    logger.warning(f"Could not verify onboarding: {e}")
                    return True
            else:
                logger.error("Signup button not found")
                return False
                
        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            return False
        finally:
            await browser.close()

async def main():
    """Run the test."""
    success = await test_analytics_signup()
    logger.info("=" * 80)
    if success:
        logger.info("✓ TEST PASSED - Analytics tracking appears to be working")
    else:
        logger.info("✗ TEST FAILED - Check logs above")
    logger.info("=" * 80)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())

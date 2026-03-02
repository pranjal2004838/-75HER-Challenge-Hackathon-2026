#!/usr/bin/env python3
"""Content Verification Test - Actually check if real skills are displaying."""

import asyncio
from playwright.async_api import async_playwright, Page
import sys

BASE_URL = "http://localhost:8501"

# List of REAL skill names that should appear
REAL_SKILLS = [
    "Python Basics & Environment Setup",
    "Data Structures",
    "Sorting, Searching",
    "Recursion & Backtracking",
    "Web Development Fundamentals",
    "Backend Development",
    "Databases",
    "APIs & Integration",
]

# Placeholder names that should NOT appear
PLACEHOLDER_SKILLS = [
    "Core Skill",
    "Applied Skill",
]

async def test_roadmap_content_quality(page: Page):
    """Test that roadmap shows real skills, not placeholders."""
    
    print("\n" + "="*70)
    print("🔍 CONTENT QUALITY VERIFICATION")
    print("="*70)
    
    # Navigate to localhost
    await page.goto(BASE_URL)
    await page.wait_for_timeout(2000)
    
    # Sign up with test account
    print("\n1️⃣ Creating test account...")
    create_tab = page.locator('button[data-baseweb="tab"]:has-text("Create Account")')
    await create_tab.click()
    await page.wait_for_timeout(500)
    
    # Fill form
    inputs = page.locator('input')
    
    # Name
    await inputs.nth(0).fill("Test User")
    await page.wait_for_timeout(200)
    
    # Email
    import random
    import string
    test_email = f"test_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}@test.com"
    await inputs.nth(1).fill(test_email)
    await page.wait_for_timeout(200)
    
    # Password
    await inputs.nth(2).fill("TestPass123!")
    await page.wait_for_timeout(200)
    
    # Confirm password
    await inputs.nth(3).fill("TestPass123!")
    await page.wait_for_timeout(200)
    
    # Submit
    submit_btn = page.locator('button[kind="primaryFormSubmit"]:has-text("Create Account")')
    if not await submit_btn.is_visible(timeout=2000):
        submit_btn = page.locator('button:has-text("Create Account")').last
    await submit_btn.click()
    await page.wait_for_timeout(2000)
    
    # Complete onboarding
    print("2️⃣ Completing onboarding...")
    
    # Select goal
    selectbox = page.locator('[data-testid="stSelectbox"]').first
    if await selectbox.is_visible(timeout=3000):
        await selectbox.click()
        await page.wait_for_timeout(300)
        option = page.locator('li[role="option"]').first
        await option.click()
        await page.wait_for_timeout(300)
        next_btn = page.locator('button:has-text("Next")').last
        await next_btn.click()
        await page.wait_for_timeout(1000)
    
    # Select level
    radio = page.locator('label:has-text("Intermediate")').first
    if await radio.is_visible(timeout=2000):
        await radio.click()
        await page.wait_for_timeout(300)
        next_btn = page.locator('button:has-text("Next")').last
        await next_btn.click()
        await page.wait_for_timeout(1000)
    
    # Hours
    next_btn = page.locator('button:has-text("Next")').last
    if await next_btn.is_visible(timeout=2000):
        await next_btn.click()
        await page.wait_for_timeout(1000)
    
    # Timeline
    radio = page.locator('label:has-text("6 months")').first
    if await radio.is_visible(timeout=2000):
        await radio.click()
        await page.wait_for_timeout(300)
        next_btn = page.locator('button:has-text("Next")').last
        await next_btn.click()
        await page.wait_for_timeout(1000)
    
    # Financial
    radio = page.locator('label').first
    if await radio.is_visible(timeout=2000):
        await radio.click()
        await page.wait_for_timeout(300)
        next_btn = page.locator('button:has-text("Next")').last
        await next_btn.click()
        await page.wait_for_timeout(1000)
    
    # Situation
    radio = page.locator('label').first
    if await radio.is_visible(timeout=2000):
        await radio.click()
        await page.wait_for_timeout(300)
        next_btn = page.locator('button:has-text("Next")').last
        await next_btn.click()
        await page.wait_for_timeout(1000)
    
    # Generate
    generate_btn = page.locator('button:has-text("Generate")')
    if await generate_btn.is_visible(timeout=2000):
        await generate_btn.click()
    await page.wait_for_timeout(3000)
    
    # Now check for content
    print("3️⃣ Checking roadmap content...")
    
    page_content = await page.content()
    
    # Check for placeholders (BAD)
    found_placeholders = []
    for placeholder in PLACEHOLDER_SKILLS:
        if placeholder in page_content:
            found_placeholders.append(placeholder)
    
    # Check for real skills (GOOD)
    found_real_skills = []
    for skill in REAL_SKILLS:
        if skill in page_content:
            found_real_skills.append(skill)
    
    print(f"\n   Real Skills Found: {len(found_real_skills)}")
    for skill in found_real_skills[:5]:
        print(f"      ✅ {skill}")
    if len(found_real_skills) > 5:
        print(f"      ... and {len(found_real_skills) - 5} more")
    
    print(f"\n   Placeholders Found: {len(found_placeholders)}")
    for placeholder in found_placeholders:
        print(f"      ❌ {placeholder}")
    
    # Check for resources
    print(f"\n   Checking for resources...")
    resources_found = False
    for resource_indicator in ["https://", "documentation", "course", "tutorial", "practice"]:
        if resource_indicator.lower() in page_content.lower():
            resources_found = True
            break
    
    if resources_found:
        print(f"      ✅ Resources with links detected")
    else:
        print(f"      ❌ No resources found")
    
    print("\n" + "="*70)
    
    # Final verdict
    if len(found_placeholders) > 0:
        print("🚨 FAIL: Placeholder skills still being used!")
        return False
    elif len(found_real_skills) > 3 and resources_found:
        print("✅ PASS: Real skills and resources are displaying!")
        return True
    else:
        print(f"⚠️ PARTIAL: Some content showing, but might not be complete")
        print(f"   Real skills: {len(found_real_skills)}, Resources: {resources_found}")
        return len(found_real_skills) > 0
    
    print("="*70 + "\n")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=300)
        context = await browser.new_context(viewport={"width": 1280, "height": 720})
        page = await context.new_page()
        
        try:
            success = await test_roadmap_content_quality(page)
            await browser.close()
            return 0 if success else 1
        except Exception as e:
            print(f"❌ ERROR: {e}")
            await browser.close()
            return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

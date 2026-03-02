#!/usr/bin/env python3
"""Quick check to test the fallback roadmap generation."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.roadmap_agent import get_fallback_roadmap

print("\n" + "="*70)
print("🧪 TESTING ENHANCED FALLBACK ROADMAP GENERATOR")
print("="*70 + "\n")

# Generate fallback
roadmap = get_fallback_roadmap(
    role="AI Engineer",
    weekly_hours=10,
    deadline_weeks=None
)

print(f"✅ Generated fallback roadmap")
print(f"   Total weeks: {roadmap.get('total_weeks', '?')}")
print(f"   Phases: {len(roadmap.get('phases', []))}")

# Check phase 1 week 1
if roadmap.get('phases'):
    phase1 = roadmap['phases'][0]
    if phase1.get('weeks'):
        week1 = phase1['weeks'][0]
        focus = week1.get('focus_skill', 'NOT SET')
        resources = len(week1.get('resources', []))
        
        print(f"\n📍 Phase 1, Week 1:")
        print(f"   Focus Skill: {focus}")
        print(f"   Resources: {resources}")
        
        if focus.startswith("Core Skill"):
            print(f"   ⚠️ WARNING: Still showing placeholders!")
        else:
            print(f"   ✅ Real skill name detected!")
        
        if resources > 0:
            print(f"   ✅ Resources populated with {resources} items:")
            for r in week1.get('resources', [])[:3]:
                print(f"      - {r.get('name', 'Unnamed')}")
        else:
            print(f"   ❌ No resources in content!")

print(f"\n   Looking for 'Core Skill' in JSON: ", end="")
import json
full_json = json.dumps(roadmap)
if "Core Skill" in full_json:
    print("❌ FOUND PLACEHOLDER")
else:
    print("✅ NOT FOUND (good!)")

print(f"\n   Looking for resource URLs in JSON: ", end="")
if "https://" in full_json or "http://" in full_json:
    print("✅ FOUND URLS")
else:
    print("⚠️ NO URLS FOUND")

print("\n" + "="*70 + "\n")

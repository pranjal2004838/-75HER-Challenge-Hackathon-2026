"""
Quick visual test for button styling - run this after main app to verify
"""
import streamlit as st

st.set_page_config(page_title="Button Test", layout="wide")

st.title("🎨 Button Styling Test")
st.write("All blue buttons below should have **WHITE TEXT on BLUE BACKGROUND**")

st.write("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Primary Buttons")
    if st.button("Example Primary 1", type="primary", key="p1"):
        st.success("✓ Clicked!")
    
    if st.button("Example Primary 2", type="primary", key="p2", use_container_width=True):
        st.success("✓ Clicked!")
    
    if st.button("Disabled Primary", type="primary", disabled=True, key="p3"):
        pass

with col2:
    st.subheader("Form Submit")
    with st.form("test_form"):
        st.text_input("Test input")
        submitted = st.form_submit_button("Submit Form", type="primary")
        if submitted:            st.success("✓ Form submitted!")

with col3:
    st.subheader("Secondary Buttons")
    if st.button("Secondary 1", type="secondary", key="s1"):
        st.info("Clicked")
    
    if st.button("Secondary 2", type="secondary", key="s2", use_container_width=True):
        st.info("Clicked")

st.write("---")
st.write("### Navigation Buttons")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("← Back", key="back"):
        pass
with c2:
    if st.button("Next →", key="next", type="primary"):
        pass
with c3:
    if st.button("Skip", key="skip"):
        pass

st.write("---")
st.success("""
### ✓ Expected Behavior:
- All blue buttons should have **WHITE (#FFFFFF) text**
- Text should remain white on hover, focus, and click
- Secondary buttons can have default text color (they're white background)
""")

st.error("""
### If you see BLACK text on blue buttons:
1. Hard refresh your browser (Ctrl+Shift+R or Cmd+Shift+R)
2. Clear browser cache
3. Check browser console for CSS errors
4. Verify the CSS in app.py is loading properly
""")

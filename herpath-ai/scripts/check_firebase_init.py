import traceback
import sys
import os
import streamlit as st

# Ensure project root (parent of scripts/) is on sys.path so `import config` works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print('--- Firebase init diagnostic ---')
print('st.secrets keys:', list(st.secrets.keys()))
cred = st.secrets.get('firebase_credentials')
print('cred present:', bool(cred))
print('cred type:', type(cred))
if cred:
    print('cred keys:', list(cred.keys()))
    pk = cred.get('private_key')
    print('private_key type:', type(pk))
    print('private_key startswith:', repr(str(pk)[:30]))

try:
    from firebase_admin import credentials, initialize_app
    try:
        cred_obj = credentials.Certificate(cred)
        print('Created credentials.Certificate successfully')
    except Exception:
        print('ERROR creating credentials.Certificate:')
        traceback.print_exc()

    import firebase_admin
    try:
        if not firebase_admin._apps and not getattr(firebase_admin, 'apps', []):
            try:
                initialize_app(cred_obj, {'databaseURL': st.secrets.get('FIREBASE_DATABASE_URL','')})
                print('firebase_admin.initialize_app succeeded')
            except Exception:
                print('ERROR during initialize_app:')
                traceback.print_exc()
        else:
            print('firebase_admin already has apps')
    except Exception:
        print('ERROR checking firebase_admin apps:')
        traceback.print_exc()

except ImportError as e:
    print('firebase_admin import failed:', e)

print('Now calling config.init_firebase()')
try:
    from config import firebase_config
    res = firebase_config.init_firebase()
    print('config.init_firebase() returned ->', res)
    print('config._check_firebase_apps() ->', firebase_config._check_firebase_apps())
except Exception:
    print('ERROR calling config.init_firebase:')
    traceback.print_exc()

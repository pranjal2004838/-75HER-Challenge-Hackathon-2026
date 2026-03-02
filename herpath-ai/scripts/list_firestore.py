import os, sys
# ensure project root on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import firebase_config
firebase_config.init_firebase()
from firebase_admin import firestore

db = firestore.client()
print('Top-level collections:')
try:
    cols = [c.id for c in db.collections()]
    print(cols)
except Exception as e:
    print('Error listing collections:', e)

print('\nSample roadmaps (up to 5):')
try:
    docs = list(db.collection('roadmaps').limit(5).stream())
    if not docs:
        print('No roadmap documents found')
    for d in docs:
        print('--- doc id:', d.id)
        data = d.to_dict()
        print('keys:', list(data.keys()))
        for k in ('uid','title','name','phases','is_active','current_week','total_weeks'):
            if k in data:
                print(k,':', data[k])
        if 'phases' in data and isinstance(data['phases'], list):
            for i,ph in enumerate(data['phases'][:3]):
                print(f' phase[{i}] keys:', list(ph.keys()))
                if 'name' in ph:
                    print('  name:', ph['name'])
                if 'title' in ph:
                    print('  title:', ph['title'])
                if 'weeks' in ph:
                    print('  weeks count:', len(ph['weeks']))
                    if ph['weeks']:
                        print('   week[0] keys:', list(ph['weeks'][0].keys()))
                        if 'tasks' in ph['weeks'][0]:
                            print('   sample task titles:', [t.get('title') or t.get('name') for t in ph['weeks'][0].get('tasks',[])[:3]])
except Exception as e:
    print('Error reading roadmaps:', e)

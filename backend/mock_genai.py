import os
import sys

site_packages = [p for p in sys.path if 'site-packages' in p][0]
google_dir = os.path.join(site_packages, 'google')
genai_dir = os.path.join(google_dir, 'generativeai')

os.makedirs(genai_dir, exist_ok=True)

with open(os.path.join(google_dir, '__init__.py'), 'w') as f:
    pass

with open(os.path.join(genai_dir, '__init__.py'), 'w') as f:
    f.write('''class DummyModel:
    def generate_content(self, *args, **kwargs):
        class Resp:
            text = "{}"
        return Resp()

class GenerativeModel(DummyModel):
    def __init__(self, *args, **kwargs):
        pass

def configure(*args, **kwargs):
    pass
''')
print("Mock google.generativeai created")

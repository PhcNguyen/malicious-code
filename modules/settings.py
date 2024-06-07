from pathlib import Path
import os.path


BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True


YML_DIRS = os.path.join(BASE_DIR, 'modules', 'ext.yml')
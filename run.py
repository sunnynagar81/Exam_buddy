import subprocess
import sys
import time
import webbrowser
from pathlib import Path

BASE = Path(__file__).parent
LANDING = (BASE / "landing.html").as_uri()
APP = str(BASE / "app.py")

# Start the Streamlit app
app_process = subprocess.Popen([sys.executable, "-m", "streamlit", "run", APP])

# Give the app a few seconds to start, then open the landing page
time.sleep(4)
webbrowser.open(LANDING)

try:
    app_process.wait()
except KeyboardInterrupt:
    app_process.terminate()
    print("Exam Buddy stopped.")
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
REPORT_DIR = ROOT_DIR / "reports"
ASSET_DIR = ROOT_DIR / "assets"
LOG_DIR = ROOT_DIR / "logs"
TEMP_DIR = ROOT_DIR / "temp"

for folder in [
    DATA_DIR,
    REPORT_DIR,
    ASSET_DIR,
    LOG_DIR,
    TEMP_DIR
]:
    folder.mkdir(exist_ok=True)

OLLAMA_MODEL = "qwen2.5:3b"
OLLAMA_TIMEOUT = 120


APP_NAME = "InsightForge AI"
PAGE_ICON = "📊"
LAYOUT = "wide"

DEFAULT_THEME = "plotly_white"
MAX_PREVIEW_ROWS = 10
MAX_UNIQUE_VALUES = 20
CORRELATION_THRESHOLD = 0.75

RANDOM_STATE = 42
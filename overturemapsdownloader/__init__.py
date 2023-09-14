import logging
import warnings
from rich.console import Console

console = Console()

warnings.simplefilter(action="ignore", category=FutureWarning)
# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

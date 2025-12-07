import logging
import sys
from app.core.config import get_settings

def setup_logging():
    settings = get_settings()
    
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set lower level for some noisy libraries if needed
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)

logger = logging.getLogger("ai_travel_planner")

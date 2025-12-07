import functools
import time
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

class CircuitBreakerOpenException(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF-OPEN

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = "HALF-OPEN"
                    logger.info(f"Circuit breaker for {func.__name__} is HALF-OPEN")
                else:
                    logger.warning(f"Circuit breaker for {func.__name__} is OPEN. Call rejected.")
                    raise CircuitBreakerOpenException(f"Circuit breaker is OPEN for {func.__name__}")

            try:
                result = await func(*args, **kwargs)
                if self.state == "HALF-OPEN":
                    self.state = "CLOSED"
                    self.failures = 0
                    logger.info(f"Circuit breaker for {func.__name__} is CLOSED")
                return result
            except Exception as e:
                self.failures += 1
                self.last_failure_time = time.time()
                logger.error(f"Call to {func.__name__} failed. Failure count: {self.failures}")
                
                if self.failures >= self.failure_threshold:
                    self.state = "OPEN"
                    logger.error(f"Circuit breaker for {func.__name__} is now OPEN")
                
                raise e

        return wrapper

# Singleton instances or factory can be used
# For simplicity, we can instantiate per service method or globally

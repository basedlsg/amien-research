"""
Retry utilities with exponential backoff
Handles transient failures for AI API calls and other operations
"""

import asyncio
import functools
from typing import Any, Callable, Optional, Tuple, Type

from config.logging_config import get_logger
from config.constants import (
    MAX_RETRIES,
    RETRY_BASE_DELAY_SECONDS,
    RETRY_MAX_DELAY_SECONDS,
)

logger = get_logger(__name__)


async def retry_with_exponential_backoff(
    func: Callable,
    *args,
    max_retries: int = MAX_RETRIES,
    base_delay: float = RETRY_BASE_DELAY_SECONDS,
    max_delay: float = RETRY_MAX_DELAY_SECONDS,
    retryable_exceptions: Optional[Tuple[Type[Exception], ...]] = None,
    **kwargs
) -> Any:
    """
    Retry an async function with exponential backoff

    Args:
        func: Async function to retry
        *args: Positional arguments for func
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        retryable_exceptions: Tuple of exception types to retry. If None, retries all exceptions
        **kwargs: Keyword arguments for func

    Returns:
        Result from successful function call

    Raises:
        Last exception if all retries fail
    """
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            result = await func(*args, **kwargs)
            if attempt > 0:
                logger.info(f"Retry successful on attempt {attempt + 1}")
            return result

        except Exception as e:
            last_exception = e

            # Check if this exception type should be retried
            if retryable_exceptions and not isinstance(e, retryable_exceptions):
                logger.warning(f"Non-retryable exception: {type(e).__name__}: {e}")
                raise

            # Don't sleep on last attempt
            if attempt < max_retries:
                # Calculate exponential backoff delay
                delay = min(base_delay * (2 ** attempt), max_delay)

                logger.warning(
                    f"Attempt {attempt + 1}/{max_retries + 1} failed: {type(e).__name__}: {e}. "
                    f"Retrying in {delay:.1f}s..."
                )

                await asyncio.sleep(delay)
            else:
                logger.error(
                    f"All {max_retries + 1} attempts failed. Last error: {type(e).__name__}: {e}"
                )

    # Raise the last exception after all retries exhausted
    raise last_exception


def with_retry(
    max_retries: int = MAX_RETRIES,
    base_delay: float = RETRY_BASE_DELAY_SECONDS,
    max_delay: float = RETRY_MAX_DELAY_SECONDS,
    retryable_exceptions: Optional[Tuple[Type[Exception], ...]] = None,
):
    """
    Decorator to add retry logic with exponential backoff to async functions

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        retryable_exceptions: Tuple of exception types to retry. If None, retries all exceptions

    Returns:
        Decorated function with retry logic

    Example:
        @with_retry(max_retries=3, retryable_exceptions=(TimeoutError, ConnectionError))
        async def call_ai_api():
            # API call that might fail transiently
            pass
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await retry_with_exponential_backoff(
                func,
                *args,
                max_retries=max_retries,
                base_delay=base_delay,
                max_delay=max_delay,
                retryable_exceptions=retryable_exceptions,
                **kwargs
            )
        return wrapper
    return decorator

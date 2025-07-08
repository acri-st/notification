from msfwk.utils.logging import get_logger

logger = get_logger("application")


async def run_with_error_logging(func, *args, **kwargs):
    try:
        return await func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Background task error in {func.__name__}: {e!s}", exc_info=True)
        raise

import logging

from msfwk.application import app
from msfwk.context import current_config, register_init
from msfwk.mqclient import load_default_rabbitmq_config
from msfwk.utils.logging import get_logger
from msfwk.utils.logging import stream_handler as acri_log_handler

from notification.email import MailNotificationModule

logger = get_logger("application")

app_handling = app


async def init(config: dict) -> bool:
    """Init"""
    logger.info("Initialising notification ...")
    load_succeded = load_default_rabbitmq_config()
    current_config.set(config)
    if load_succeded:
        logger.info("added all automoderation modules")
        notification = MailNotificationModule()
        await notification.start()
    else:
        logger.error("Failed to load rabbitmq config")
    return load_succeded


logging.getLogger("sqlalchemy.engine.Engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.engine.Engine").propagate = False
logging.getLogger("sqlalchemy.engine.Engine").handlers = [acri_log_handler]

register_init(init)

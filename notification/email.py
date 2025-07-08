import asyncio
import hashlib
import re
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

import aio_pika
import aiosmtplib
from mako.lookup import TemplateLookup
from mako.template import Template
from msfwk.context import current_transaction
from msfwk.desp.rabbitmq.mq_message import (
    MQContentType,
    decode_consume_message,
)
from msfwk.mqclient import RabbitMQConfig, consume_mq_queue_async
from msfwk.notification import EmailMQMessage
from msfwk.utils.logging import get_logger

logger = get_logger("application")

class MailNotificationModule:
    """One module of moderation"""

    content_type: MQContentType
    consume_queue: str
    task: asyncio.Task | None = None

    def __init__(self) -> "MailNotificationModule":
            self.consume_queue = RabbitMQConfig.MAIL_NOTIFICATION_QUEUE


    async def on_message(self, message: aio_pika.IncomingMessage) -> None:
        """Calls self.analyse on message received from the listened queue

        Args:
            mq_message (DespMQMessage): _description_
            message (aio_pika.IncomingMessage): _description_
        """
        mq_message = await decode_consume_message(message, EmailMQMessage)
        logger.debug("current_transaction : %s", current_transaction.get())
        if mq_message is None:
            logger.warning("Cannot send email due to decoding error")
            return
        logger.info("Notification start sending %s email", mq_message.id)
        await self.send_email_async(mq_message)
        logger.info(
            "Notification finished analysing %s email", mq_message.id
        )
        await message.ack()

    async def start(self) -> None:
        """Start the module

        Listen to "consume_queue" and analyse the incomming message.
        Then redirect them in the next automod Queue, or handling
        """
        self.task = await consume_mq_queue_async(self.consume_queue, lambda msg: self.on_message(msg))
        logger.info(
            "Notification Module Start listening on %s", self.consume_queue
        )

    async def send_email_async(self, mail: EmailMQMessage) -> None:
        """Send email to SMTP

        Args:
            mail (EmailMQMessage): mail object
        """
        logger.warning(mail)
        try:
            # Create message
            msg = MIMEMultipart()
            msg["From"] = mail.sender_email
            msg["To"] = mail.user_email
            msg["Subject"] = f"[{mail.project}] {mail.subject}"

            message = self._clean_html_tags(mail.message)

            template_vars = {
                "message": message,
            }
            output = self._render_template(
                template_vars,
                mail.project,
                f"{mail.template_path}",
            )

            msg.attach(MIMEText(output, "plain"))

            # Create an SMTP connection with SSL context that ignores verification
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            # Connect and send email
            server = aiosmtplib.SMTP(
                hostname=mail.smtp_server,
                port=mail.smtp_port,
                use_tls=False,
                tls_context=ssl_context
            )
            await server.connect()
            await server.sendmail(mail.sender_email, mail.user_email, msg.as_string())
            await server.quit()
            logger.info("Email sent successfully!")
        except Exception as e:
            msg = "Error when sending email to SMTP"
            logger.exception(msg, exc_info=e)


    def _render_template(self, context: dict[str, Any], file_folder: str, file_name: str) -> str:
        """Render a mako template

        Args:
            context: Template context
            file_folder: Folder containing the template
            file_name: Template file name

        Returns:
            str: Rendered template
        """
        try:
            lookup = TemplateLookup(
                directories=[f"./{file_folder}"], default_filters=["h"], input_encoding="utf-8", output_encoding="utf-8"
            )
            content = Template(filename=f"./{file_folder}/{file_name}", lookup=lookup).render(**context)  # noqa: S702 (fixed with the template lookup)
            sha256_hash = hashlib.sha256()
            sha256_hash.update(content.encode("utf-8"))
            hash_hex = sha256_hash.hexdigest()
            logger.info("Generated content:\n%s\nSHA256: %s", content, hash_hex)
            return content
        except Exception as e:
            msg = f"Failed to render template {file_name}"
            logger.exception(msg, exc_info=e)

    @classmethod
    def _clean_html_tags(cls, text:str):
        """Remove HTML tags from a given string."""
        return re.sub(r"<.*?>", "", text)

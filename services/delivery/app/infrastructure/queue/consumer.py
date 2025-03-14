from aio_pika import connect_robust
from app.application.services import delivery_service
import json
import logging
from app.application.services.smtp_service import SMTPService
from app.application.services.telegram_service import TelegramService
from app.application.dto.telegram import TelegramDTO

logger = logging.getLogger(__name__)


async def process_mailing(message):
    try:
        data = json.loads(message.body.decode())
        logger.info(f"Processing mailing ID: {data['mailing_id']}")

        smtp_service = SMTPService()
        telegram_service = TelegramService()
        delivery_service_instance = delivery_service.DeliveryService(
            smtp_service=smtp_service, telegram_service=telegram_service
        )

        await delivery_service_instance.send_mailing(data)
        logger.info(f"Successfully processed mailing ID: {data['mailing_id']}")
        await message.ack()

    except Exception as e:
        logger.error(f"Failed to process mailing: {str(e)}")
        await message.reject(requeue=True)


async def start_consumer():
    logger.info("Starting consumer connection...")
    try:
        connection = await connect_robust("amqp://guest:guest@rabbitmq:5672/")
        logger.info("RabbitMQ connection established")
        channel = await connection.channel()
        logger.info("Channel created")

        queue = await channel.declare_queue(
            "mailings.created", auto_delete=False, durable=True
        )
        logger.info("Queue declared, starting message processing...")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    logger.info(f"Processing message: {message.body.decode()}")
                    await process_mailing(message)
    except Exception as e:
        logger.error(f"Consumer error: {e}")

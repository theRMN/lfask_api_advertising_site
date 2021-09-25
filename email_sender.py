import asyncio
from aiosmtplib import send
import more_itertools

from app import Creator


class EmailSender:

    async def extract_and_send(
            self,
            hostname,
            port,
            sender,
            username,
            password
    ):

        cor_list = []
        cur = Creator.query.all()

        for row in cur:
            recipients = row.email
            message = f'Уважаемый {row.name}! Спасибо, что пользуетесь нашим сервисом объявлений.'.encode('utf-8')
            cor_list.append(
                send(
                    message,
                    recipients=recipients,
                    sender=sender,
                    hostname=hostname,
                    port=port,
                    username=username,
                    password=password,
                    start_tls=True
                )
            )

        for chunk in more_itertools.chunked(cor_list, 10):
            await asyncio.gather(*chunk)

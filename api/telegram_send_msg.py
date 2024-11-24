# module telegram_send_msg

import asyncio
import telegram 


if __name__ == '__main__':
    bot = telegram.Bot(token='token')
    asyncio.run(
        bot.send_message(chat_id='123456789', text='hello, world!')
    )



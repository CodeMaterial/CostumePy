import logging
from system.costume_modules import CostumeModule
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup
import configparser

config = configparser.ConfigParser()
config.read('config/system_config.ini')

bot = telepot.Bot(config["TELEGRAM"]["bot_id"])  # This is placed here as you can't pickle a thread locking object


class Telegram(CostumeModule):

    def __init__(self):
        super().__init__(refresh_rate=1/30)

        self.listeners["ALL_MODULES"] = self.notify_event
        self.listeners["NOTIFY"] = self.notify_event
        self.listeners["REFRESH_RATE"] = self.notify_refresh
        self.listeners["ALL_MODULES"] = self.notify_event
        logging.info(self.listeners)
        self.admin_id = config["TELEGRAM"]["admin_id"]

    def notify_refresh(self, event):
        self.send_message("Refresh rate for %s: %.2f fps" % (event.source, 1/event.data))

    def notify_event(self, event):
        self.send_message("Notification: %r" % event)

    def send_message(self, text, reply_markup=None):
        bot.sendMessage(self.admin_id, text, reply_markup)

    def setup(self):
        MessageLoop(bot, self.handle).run_as_thread()  # This thread gets run in the main process.
        self.send_message("Telegram setup")
        self.broadcast("LIST_MODULES")

    def handle(self, msg):

        user_id = msg["from"]["id"]
        username = msg["from"]["username"]
        chat_id = msg["chat"]["id"]
        text = msg["text"]

        logging.info("Message received from %s (%i) in chat %i: %s" % (username, user_id, chat_id, text))

        if text.upper() == "/REFRESH":
            self.send_message("requesting refresh rate")
            self.broadcast("MEASURE_REFRESH")


        if text.upper() == "/BLUSH":
            self.broadcast("BLUSH", data=True)
            self.broadcast("BLUSH", data=False, delay=5)
            self.send_message("Blush event added")


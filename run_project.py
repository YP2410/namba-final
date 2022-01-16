import threading

import backend.telegram_bot
import backend.app

class FlaskThread(threading.Thread):
    def run(self) -> None:
        backend.app.app.run()

if __name__ == '__main__':
    flask_thread = FlaskThread()
    flask_thread.start()
    backend.telegram_bot.main()
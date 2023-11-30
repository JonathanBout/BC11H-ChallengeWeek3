from datetime import datetime, timedelta


class ScoreManager:
    def __init__(self) -> None:
        self.__start_time = datetime.now()
        self.__elapsed = timedelta()
        self.is_paused = True

    def start(self):
        self.is_paused = False
        self.__start_time = datetime.now()
        self.__elapsed = timedelta()

    def pause(self):
        if not self.is_paused:
            self.__elapsed += datetime.now() - self.__start_time
            self.is_paused = True

    def resume(self):
        if self.is_paused:
            self.is_paused = False
            self.__start_time = datetime.now()

    def get_elapsed(self):
        total_elapsed = self.__elapsed

        if not self.is_paused:
            total_elapsed += datetime.now() - self.__start_time

        return total_elapsed

    def get_score(self):
        return int(
            self.get_elapsed().total_seconds()  # TODO: make some better formula?
        )

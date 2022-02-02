from datetime import datetime


class Log:
    @classmethod
    def print_log(cls, txt):
        cls.current_date = datetime.now()
        return f'{cls.current_date.strftime("%d/%m/%Y %H:%M:%S")} - {txt}'

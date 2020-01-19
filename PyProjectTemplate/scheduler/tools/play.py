# from dateutil import parser

# from tls.settings import *


# def datetime2str(ts, fmt="%Y-%m-%d %H:%M:%S"):
#     return datetime.strftime(ts, fmt)


# def str2datetime(ts, fmt="%Y-%m-%d %H:%M:%S"):
#     return datetime.strptime(ts, fmt)


# def get_cur_time():
#     return datetime.now(TIMEZONE)


# #  ISO 8601 datetime to python datetime
# def iso_string_to_datetime(iso_string):
#     return parser.parse(iso_string).astimezone(TIMEZONE)


# def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))

import random
import time

class LazyProperty:
    def __init__(self, function):
        self.function = function
        self.name = function.__name__

    def __get__(self, obj, type=None) -> object:
        obj.__dict__[self.name] = self.function(obj)
        return obj.__dict__[self.name]

    # def __set__(self, obj, value):
    #     pass

class DeepThought:
    @LazyProperty
    def meaning_of_life(self):
        time.sleep(1)
        return 42

my_deep_thought_instance = DeepThought()
print(my_deep_thought_instance.meaning_of_life)
print(my_deep_thought_instance.meaning_of_life)
print(my_deep_thought_instance.meaning_of_life)

from datetime import date, datetime, timedelta

def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

result = []
for i in perdelta(date(2017, 3, 1), date(2017, 8, 31), timedelta(days=14)):
    result.append(str(i))

print result
def next_count(str):
  index = 0
  number = 0
  while index < len(str) and str[index].isdigit():
    number = number*10 + int(str[index])
    index += 1
  return number, str[index:]

def next_string(str):
  index = 0
  while index < len(str) and not str[index].isdigit():
    index += 1

  return str[0:index], str[index:]

def get_buffer(str):
  buffer = []
  while len(str) > 0:
    num, str = next_count(str)
    for i in range(num):
      buffer.append(None)
    buf, str = next_string(str)
    for i in range(len(buf)):
      buffer.append(buf[i])

  return buffer

def solution(S, T):
  str1_buff = get_buffer(S)
  str2_buff = get_buffer(T)

  #print "First len is %s and buffer is '%s'" % (len(str1_buff), str1_buff)
  #print "Second len is %s and buffer is '%s'" % (len(str2_buff), str2_buff)

  if len(str1_buff) != len(str2_buff):
    return False

  for i in range(len(str1_buff)):
    if str1_buff[i] != None and str2_buff[i] != None and str1_buff[i] != str2_buff[i]:
      return False

  return True
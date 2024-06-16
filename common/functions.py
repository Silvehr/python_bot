def print_list(list: list):
  result = ' '
  for item in list:
    result += item + ' '
  return result


def print_dict(dict: dict):
  result = ''
  for key, value in dict.items():
    result += str(key) + ': ' + str(value) + ' '
  return result
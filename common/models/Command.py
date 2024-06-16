class Command:
    STANDARD_COMMAND_SEPARATOR = " "
    
    _source : str
    _splitted : str
    _separator : str = " "
    
    def __init__(self, source : str, separator : str):
        self._source = source
        if len(separator) > 0:
            self._separator = separator
        self._splitted = source.split(self._separator)
    
    def prefix(self):
        return self._splitted[0]
    
    def command(self):
        return self._splitted[1]
    
    def get_argument(self, arg_i):
        if len(self._splitted) - 2 >= 0:
            return self._splitted[2 + arg_i]
        else:
            return ""
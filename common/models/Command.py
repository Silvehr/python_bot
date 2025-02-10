class Command:
    STANDARD_COMMAND_SEPARATOR = " "
    
    _source : str
    _splitted : str
    _separator : str = " "
    
    def __init__(self, source : str, separator : str):
        self._source = source
        if len(separator) > 0:
            self._separator = separator
        self._splitted=[]
        c_arg = ""
        i = 0

        while i < len(source):
            c = source[i]
            if c==' ' and len(c_arg) > 0:
                self._splitted.append(c_arg)
            elif c == '"':
                end = source.find('"',i+1)
                self._splitted.append(source[(i+1):(end)])
                if end == -1:
                    raise SyntaxError()
                i = end
            else:
                c_arg+= c
            i+=1

        if len(c_arg) > 0:
            self._splitted.append(c_arg)
                
    
    def prefix(self):
        return self._splitted[0]
    
    def command(self):
        return self._splitted[1]
    
    def get_argument(self, arg_i):
        if len(self._splitted) - 2 >= 0:
            return self._splitted[2 + arg_i]
        else:
            return ""
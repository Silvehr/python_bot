class Command:
    STANDARD_COMMAND_SEPARATOR = " "
    
    def __init__(self, source : str, separator : str= " "):
        self._source : str = source

        if len(separator) > 0:
            self._separator : str = separator

        self._split : list[str] = []

        c_arg = ""
        i = 0

        while i < len(source):
            c = source[i]
            if c==' ' or c == '\n' or c == '\t':
                if len(c_arg) > 0:
                    self._split.append(c_arg)
                    c_arg=""
            elif c == '"':
                end = source.find('"',i+1)
                self._split.append(source[(i + 1):end])
                if end == -1:
                    raise SyntaxError()
                i = end
            else:
                c_arg+= c
            i+=1

        if len(c_arg) > 0:
            self._split.append(c_arg)

        self._currentIndex = 2
                
    
    def prefix(self):
        return self._split[0]
    
    def command(self) -> str | None:
        if len(self._split) == 0:
            return None
        else:
            return self._split[1]

    def OtherToList(self):
        return self._split[self._currentIndex:]

    def __getitem__(self, item: int):
        if len(self._split) - 2 >= 0:
            return self._split[2 + item]
        else:
            return ""

    def get_argument(self, arg_i):
        if len(self._split) - 2 >= 0:
            return self._split[2 + arg_i]
        else:
            return ""

    @property
    def Current(self) -> str:
        return self._split[self._currentIndex]

    def MoveNext(self) -> bool:
        if len(self._split) > self._currentIndex:
            self._currentIndex+=1
            return True
        else:
            return False

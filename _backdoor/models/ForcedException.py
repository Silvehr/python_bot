class ForcedException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.add_note("This is exception thrown as a test of logger")
class NetworkException(Exception):
    code: int
    
    def __init__(self, code: int) -> None:
        super().__init__(f"code={code}")

        self.code = code

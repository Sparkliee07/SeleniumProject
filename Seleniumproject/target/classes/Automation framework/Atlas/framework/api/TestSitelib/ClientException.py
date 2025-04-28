import json

class ClientException(Exception):
    def __init__(self, errorCode, message, innerException=None):
        super().__init__(message)
        self.message = None
        self.errorCode = errorCode
        self.innerException = innerException

    def __str__(self):
        return f"ClientException: {self.errorCode}, {self.message}, InnerException: {self.innerException}"

    def to_dict(self):
        return {
            'errorCode': self.errorCode,
            'message': str(self),
            'innerException': str(self.innerException) if self.innerException else None
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data):
        errorCode = data.get('errorCode')
        message = data.get('message')
        innerException = data.get('innerException')
        return cls(errorCode, message, innerException)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls.from_dict(data)

if __name__ == "__main__":
    # Usage example
    try:
        raise ClientException(0, "Unknown process control exception")
    except ClientException as e:
        print(e)
        serialized = e.to_json()
        print(f"Serialized: {serialized}")
        deserialized = ClientException.from_json(serialized)
        print(f"Deserialized: {deserialized}")

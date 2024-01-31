import abc

class File_Type(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def load(*args, **kwargs):
        pass

    @staticmethod
    @abc.abstractmethod
    def save(*args, **kwargs):
        pass

    @staticmethod
    @abc.abstractmethod
    def is_type(cls, *args, **kwargs):
        pass
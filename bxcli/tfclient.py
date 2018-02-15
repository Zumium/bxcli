from abc import ABCMeta, abstractmethod

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TMultiplexedProtocol, TBinaryProtocol

from . import config
from .tf.boxes import BoxService, FileService, LinkService


class ClientSession(metaclass=ABCMeta):

    @abstractmethod
    def service_name(self):
        pass

    @abstractmethod
    def __enter__(self):
        transport = TSocket.TSocket('localhost', config.port())
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        protocol = TMultiplexedProtocol.TMultiplexedProtocol(protocol, self.service_name())

        transport.open()
        self.transport = transport
        self.protocol = protocol

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.transport.close()
        return False


class BoxServiceSession(ClientSession):

    def service_name(self):
        return "BoxService"

    def __enter__(self):
        super(BoxServiceSession, self).__enter__()
        return BoxService.Client(self.protocol)


class FileServiceSession(ClientSession):

    def service_name(self):
        return "FileService"

    def __enter__(self):
        super(FileServiceSession, self).__enter__()
        return FileService.Client(self.protocol)


class LinkServiceSession(ClientSession):

    def service_name(self):
        return "LinkService"

    def __enter__(self):
        super(LinkServiceSession, self).__enter__()
        return LinkService.Client(self.protocol)

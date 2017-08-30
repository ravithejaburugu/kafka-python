from __future__ import absolute_import
import abc


class ABCRecord(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def offset(self):
        """ Absolute offset of record
        """

    @abc.abstractproperty
    def timestamp(self):
        """ Epoch milliseconds
        """

    @abc.abstractproperty
    def timestamp_type(self):
        """ CREATE_TIME(0) or APPEND_TIME(1)
        """

    @abc.abstractproperty
    def key(self):
        """ Bytes key or None
        """

    @abc.abstractproperty
    def value(self):
        """ Bytes value or None
        """

    @abc.abstractproperty
    def checksum(self):
        """ Prior to v2 format CRC was contained in every message. This will
            be the checksum for v0 and v1 and None for v2 and above.
        """

    @abc.abstractproperty
    def headers(self):
        """ If supported by version list of key-value tuples, or empty list if
            not supported by format.
        """


class ABCRecordBatchBuilder(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def append(self, offset, timestamp, key, value, headers):
        """ Writes record to internal buffer.

        Arguments:
            offset (int): Relative offset of record, starting from 0
            timestamp (int): Timestamp in milliseconds since beginning of the
                epoch (midnight Jan 1, 1970 (UTC))
            key (bytes or None): Key of the record
            value (bytes or None): Value of the record
            headers (List[Tuple[str, bytes]]): Headers of the record. Header
                keys can not be ``None``.

        Returns:
            bool: If message was successfully written. False means that there's
                no more space for the record.
        """

    @abc.abstractmethod
    def build(self):
        """ Close for append, compress if needed, write size and header and
            return a ready to send bytes object.

            Return:
                bytes: finished batch, ready to send.
        """


class ABCRecordBatch(object):
    """ For v2 incapsulates a RecordBatch, for v0/v1 a single (maybe
        compressed) message.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __iter__(self):
        """ Return iterator over records (ABCRecord instances). Will decompress
            if needed.
        """


class ABCRecords(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, buffer):
        """ Initialize with bytes-like object conforming to the buffer
            interface, used by struct.unpack. Ie. `buffer` on Python2 or
            `memoryview` on Python3 can be used, as well as `str` and `bytes`.
        """

    @abc.abstractmethod
    def size_in_bytes(self):
        """ Returns the size of buffer.
        """

    @abc.abstractmethod
    def next_batch(self):
        """ Return next batch of records (ABCRecordBatch instances).
        """

    @abc.abstractmethod
    def has_next(self):
        """ True if there are more batches to read, False otherwise.
        """

import time
import os

import construct

from tlsenum import hello_constructs


class ClientHello(object):

    @property
    def protocol_version(self):
        return self._protocol_version

    @protocol_version.setter
    def protocol_version(self, protocol_version):
        assert protocol_version in ["3.0", "1.0", "1.1", "1.2"]

        self._protocol_version = protocol_version

        if protocol_version == "3.0":
            self._protocol_minor = 0
        elif protocol_version == "1.0":
            self._protocol_minor = 1
        elif protocol_version == "1.1":
            self._protocol_minor = 2
        elif protocol_version == "1.2":
            self._protocol_minor = 3

    @property
    def deflate(self):
        return self._deflate

    @deflate.setter
    def deflate(self, deflate):
        self._deflate = deflate
        if deflate:
            self._compression_method = [1, 0]
        else:
            self._compression_method = [0]

    def build(self):
        protocol_version = construct.Container(
            major=3, minor=self._protocol_minor
        )

        random = construct.Container(
            gmt_unix_time=int(time.time()), random_bytes=os.urandom(28)
        )

        session_id = construct.Container(
            length=0, session_id=b""
        )

        compression_method = construct.Container(
            length=len(self._compression_method),
            compression_methods=self._compression_method
        )

        return hello_constructs.ClientHello.build(
            construct.Container(
                version=protocol_version, random=random, session_id=session_id,
                compression_methods=compression_method
            )
        )

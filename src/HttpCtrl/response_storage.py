"""

HttpCtrl library provides HTTP/HTTPS client and server API to Robot Framework to make REST API testing easy.

Authors: Andrei Novikov
Date: 2018-2019
Copyright: GNU Public License

HttpCtrl is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

HttpCtrl is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import threading

from robot.api import logger

from HttpCtrl.utils.singleton import Singleton


class ResponseStorage(metaclass=Singleton):
    def __init__(self):
        self.__response = None
        self.__event_incoming = threading.Condition()


    def __ready(self):
        return self.__response is not None


    def push(self, response):
        with self.__event_incoming:
            logger.info("Push response to the Response Storage: %s" % response)
            self.__response = response
            self.__event_incoming.notify()


    def pop(self, timeout=5.0):
        with self.__event_incoming:
            if not self.__ready():
                result = self.__event_incoming.wait_for(self.__ready, timeout)
                if result is False:
                    return None

            response = self.__response
            self.__response = None
            return response


    def clear(self):
        with self.__event_incoming:
            self.__response = None

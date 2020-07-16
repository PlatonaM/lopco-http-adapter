"""
   Copyright 2020 InfAI (CC SES)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

__all__ = ("Storage", "Notification")


from .logger import getLogger
from .configuration import conf
import uuid
import os
import hashlib
import requests
import threading
import queue
import time


logger = getLogger(__name__.split(".", 1)[-1])


class Storage:

    def save(self, stream):
        name = uuid.uuid4().hex
        file_path = os.path.join(conf.DS.path, name)
        file_hash = hashlib.sha512()
        with open(file_path, 'wb') as file:
            while True:
                chunk = stream.read(conf.DS.chunk_size)
                if not chunk:
                    break
                file.write(chunk)
                file_hash.update(chunk)
        logger.debug("saved {} bytes to file '{}'".format(os.path.getsize(file_path), name))
        return name, file_hash.hexdigest()


class Notification(threading.Thread):

    def __init__(self):
        super().__init__(name="notifier", daemon=True)
        self.__queue = queue.Queue()

    def add(self, f_hash, m_id, f_name):
        self.__queue.put_nowait(
            {
                "hash": f_hash,
                "machine_id": m_id,
                "file_name": f_name
            }
        )

    def run(self):
        while True:
            data = self.__queue.get()
            while True:
                try:
                    resp = requests.post("{}/{}".format(conf.JM.url, conf.JM.api), json=data)
                    if resp.status_code == 200:
                        logger.debug("sent notification for '{}'".format(data["hash"]))
                        break
                    if resp.status_code == 409:
                        logger.warning("already sent notification for '{}'".format(data["hash"]))
                        break
                    logger.warning("can't send notification for '{}' - {}".format(data["hash"], resp.status_code))
                except Exception as ex:
                    logger.warning("can't send notification for '{}' - {}".format(data["hash"], ex))
                time.sleep(5)


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

__all__ = ("Upload", )


from .logger import getLogger
from . import handlers
import falcon



logger = getLogger(__name__.split(".", 1)[-1])


def reqDebugLog(req):
    logger.debug("method='{}' path='{}' content_type='{}'".format(req.method, req.path, req.content_type))


def reqErrorLog(req, ex):
    logger.error("method='{}' path='{}' - {}".format(req.method, req.path, ex))


class Upload:
    def __init__(self, stg_handler: handlers.Storage, notif_handler: handlers.Notification):
        self.__stg_handler = stg_handler
        self.__notif_handler = notif_handler

    def on_post(self, req: falcon.request.Request, resp: falcon.response.Response, m_id):
        reqDebugLog(req)
        try:
            f_name, hash = self.__stg_handler.save(req.stream)
            resp.body = hash
            resp.content_type = falcon.MEDIA_TEXT
            resp.status = falcon.HTTP_200
            self.__notif_handler.add(hash, m_id, f_name)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)

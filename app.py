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

from adapter.logger import initLogger
from adapter.configuration import conf
from adapter import handlers
from adapter import api
import falcon


initLogger(conf.Logger.level)


stg_handler = handlers.Storage()

notif_handler = handlers.Notification()

app = falcon.API()

app.req_options.strip_url_path_trailing_slash = True

routes = (
    ("/{ds_id}", api.Upload(stg_handler, notif_handler)),
)

for route in routes:
    app.add_route(*route)

notif_handler.start()

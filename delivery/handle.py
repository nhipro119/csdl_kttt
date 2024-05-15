from . import api
class Handle:
    def __init__(self):
        self.api = api.Api()

    def setup(self,router):
        router.add_url_rule("/search", "search", self.api.search, methods=["POST"])
        router.add_url_rule("/ping", "ping", self.api.ping, methods=["GET"])
        return router
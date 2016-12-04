import falcon


class Prova:
    def on_get(self,req,res):
        res.body="Prova!"

api = falcon.API()

api.add_route("/prova",Prova())

import yaml



class Reader:
    server_config_dir = "./Config/server_config.yaml"
    service_config_dir = "./Config/service_config.yaml"
    
    def __init__(self) ->None:
        pass
    def get_server_config(self):
        with open(self.server_config_dir, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

            f.close()
        return data
    def get_service_config(self):
        with open(self.service_config_dir, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

            f.close()
        return data
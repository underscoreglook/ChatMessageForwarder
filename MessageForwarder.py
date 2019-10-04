import importlib
import yaml

from Router import Router
from DiscordClient import DiscordClient

if __name__ == "__main__":
    router = Router()
    with open('config.yaml') as configFile:
        data = yaml.load(configFile, Loader=yaml.FullLoader)
        for key in data:
            if not data[key]["enabled"]:
                continue;
            className = key.capitalize() + "Client"
            module = importlib.import_module(className)
            actualClass = getattr(module, className)
            router.addClient(actualClass(router))
    router.start()

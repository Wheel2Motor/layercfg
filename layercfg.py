import os
import json
import shutil
import threading


class LayerConfig:


    TEXT_CONFIG_FILE_NAME = "config.json"


    def __init__(self, root):
        self.__root = root


    @property
    def root(self):
        return self.__root


    def init_path(
            self,
            path:str,
            config_content:dict={},
            need_config=True,
            reset:bool=False
            ) -> None:
        with threading.Lock():
            target = os.path.join(self.root, path)
            target_config = os.path.join(target, self.TEXT_CONFIG_FILE_NAME)
            if reset and os.path.exists(target):
                shutil.rmtree(target)
            if not os.path.exists(target):
                os.makedirs(target)
            if need_config and (not os.path.exists(target_config)):
                with open(target_config, "w", encoding="utf-8") as f:
                    f.write(json.dumps(config_content))


    def get_config_dir(
            self,
            path:str,
            ensure_exists:bool=True
            ) -> str:
        target = os.path.join(self.root, path) if path else self.root
        if ensure_exists and not os.path.exists(target):
            raise Exception("Config dir not found: {0}".format(target))
        return target


    def get_config_file(
            self,
            path:str,
            ensure_exists:bool=True
            ) -> str:
        target = os.path.join(self.root, path) if path else self.root
        target_file = os.path.join(target, self.TEXT_CONFIG_FILE_NAME)
        if ensure_exists and not os.path.exists(target_file):
            raise Exception("Config file not found: {0}".format(target))
        return target_file


    def get_config(
            self,
            path:str,
            key:str,
            **kwargs
            ) -> str:
        target_file = self.get_config_file(path, True)
        with threading.Lock():
            with open(path, encoding="utf-8") as f:
                data = json.loads(f.read())
                return data.get(key, **kwargs)


    def set_config(
            self,
            path:str,
            key:str,
            value:str
            ) -> None:
        target_file = self.get_config_file(path, True)
        with threading.Lock():
            data = None
            with open(target_file, "r", encoding="utf-8") as f:
                data = json.loads(f.read())
            data[key] = value
            out = json.dumps(data)
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(out)


    def list_sublayer(self) -> list:
        return list(filter(lambda item: os.path.isdir(self.get_config_dir(item)),
                           os.listdir(self.root)))


if __name__ == "__main__":
    cfg_root = LayerConfig("LWConfig")
    cfg_root.init_path("global")
    cfg_root.init_path("project")
    cfg_proj = LayerConfig(cfg_root.get_config_dir("project"))
    cfg_proj.init_path("A")
    cfg_proj.init_path("B")
    cfg_proj.init_path("C")
    cfg_proj.set_config(None, "name", 123)

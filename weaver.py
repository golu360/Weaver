import yaml
from fabric import Connection


class Weaver:
    def __init__(self, config, context):
        with open("{}".format(config), 'r') as stream:
            try:
                self.config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        self.is_ssh = "ssh_config" in self.config
        self.context = context

    def validate_ssh_config(self):
        if self.config["ssh_config"] is None:
            print("[ERROR] No Connection Parameter Specified in SSH Config")
            return  False
        validation_keys = ["user", "host", "forward_agent", "timeout", "key_file"]
        config_keys = self.config["ssh_config"].keys()
        errors = []
        for key in validation_keys:
            if key not in config_keys:
                errors.append(key)
        if len(errors) >= 1 or len(config_keys) == 0:
            print("[ERROR] {} keys not present in config".format(",".join(errors)))
        return len(errors) == 0

    def get_context(self):
        # if ssh config is found, create connection or return default context

        if self.is_ssh:
            valid_config = self.validate_ssh_config()
            if valid_config:
                connection = {
                    "user": self.config["ssh_config"]["user"],
                    "host": self.config["ssh_config"]["host"],
                    "port": 22,
                    "forward_agent": self.config["ssh_config"]["forward_agent"],
                    "connect_timeout": self.config["ssh_config"]["timeout"],
                    "connect_kwargs": {
                        "key_filename": self.config["ssh_config"]["key_file"],
                    },
                }
                context = Connection(**connection)
                return context
            else:
                return None
        else:
            return self.context

    def run(self):
        ctx = self.get_context()
        if ctx is not None:  ## if valid context is passed then run commands, else dont
            print("[INFO] Executing Commands...")
            for command in self.config["run"]:
                if self.is_ssh:
                    ctx.run(command)
                if self.is_ssh:
                    ctx.close()

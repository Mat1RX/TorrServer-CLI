import yaml
class Configuration:
    def __init__(self, configuration_file_name):
        self.configuration_file_name = configuration_file_name
        with open(self.configuration_file_name, "r") as file:
            self.config_dict = yaml.safe_load(file)


    def __str__(self):
        return self.config_dict

    def __getattr__(self, item):
        if item in self.config_dict:
            return self.config_dict[item]
        raise AttributeError(f"Config has no attribute '{item}'")


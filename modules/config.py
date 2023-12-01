import yaml


class Config:
    def __init__(self, path):
        self.config_path = path
        self.config = self.load()

    def updata(self, data):
        with open(self.config_path, 'w') as file:
            yaml.safe_dump(data, file)

    def load(self):
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            return e

    @staticmethod
    def create(path, data = {'example':'test'}):
        with open(path, 'w') as file:
            yaml.safe_dump(data, file)

def test():
    Config.create('test.yaml')

if __name__ == '__main__':
    test()

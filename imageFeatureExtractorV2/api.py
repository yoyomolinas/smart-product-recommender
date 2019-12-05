import json

def config():
    with open("config.json", 'r') as f:
        config_dict = json.read(f)
    return config_dict

if __name__ == '__main__':
    config_dict = config()
    print(config_dict)
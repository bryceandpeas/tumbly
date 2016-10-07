from configparser import ConfigParser


def get_config(cfg_name):
    # Set config parser
    cfg = ConfigParser()
    # Read configuration file
    cfg.read(cfg_name)
    # Get data
    config_app_key = cfg.get('Auth', 'AppKey')
    config_app_secret = cfg.get('Auth', 'AppSecret')

    return (config_app_key, config_app_secret)


def put_config(cfg, key, secret):
    # Set config parser
    Config = ConfigParser()
    # Create config file
    cfgfile = open(cfg, 'w')
    # Add section
    Config.add_section('Auth')
    # Add key and secret
    Config.set('Auth', 'AppKey', key)
    Config.set('Auth', 'AppSecret', secret)
    # Write and close
    Config.write(cfgfile)
    cfgfile.close()


def main():
    return None

if __name__ == '__main__':
    main()

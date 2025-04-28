from configparser import ConfigParser
from argparse import ArgumentParser

from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler


def main(config_file, restart):
    cparser = ConfigParser()
    print('a')
    cparser.read(config_file)
    print('a')
    config = Config(cparser)
    print('if we stop here the server is down :(')
    config.cache_server = get_cache_server(config, restart)
    print('a')
    crawler = Crawler(config, restart)
    print('a')
    crawler.start()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file, args.restart)

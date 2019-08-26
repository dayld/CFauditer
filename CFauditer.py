import argparse
import datetime
import logging
import socket
from json import dumps
from time import sleep

import requests

CHECK_INTERVAL = 10  # check for new logs interval in minutes
log_file = '/opt/CFauditer/cloudflare-audit.log'  # file for downloaded logs

CF_TOKEN = '1111111111111111111111111111111111111'
CF_EMAIL = 'email@example.com'
CF_ORG = '11111111111111111111111111111111'
HOST = 'logstash.example.com'
PORT = 9000

logging.basicConfig(filename='/opt/CFauditer/CFauditer.log',
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%d-%m %H:%M:%S',
                    level=logging.INFO)


def get_since_date():
    # get utc now date
    utc_now = datetime.datetime.utcnow()
    # round seconds and microseconds
    round_now = utc_now.replace(second=0, microsecond=0)
    # calc delta with CHECK_INTERVAL
    since_date = round_now - datetime.timedelta(minutes=CHECK_INTERVAL)
    # format to RFC3339
    since_date = since_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    return since_date


def get_log(since_date):
    headers = {'Content-Type': 'application/json', 'X-Auth-Key': CF_TOKEN, 'X-Auth-Email': CF_EMAIL}
    query = 'export=false&since={}&per_page=1000'.format(since_date)
    url = 'https://api.cloudflare.com/client/v4/organizations/{0}/audit_logs?{1}'.format(CF_ORG, query)

    try:
        r = requests.get(url, headers=headers, timeout=10)
        print r.content
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception('')
    except:
        logging.error('Could not get data from Cloudflare API.')
        return None


def send_sock(msg):
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, int(PORT))
    tcpsock.connect(server_address)
    tcpsock.sendall(msg)
    tcpsock.close()


def write_file(msg):
    with open(log_file, 'a') as f:
        f.write(msg)
        f.close()


def loop(args):
    while True:
        since_date = get_since_date()
        log = get_log(since_date)
        if log and log['success']:
            logging.info('Got {} events from Cloudflare'.format(str(len(log['result']))))
            for line in log['result']:
                msg = dumps(line) + '\n'
                if args.socket:
                    send_sock(msg)
                if args.file:
                    write_file(msg)
        sleep(CHECK_INTERVAL * 60)


def main():
    parser = argparse.ArgumentParser(description='Cloudflare audit logs exporter')
    parser.add_argument('-s', '--socket', help='Send parsed events though socket. Default: true', default=True,
                        action='store_true')
    parser.add_argument('-f', '--file', help='Save parsed events to file. Default: true', default=True,
                        action='store_true')
    args = parser.parse_args()

    try:
        loop(args)
    except KeyboardInterrupt:
        logging.info('Exit due to KeyboardInterrupt')


if __name__ == '__main__':
    main()

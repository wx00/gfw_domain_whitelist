#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from argparse import ArgumentParser

from utils import reformat_from_file, get_online_list, get_file_data


PAC_RULE_FMT = '"{}":1,\n'


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-i',
        '--input',
        dest='input',
        default=os.path.join('template', 'whitelist.pac'),
        help='path to gfwlist',
    )
    parser.add_argument(
        '-o',
        '--output',
        dest='output',
        default='whitelist.pac',
        help='path to output pac',
        metavar='PAC',
    )
    parser.add_argument(
        '-p',
        '--proxy',
        dest='proxy',
        default='"SOCKS5 127.0.0.1:1080; SOCKS 127.0.0.1:1080;"',
        help='the proxy parameter in the pac file, for example,\
        "SOCKS5 127.0.0.1:1080; SOCKS 127.0.0.1:1080;"',
        metavar='SOCKS5',
    )
    parser.add_argument(
        '-l',
        '--local-rules',
        dest='rules',
        help='use local rule file for whitelist rules, use dnsmasq .conf format, '
        'or one domain per line surrounded by "/".',
        metavar='RULE_FILE',
    )
    return parser.parse_args()


def writetemplate(template, proxy, output_file, rulesfile=None):

    domains_content = final_list(rulesfile)
    proxy_content = get_file_data(template)
    proxy_content = proxy_content.replace('__PROXY__', proxy)
    proxy_content = proxy_content.replace('__DOMAINS__', domains_content)

    with open(output_file, 'w') as file_obj:
        file_obj.write(proxy_content)


def final_list(rulesfile):
    if rulesfile is not None:
        list_result = reformat_from_file(rulesfile, PAC_RULE_FMT)
    else:
        list_result = get_online_list(PAC_RULE_FMT)
    content = '{\n' + ''.join(list_result) + '"yourdomainhere.com":1\n}'
    print('All done!')
    return content


def main():
    args = parse_args()
    writetemplate(
        args.input,
        '"' + args.proxy.strip('"') + '"',
        args.output,
        args.rules,
    )


if __name__ == '__main__':
    main()

import re
import certifi
import urllib3


def reformat(f, fmt):
    whitelist = []
    for line in f:
        l = re.findall(r'(?<=^server=/).+?(?=/)', line)
        if l:
            whitelist.append(fmt.format(l[0]))
    return whitelist


def reformat_from_file(filename, fmt):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return reformat(f, fmt)
    except IOError:
        print('Unable to open local rule file, exiting...')
        exit(1)


def get_online_list(fmt):
    print('Getting domain whitelist...')
    dnsmasq_china_list = 'https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/accelerated-domains.china.conf'
    try:
        content = getList(dnsmasq_china_list)
        content = content.decode('utf-8')
        with open('whitelistCache', 'w', encoding='utf-8') as f:
            f.write(content)
    except:
        print('Get list update failed,use cache to update instead.')

    whitelist = reformat_from_file('whitelistCache', fmt)

    return whitelist


def get_file_data(filename):
    content = ''
    with open(filename, 'r') as file_obj:
        content = file_obj.read()
    return content


def getList(listUrl):
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',  # Force certificate check.
        ca_certs=certifi.where(),  # Path to the Certifi bundle.
    )

    data = http.request('GET', listUrl, timeout=10).data
    return data

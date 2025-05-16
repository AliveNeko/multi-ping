import ping3
from concurrent.futures import ThreadPoolExecutor
import time
import requests
import csv


def process_ip(ip):
    # Ping测试
    delays = []
    success = 0
    for i in range(4):
        try:
            # 超时设置为1秒，单位秒
            delay = ping3.ping(ip, timeout=1)
            if delay is not None:
                delays.append(delay * 1000)  # 转换为毫秒
                success += 1
        except Exception as e:
            pass  # 处理其他异常

        # 前三次等待，最后一次不等待
        if i < 3:
            time.sleep(0.5)

    # 计算结果
    avg_delay = sum(delays)/len(delays) if success > 0 else None
    loss_rate = (4 - success) / 4 * 100

    # 代理配置
    proxies = {
        "http": "http://127.0.0.1:7897",  # 替换为你的代理地址
        "https": "http://127.0.0.1:7897"
    }
    session = requests.Session()
    session.proxies = proxies

    # IP信息查询
    ipInfoUrl = f'https://api.ipinfo.io/lite/{ip}'
    params = {
        'token': 'a6c2e5328296f5'  # 替换或检查你的token是否正确
    }

    country = "未知"
    as_name = "未知"
    try:
        response = requests.get(ipInfoUrl, params=params)
        response.raise_for_status()  # 自动处理HTTP错误（如404、500等）
        data = response.json()

        country = data.get('country_code')
        as_name = data.get('as_name')
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
    except ValueError as e:
        print(f"解析JSON失败: {e}")
    except KeyError as e:
        print(f"返回数据缺少预期字段: {e}")

    if avg_delay is not None:
        print(
            f'IP: {ip}, 平均延迟: {avg_delay:.2f}, 丢包率: {loss_rate:.1f}, 地区: {country}')
    else:
        print(
            f'IP: {ip}, 平均延迟: 超时, 丢包率: {loss_rate:.1f}, 地区: {country}')

    # 返回结果
    return {
        'ip': ip,
        'avg_delay': avg_delay,
        'loss_rate': loss_rate,
        'country': country,
        'as_name': as_name,
    }


def main():
    # 读取IP列表
    try:
        with open('ip.txt', 'r') as f:
            ips = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("错误：ip.txt文件未找到")
        return

    # 使用多线程处理
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(process_ip, ips)

    # 排序处理：按延迟倒序（None值放在最后）
    sorted_results = sorted(
        results,
        key=lambda x: x['avg_delay'] if x['avg_delay'] is not None else float(
            'inf'),
        reverse=False
    )

    headers = ["IP", "平均延迟", "丢包率", "地区", "ASN"]
    with open('result.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()  # 自动写标题

        for result in sorted_results:
            writer.writerow({
                "IP": result['ip'],
                "平均延迟": "超时" if result['avg_delay'] is None else f"{result['avg_delay']:.2f} ms",
                "丢包率": f"{result['loss_rate']:.1f}%",
                "地区": result['country'],
                "ASN": result['as_name']
            })


if __name__ == '__main__':
    main()

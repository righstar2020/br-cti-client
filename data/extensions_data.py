import ipaddress
import requests
import threading
import random
def ip_to_location(ip:str):
    """
    判断传入的ip地址是否为公网地址，是则返回对应的实际地理位置，否则返回标注“内网”
    :param ip:IP地址
    :return:实际地理位置或内网标注
    """
    # 验证ip地址是否有效
    try:
        ip_object = ipaddress.ip_address(ip)
    except ValueError:
        print(f"error：{ip} 不是一个有效的IP地址！")
        return f"error：{ip} 不是一个有效的IP地址！"

    # 私有地址
    if ip_object.is_private:
        print(f"{ip} 是私有地址")
        return f"{ip} 是私有地址"

    # 公网地址返回实际地理位置
    try:
        url = f"http://ip-api.com/json/{ip}"  # 构造调用ip-api服务的url，并设置返回数据为json格式（免费的查询服务只能用http）
        response = requests.get(url, timeout=5)  # 发送请求，设置超时时间为5秒
        response_data = response.json()
        # 调用服务成功，返回地理信息
        if response_data["status"] == "success":
            print(f"{ip} 对应地理位置：{response_data['country']}, {response_data['regionName']}, {response_data['city']}")
            return f"{response_data['country']},{response_data['regionName']},{response_data['city']}"

        # 调用服务失败，打印报错信息
        elif response_data["status"] == "fail":
            print(f"{ip} 调用查询服务失败：{response_data['message']}")
            return ""

    except Exception as e:
        print(f"{ip} 查询地理位置时出错！error：{e}")
        return ""


def ips_to_location(ips:dict):
    """
        将ip字典转换为地理位置字典
        param:
            ips: 字典(ip->ip出现数量)
        return:
            ip_location_map: 字典(ip->地理位置)
            location_num_map: 字典(地理位置->位置出现数量)
            errors: 错误信息列表
    """
    ip_location_map = {}
    location_num_map = {}
    errors = [] 
    for index,(ip,ip_num) in enumerate(ips.items()):
        print(f"正在处理ip:{ip}({index}/{len(ips.keys())})")
        try:
            location = ip_to_location(ip)   
        except Exception as e:
            errors.append(f"ip_to_location error:{e}")
            continue
        ip_location_map[ip] = location
        location_num_map[location] = location_num_map.get(location,0)+ip_num
    return ip_location_map,location_num_map,errors
def ips_to_location_mock_random(ips:dict):
    """
        将IP地址随机转换为地理位置
        param:
            ips: 字典(ip->ip出现数量)
        return:
            ip_location_map: 字典(ip->地理位置)
            location_num_map: 字典(地理位置->位置出现数量)
            errors: 错误信息列表
    """
    ip_location_map = {}
    location_num_map = {}
    errors = []
    
    # 模拟的地理位置列表
    locations = [
        "中国,北京,北京",
        "中国,上海,上海", 
        "中国,广东,深圳",
        "美国,加利福尼亚,旧金山",
        "日本,东京,东京",
        "韩国,首尔,首尔",
        "英国,伦敦,伦敦",
        "德国,柏林,柏林",
        "法国,巴黎,巴黎",
        "俄罗斯,莫斯科,莫斯科"
    ]
    
    for ip, ip_num in ips.items():
        # 随机选择一个地理位置
        location = random.choice(locations)
        ip_location_map[ip] = location
        location_num_map[location] = location_num_map.get(location, 0) + ip_num
        
    return ip_location_map, location_num_map, errors
def ips_to_location_concurrent(ips:dict, max_workers=10000):
    """
        使用多线程并发将ip字典转换为地理位置字典
        param:
            ips: 字典(ip->ip出现数量)
            max_workers: 最大线程数,默认10
        return:
            ip_location_map: 字典(ip->地理位置)
            location_num_map: 字典(地理位置->位置出现数量) 
            errors: 错误信息列表
    """
    ip_location_map = {}
    location_num_map = {}
    errors = []
    threads = []
    results = {}
    
    def process_ip(ip, ip_num):
        try:
            location = ip_to_location(ip)
            results[ip] = (location, ip_num, None)
        except Exception as e:
            results[ip] = (None, ip_num, f"ip_to_location error:{e}")
            
    # 创建并启动线程
    for index, (ip, ip_num) in enumerate(ips.items()):
        while len(threads) >= max_workers:
            for t in threads[:]:
                if not t.is_alive():
                    threads.remove(t)
                    
        thread = threading.Thread(target=process_ip, args=(ip, ip_num))
        thread.daemon = True
        thread.start()
        threads.append(thread)
        print(f"启动处理:{index + 1}/{len(ips.keys())}")
        
    # 等待所有线程完成
    for t in threads:
        t.join()
        
    # 处理结果
    for ip, (location, ip_num, error) in results.items():
        if error:
            errors.append(error)
            continue
            
        ip_location_map[ip] = location
        location_num_map[location] = location_num_map.get(location, 0) + ip_num
            
    return ip_location_map, location_num_map, errors








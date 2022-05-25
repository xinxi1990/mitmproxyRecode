import os
import time
import json
import csv
from mitmproxy import http
from mitmproxy import ctx

"""
接口用例流量录制
mitmdump -s cli_record.py
"""

currentPath = os.path.abspath(os.path.dirname(__file__))
currentTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
savePath = os.path.join(currentPath, currentTime + "-case.csv")

print("******************** Save Case Path: {savePath} ********************".format(savePath=savePath))

with open(savePath, 'a+') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(
        [["request_url", "request_headers", "request_method", "status_code", "response_data", "response_time"]])


def request(flow):
    print(flow.request.pretty_url)


def response(flow: http.HTTPFlow):
    # 加上过滤条件
    if "igetcool-gateway.igetcool.com" in str(flow.request.pretty_url) and 'GET' in str(flow.request.method):
        # 打开保存在本地的数据文件
        #print(flow.request.get_text())
        requestInfo = {}
        requestInfo['request_url'] = str(flow.request.pretty_url)
        data = json.loads(flow.response.content)
        requestInfo['request_headers'] = create_headers(flow.request.headers)
        requestInfo['request_method'] = flow.request.method
        requestInfo['status_code'] = flow.response.status_code
        requestInfo['reason'] = flow.response.reason
        requestInfo['response_data'] = data
        requestInfo['response_headers'] = create_headers(flow.response.headers)
        requestInfo['request_time_start'] = flow.request.timestamp_start
        requestInfo['request_time_end'] = flow.request.timestamp_end
        requestInfo['response_time_start'] = flow.response.timestamp_start
        requestInfo['response_time_end'] = flow.response.timestamp_end
        requestInfo['response_time'] = requestInfo['response_time_end'] - requestInfo['request_time_start'] # 响应时间
        print(requestInfo)
        with open(savePath, 'a+') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(
                [[requestInfo['request_url'], requestInfo['request_headers'], requestInfo['request_method'],
                  requestInfo['status_code'], requestInfo['response_data'], requestInfo['response_time']]])
            ctx.log('********************** 写入数据成功 ********************** ')



def create_headers(headers):
    """
    组装请求头
    :param headers:
    :return:
    """
    headersInfo = {}
    for k, v in headers.items():
        headersInfo[k] = v
    return headersInfo


def save_data(data, path):
    """
    保存数据
    :param data:
    :param path:
    :return:
    """
    header = list(data[0].keys())  # 数据列名
    with open(path, 'a+', newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writerows(data)  # 写入数据




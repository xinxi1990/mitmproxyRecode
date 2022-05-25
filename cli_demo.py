import time
import json
import random
from mitmproxy import http, ctx
from mitmproxy import flow


def request(flow):
    """
    修改请求头
    :param flow:
    :return:
    """
    # if "igetcool-gateway.igetcool.com" in str(flow.request.pretty_url):
    #     flow.request.headers["agent"] = "MitmProxy"

    if 'https://igetcool-gateway.igetcool.com/app-api-user-server/white/app/head/config.json' in str(
            flow.request.pretty_url):
        ctx.log.info("pretty host is: %s" % flow.request.pretty_host)
        flow.request.host = "localhost"
        flow.request.port = 3000
        flow.request.scheme = 'http'
        flow.request.url = flow.request.scheme + '://' + flow.request.host + ':' + flow.request.port + '/app-api-user-server/white/app/head/config.json'


def response(flow: http.HTTPFlow):
    # 加上过滤条件
    if "igetcool" in str(flow.request.pretty_url):
        with open("/Users/xinxi/Documents/zhihu/mitmproxyRecode/igetget.json", 'r') as f:
            resp_info = json.loads(f.read())
            print(resp_info)
        flow.response.set_text(json.dumps(resp_info))


        # flow.response.status_code = 404
        # flow.response = http.HTTPResponse.make(status_code=404)
        # flow.response = flow.response.make(404)
        # print(flow.response.status_code)
        # data = json.loads(flow.response.content)
        # print('------------------ 修改前 ------------------')
        # print(data)
        # """
        # {
        #     'code': 10000,
        #     'msg': '成功',
        #     'friendlyMsg': None,
        #     'data': {
        #         'isShow': 1,
        #         'showImg': 'https://coolcdn.igetcool.com/p/2022/4/a6f242f6af8725c2f9a28a97ae26a6fc.png?_96x96.png',
        #         'jumpUrl': 'igetcool://juvenile.dedao.app/go/h5?params_url=https%3A%2F%2Figetcool-share.igetcool.com%2Fgold-rule&params_title=学员金币商城',
        #         'type': 0,
        #         'goldNum': '0',
        #         'hasExchange': 0,
        #         'miniBarGoldDesc': '首次听完本节奖金币',
        #         'showMiniBarGoldDesc': 1
        #     }
        # }
        # """
        # print('------------------ 修改后 ------------------')
        # data['data']['isShow'] = 2
        # flow.response.set_text(json.dumps(data))
        # data = json.loads(flow.response.content)
        # print(data)

        # request_timestamp_start = flow.request.timestamp_start
        # random_time = random.randint(100, 1000)
        # print(random_time)
        # time.sleep(random_time / 1000)
        # response_timestamp_end = flow.response.timestamp_end
        # print(response_timestamp_end - request_timestamp_start)


# addons = [
#   LocalRedirect()
# ]
# def response(flow: http.HTTPFlow):
#     # 加上过滤条件
#     if 'https://igetcool-gateway.igetcool.com/app-api-user-server/white/app/head/config.json' in str(flow.request.pretty_url):
#         with open("/Users/xinxi/Documents/zhihu/mitmproxyRecode/igetget.json", 'r') as f:
#             resp_info =f.readlines()
#

with open("/Users/xinxi/Documents/zhihu/mitmproxyRecode/igetget.json", 'r') as f:
    resp_info = json.loads(f.read())
    print(resp_info)

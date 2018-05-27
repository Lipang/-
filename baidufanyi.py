import requests
import js2py
import re


class BaiDuTra(object):

    def __init__(self):
        js_path = './sign.js'
        js_content = open(js_path, 'r').read()
        self.query = None
        self.get_sign = js2py.eval_js(js_content)

    def get_gtk(self):
        url = 'http://fanyi.baidu.com/'
        headers = {
            'Host': 'fanyi.baidu.com',
            'Pragma': 'no-cache',
            'Referer': 'http://fanyi.baidu.com/translate',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
        html = requests.get(url, headers=headers)
        gtk = re.findall("window.gtk = '(.*?)';", html.text, re.S)[0]
        # token = re.findall("window\['common'].*token: '(.*?)',", html.text, re.S)[0]
        if gtk:
            return gtk
        else:
            self.get_gtk()

    def sign(self):
        gtk = self.get_gtk()
        sign = self.get_sign(self.query, gtk)
        if sign:
            return sign
        else:
            self.sign()

    def get_tra_result(self, query):
        self.query = query
        formdata = {
            'from': 'zh',
            'to': 'en',
            'query': self.query,
            'transtype': 'realtime',
            'simple_means_flah': '3',
            'sign': self.sign(),
            'token': 'e36c0008e24af63556147e1d2981825e'
        }

        api_url = 'http://fanyi.baidu.com/v2transapi'
        api_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '145',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'fanyi.baidu.com',
            'Origin': 'http://fanyi.baidu.com',
            'Pragma': 'no-cache',
            'Referer': 'http://fanyi.baidu.com/?aldtype=16047',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'BAIDUID=F36359083CC9F6ECF1B9E45831BD3434:FG=1; BIDUPSID=F36359083CC9F6ECF1B9E45831BD3434; PSTM=1520665479; BDUSS=1FyYWRSRGYybEFMZnFOU2h5aXczSGcxNGpzSlB1NVJhUWt4aGRpalpjV0hXc3RhQVFBQUFBJCQAAAAAAAAAAAEAAAC-hodTx6PHo87SsK4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIfNo1qHzaNaN; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; H_PS_PSSID=1422_21102_26350_22075; locale=zh; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1527329069,1527329430,1527388901,1527389189; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1527389189; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; PSINO=3'
        }

        response = requests.post(api_url, headers=api_headers, data=formdata)
        try:
            response = response.json()
            result = response['trans_result']['data'][0]['result'][0][1]
            print(f'“{self.query}” 的翻译结果: {result}\n')
        except KeyError:
            raise KeyError('出错了')


if __name__ == '__main__':
    baidu = BaiDuTra()
    while True:
        query = input('请输入你想翻译的汉字: ')
        baidu.get_tra_result(query)



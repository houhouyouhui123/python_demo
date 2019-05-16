from hashlib import md5
import requests
import random
import time
word='over my views'
def generateSaltSign():
    ts=int(time.time()*1000)
    salt=ts+random.randint(1,10)
    sign=md5(('fanyideskweb' + 'over my views' + str(salt) + '@6f#X3=cCuncYssPsuRUE').encode()).hexdigest()
    return {
        'ts':ts,
        'salt':salt,
        'sign':sign,
    }
url='http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
headers={
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Content-Length':'243',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie':'OUTFOX_SEARCH_USER_ID=-1884483442@10.169.0.82; JSESSIONID=aaaGrel76FnozchuO7_Qw; OUTFOX_SEARCH_USER_ID_NCOO=2086495007.0305252; ___rl__test__cookies=1557992926979',
    'Host':'fanyi.youdao.com',
    'Origin':'http://fanyi.youdao.com',
    'Proxy-Connection':'keep-alive',
    'Referer':'http://fanyi.youdao.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
'X-Requested-With':'XMLHttpRequest',
}
tss=generateSaltSign()
formData={
    'i': word,
    'from': 'AUTO',
    'to': 'AUTO',
    'smartresult': 'dict',
    'client': 'fanyideskweb',
    'salt': tss['salt'],
    'sign': tss['sign'],
    'ts': tss['ts'],
    'bv': '316dd52438d41a1d675c1d848edf4877',
    'doctype': 'json',
    'version': '2.1',
    'keyfrom': 'fanyi.web',
    'action': 'FY_BY_REALTlME',
}
response=requests.post(url=url,headers=headers,data=formData).content.decode()
print(response)

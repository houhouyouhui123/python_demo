import requests
def getSum():
    a=1;
    sum=0
    for i in range(10):
        sum+=i
    return sum
content=requests.get('https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&1556106018122&callback=jQuery19105126889239847986_1556105964746&_=1556105964747').content.decode('gzip')
print(content)





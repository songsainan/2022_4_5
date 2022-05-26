import requests


from common.handle_conf import confger


class SetupFun:
    @classmethod
    def user_login(cls):
        url = 'http://api.lemonban.com/futureloan/member/login'
        head = confger.get('evn', 'head')
        body = {'mobile_phone': confger.get('evn', 'mobile_phone'),
                'pwd': confger.get('evn', 'pwd')}
        response = requests.request(method='post', url=url, headers=head, json=body)
        res = response.json()
        return res


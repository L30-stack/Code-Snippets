import requests
import math

url = "http://192.168.178.112/api/*/lights/4/state"

class Hue:
    def __init__(self, ip, code, lamp= []):
        self.url_snipped = f'http://{str(ip)}/api/{str(code)}/lights/'
        self.lamp = lamp
        self.requ = requests.get(self.url_snipped)
        if self.requ.status_code == 200:
            print('[HUE] connected')
        else:
            print('[Hue] Error connecting given URL')

    def mode(self, mode):
        dic = {'ON':{'on':True}, 'OFF':{'on':False}}
        if mode in dic:
            self.data = dic[mode]
        else:
            return
        for i in self.lamp:
            self.url = self.url_snipped + str(i) + '/state'
            print(self.url)
            requests.put(url, verify=False, json=self.data)

    def color(self, r, g, b):
        try:
            if int(r) <= 255 and int(g) <= 255 and int(b) <= 255:
                self.rgb_colors = [float(int(r)/255),float(int(g)/255),float(int(b)/255)]
            else:
                for i,j in [[r,'red'],[g,'green'],[b,'blue']]:
                    if i > 255:
                        print(f'Value for {j} with {i} is over 255!')
                return
        except ValueError:
            print('Invalid input!')
            return

        self.X = (self.rgb_colors[0] * 0.649926) + (self.rgb_colors[1] * 0.103455) + (self.rgb_colors[2] * 0.197109)
        self.Y = (self.rgb_colors[0] * 0.234327) + (self.rgb_colors[1] * 0.743075) + (self.rgb_colors[2] * 0.022598)
        self.Z = (self.rgb_colors[0] * 0.0000000) + (self.rgb_colors[1] * 0.053077) + (self.rgb_colors[2] * 1.035763)

        self.x_val = self.X / (self.X + self.Y + self.Z)
        self.y_val = self.Y / (self.X + self.Y + self.Z)

        self.data = {'0':(round(self.x_val, 4)), '1':(round(self.y_val, 4))}
        print(self.data)

        for i in self.lamp:
            self.url = self.url_snipped + str(i) + '/state/xy'
            requests.put(url, json=self.data)
        

    def brigtness (self, ipt = 100):
        try:
            self.data = {'bri': int(ipt)}
        except ValueError:
            print('Invalid input!')
        for i in self.lamp:
            self.url = self.url_snipped + str(i) + '/state'
            requests.put(url, verify=False, json=self.data)

    def seturation (self, ipt):
        return
Hue = Hue('192.168.178.112', '*', ['4'])
Hue.color(55,65,250)


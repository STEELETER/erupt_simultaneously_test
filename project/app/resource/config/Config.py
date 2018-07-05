


import winreg

# 获取桌面路径
def desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]

app_qss = './src/client/UnFrameStyle.qss'

client_shadow_left_top = './src/client/shadow/shadow_left_top.png'
client_shadow_left_bottom = './src/client/shadow/shadow_left_bottom.png'
client_shadow_right_top = './src/client/shadow/shadow_right_top.png'
client_shadow_right_bottom = './src/client/shadow/shadow_right_bottom.png'
client_shadow_top = './src/client/shadow/shadow_top.png'
client_shadow_bottom = './src/client/shadow/shadow_bottom.png'
client_shadow_left = './src/client/shadow/shadow_left.png'
client_shadow_right = './src/client/shadow/shadow_right.png'

client_title = "./src/client/title01.png"
client_ico = './src/client/logo.ico'

def web_url(mainPath):
    print(mainPath+'/src/web/App.html')
    return 'file:///'+mainPath+'/src/web/app.html'




#选择上传文件的默认打开地址
selectfile_path = desktop()

#下载文件的默认导出地址
exportfile_path = desktop()

sns_ip = '172.21.1.172'
sns_port = '7000'
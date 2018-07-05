import hashlib
import os



#计算文件的md值
def getFileMd5(filepath):
    with open(filepath,'rb') as f:
         md5obj = hashlib.md5()
         md5obj.update(f.read())
         hash = md5obj.hexdigest()
         return str(hash)


if __name__ =="__main__":
    print(getFileMd5("F:/eclipse-jee-kepler-SR2-win32.zip"))

import ctypes
from _ctypes import Structure

import struct

"""
unsigned char key[16]={0x2b,0x7e,0x15,0x16,0x28,0xae,0xd2,0xa6,0xab,0xf7,0x15,0x88,0x09,0xcf,0x4f,0x3c};
sm4_context ctx;
//加密
sm4_setkey_enc(&ctx,key);
unsigned char input[16], output[16];
sm4_crypt_ecb(&ctx,1,16,input,output);
//解密
sm4_setkey_dec(&ctx,key);
unsigned char input[16], output[16];
sm4_crypt_ecb(&ctx,1,16,input,output);
"""
# data_str = 'glahsfdchuangain'
# key={0x2b,0x7e,0x15,0x16,0x28,0xae,0xd2,0xa6,0xab,0xf7,0x15,0x89,0x08,0xcf,0x4f,0x3c}
# adll = ctypes.cdll.LoadLibrary('C:/Users/zhongcun/Desktop/CryptLib.dll')
# print(adll.sm4_setkey_enc(Pyth_C,str(key)))


from ctypes import *

data= '98666666668'

class Pyth_C(Structure):
    _fields_ = []
p = Pyth_C()
p.data = data

if __name__ == '__main__':
    key = { 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x89, 0x08, 0xcf, 0x4f, 0x3c}
    a = "5eb63bbbe01eeed093cb22bb8f5acdc3"
    keys = struct.unpack("4i",a[:16].encode())
    adll = ctypes.cdll.LoadLibrary('C:/Users/zhongcun/Desktop/CryptLib.dll')
    adll.sm4_setkey_enc(byref(p),str(keys))
    # input  = struct.unpack("4i",a[:16].encode())
    input = struct.unpack('4i',a[:16].encode())
    input=[0x5a]*16
    output = []
    adll.sm4_crypt_ecb(byref(p), 1, 16, str(input).encode())
    # print(output)
    print(adll.sm4_setkey_dec(byref(p)))








# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 21:19:37 2023

@author: HP
"""

import qrcode

def qrCodeGenerate(dataString):
    img = qrcode.make(dataString)
    img.save('sourceQRCode.jpg')

    
    
    


# !/usr/bin/python
# -*- coding=utf-8 -*-
"""
    @author: tangjialiang
    @date: 2016-07-01
    @desc: 解析任务,向环球wifi下订单
"""
from common.logger import logger
import requests
import json
import base64
import re
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


ERROR_TASK_CONTENT= 12
ERROR_DATA_NONE = 24
ERROR_UNKNOWN_TYPE = 25
ERROR_TICKETS_NONE = 29

class Message:
    def __init__(self):
        self.message = """
        <request>
<header>
 	<accountId>{accountId}</accountId>
 	<serviceName>{serviceName}</serviceName>
	<requestTime>{requestTime}</requestTime>
	<version>{version}</version>
	<sign>{sign}</sign>
</header>
<body>
	<productId>{productId}</productId>
	<price>{price}</price>
	<count>{count}</count>
 	<contactName>{contactName}</contactName>
	<contactMobile>{contacntMobile}</contactMobile>
 	<useDate>{useData}</useDate>
 	<useEndDate>{useEndDate}</useEndDate>
	<extendInfo>
		<takeAddress>2</takeAddress>
 		<returnAddress>4</returnAddress>
		<deliveryMessages>
					<deliveryMessage>
							<province>上海市</province>
							<city>上海市</city>
							<district>长宁区</district>
							<address>福泉路99号402室 200335	</address>
					</deliveryMessage>
		</deliveryMessages>
	</extendInfo>
 </body>
</request>
        """
        pass

    def getMessage(self):
        return self.message

    def set(self):
        pass

class API :
    def __init__(self):
        self._url = "http://uibp.uroaming.cn/open/order/"
        self.securityKey = '123456'
        self.accountId = 'Mioji'
        self.version = '2.0'
        self.requestTime = ''
        pass

    def verifyOrder(self):
        pass

    def creatOrder(self):
        pass

    def CancelOrder(self):
        pass

    def QueryOrder(self):
        pass

    def requestAction(self, data):
        pass

def NoticeOrderConsumed(data):
    pass

if __name__ == '__main__' :
    pass

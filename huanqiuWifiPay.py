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
import hashlib
import re
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

ERROR_TASK_CONTENT= 12
ERROR_DATA_NONE = 24
ERROR_UNKNOWN_TYPE = 25
ERROR_TICKETS_NONE = 29


# pattern
pattern_body = re.compile(r"<body>.*</body>")
pattern_body_content = re.compile(r"<body>(.*)</body>")


class Message:
    def __init__(self):
        self.message = ''

    def _getBodyContent(self):
        # 返回body节点的内容
        body_content = pattern_body_content.search(self.message).group(1)
        return body_content

    def _getBody(self):
        # 返回body节点和内容
        body = pattern_body.search(self.message).group()
        return body

    def _bodyEnBase64(self):
        # 得到body
        body = self._getBody()
        # encode(64)
        codedBody = base64.b64encode(body)
        # 替换原body
        tempStr = "<body>{content}</body>".format('content', codedBody)
        pattern_body.sub(tempStr, self.message)

    def formatMessage(self, data):
        pass

    def getMessage(self, data):
        self.formatMessage(data)
        return self.message


class VerifyMessage(Message):
    def __init__(self):
        self.message = """<request><header><accountId>{accountId}</accountId><serviceName>{serviceName}</serviceName><requestTime>{requestTime}</requestTime><version>{version}</version><sign>{sign}</sign></header><body><productId>{productId}</productId><price>{price}</price><count>{count}</count><contactName>{contactName}</contactName><contactMobile>{contacntMobile}</contactMobile><useDate>{useDate}</useDate><useEndDate>{useEndDate}</useEndDate><extendInfo><takeAddress>{takeAddress}</takeAddress><returnAddress>{returnAddress}</returnAddress><deliveryMessages>{deliveryMessage}</deliveryMessages></extendInfo></body></request>"""

    def _addDeliveryMessage(self, data):
        totalStr = ''
        for deliver in data.get('delivers'):
            tempStr = """<deliveryMessage><province>{province}</province><city>{city}</city><district>{district}</district><address>{address}</address></deliveryMessage>"""
            tempStr.format('province', deliver.get('province'))
            tempStr.format('city', deliver.get('city'))
            tempStr.format('district', deliver.get('district'))
            tempStr.format('address', deliver.get('address'))
            totalStr = totalStr + tempStr

        self.message.format('deliveryMessage', totalStr)

    def formatMessage(self, data):
        # header 填充
        self.message.format('accountId', data.get('accountId'))
        self.message.format('serviceName', data.get('serviceName'))
        self.message.format('requestTime', data.get('requestTime'))
        self.message.format('version', data.get('version'))

        # body 填充
        self.message.format('productId', data.get('productId'))
        self.message.format('price', data.get('price'))
        self.message.format('contactName', data.get('contactName'))
        self.message.format('contactMobile', data.get('contactMobile'))
        self.message.format('useDate', data.get('useDate'))
        self.message.format('useEndDate', data.get('useEndDate'))

        # 额外信息 填充
        self.message.fromat('takeAddress', data.get('takeAddress'))
        self.message.format('returnAddress', data.get('returnAddress'))
        self._addDeliveryMessage(data)

        #encode
        self._bodyEnBase64()

        #签名 填充
        body_content = self._getBodyContent()
        tempStr = data.get('accountId') + data.get("serviceName") + data.get("requestTime") + data.get("version") + body_content
        hash_md5 = hashlib.md5(tempStr)
        sign = (hash_md5.hexdigest()).lower()
        self.message.format('sign', sign)



class CreateMessage:
    def __init__(self):
        self.message = """<request><header><accountId>{accountId}</accountId><serviceName>{serviceName}</serviceName><requestTime>{requestTime}</requestTime><version>{version}</version><sign>{sign}</sign></header><body><productId>{productId}</productId><price>{price}</price><count>{count}</count><contactName>{contactName}</contactName><contactMobile>{contacntMobile}</contactMobile><useDate>{useDate}</useDate><useEndDate>{useEndDate}</useEndDate><extendInfo><takeAddress>{takeAddress}</takeAddress><returnAddress>{returnAddress}</returnAddress><deliveryMessages>{deliveryMessage}</deliveryMessages></extendInfo></body></request>"""
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
            <otaOrderId>{otaOrderId}</otaOrderId>
            <productId>{productId}</productId>
            <otaProductName>{otaProductName}</otaProductName>
            <price>{price}</price>
            <count>{count}</count>
            <contactName>{contactName}</contactName>
            <contactMobile>{contantMobile}</contactMobile>
            <useDate>{useDate}</useDate>
            <useEndDate/>
            <remark/>
            <extendInfo>
                <deposit>{desposit}</deposit>
                <depositMode>{depositMode}</depositMode>
                <disAmount>{disAmount}</disAmount>
                <getAddress>{getAddress}</getAddress>
                <returnAddress>{returnAddress}</returnAddress>
                <deliveryMessages>
                    {deliveryMessage}
                </deliveryMessages>
            </extendInfo>
        </body>
        </request>
        """

    def _addDeliveryMessage(self, data):
        totalStr = ''
        for deliver in data.get('delivers'):
            tempStr = """<deliveryMessage><province>{province}</province><city>{city}</city><district>{district}</district><address>{address}</address></deliveryMessage>"""
            tempStr.format('province', deliver.get('province'))
            tempStr.format('city', deliver.get('city'))
            tempStr.format('district', deliver.get('district'))
            tempStr.format('address', deliver.get('address'))
            totalStr = totalStr + tempStr

        self.message.format('deliveryMessage', totalStr)

    def formatMessage(self, data):
        # header 填充
        self.message.format('accountId', data.get('accountId'))
        self.message.format('serviceName', data.get('serviceName'))
        self.message.format('requestTime', data.get('requestTime'))
        self.message.format('version', data.get('version'))

        # body 填充
        self.message.format('otaOrderId', data.get('otaOrderId'))
        self.message.format('productId', data.get('productId'))
        self.message.format('otaProductName', data.get('otaProductName'))
        self.message.format('price', data.get('price'))
        self.message.format('count', data.get('count'))
        self.message.format('contactName', data.get('contactName'))
        self.message.format('contactMobile', data.get('contactMobile'))
        self.message.format('useDate', data.get('useDate'))
        self.message.format('useEndDate', data.get('useEndDate'))
        self.message.format('remark', data.get('remark'))

        # 额外信息 填充
        self.message.format('deposit', data.get('desposit'))
        self.message.format('depostiMode', data.get('depostiMode'))
        self.message.format('disAmount', data.get('disAmount'))
        self.message.format('getAddress', data.get('getAddress'))
        self.message.format('returnAddress', data.get('returnAddress'))
        self._addDeliveryMessage(data)

        #encode
        self._bodyEnBase64()

        #签名 填充
        body_content = self._getBodyContent()
        tempStr = data.get('accountId') + data.get("serviceName") + data.get("requestTime") + data.get("version") + body_content
        hash_md5 = hashlib.md5(tempStr)
        sign = (hash_md5.hexdigest()).lower()
        self.message.format('sign', sign)


class CancelMessage:
    def __init__(self):
        self.messge = """
        <request>
        <header>
            <accountId>{account}</accountId>
            <serviceName>{serviceName}</serviceName>
            <requestTime>{requestTime}</requestTime>
            <version>{version}</version>
            <sign>{sign}</sign>
        </header>
        <body>
            <otaOrderId>{otaOrderId}</otaOrderId>
            <vendorOrderId>{vendorOrderId}</vendorOrderId>
            <sequenceId>{sequenceId}</sequenceId>
            <cancelCount>{cancelCount}</cancelCount>
        </body>
        </request>
        """

    def formatMessage(self, data):
        # header 填充
        self.message.format('accountId', data.get('accountId'))
        self.message.format('serviceName', data.get('serviceName'))
        self.message.format('requestTime', data.get('requestTime'))
        self.message.format('version', data.get('version'))

        # body 填充
        self.message.format('otaOrderId', data.get('otaOrderId'))
        self.message.format('vendorOrderId', data.get('vendorOrderId'))
        self.message.format('sequenceId', data.get('sequenceId'))
        self.message.format('cancelCount', data.get('cancelCount'))

        #encode
        self._bodyEnBase64()

        #签名 填充
        body_content = self._getBodyContent()
        tempStr = data.get('accountId') + data.get("serviceName") + data.get("requestTime") + data.get("version") + body_content
        hash_md5 = hashlib.md5(tempStr)
        sign = (hash_md5.hexdigest()).lower()
        self.message.format('sign', sign)


class QueryMessage:
    def __init__(self):
        self.messge = """
            <request>
            <header>
                <accountId>{account}</accountId>
                <serviceName>{serviceName}</serviceName>
                <requestTime>{requestTime}</requestTime>
                <version>{version}</version>
                <sign>{sign}</sign>
            </header>
            <body>
                <otaOrderId>{otaOrderId}</otaOrderId>
                <vendorOrderId>{vendorOrderId}</vendorOrderId>
            </body>
            </request>
            """

    def formatMessage(self, data):
        # header 填充
        self.message.format('accountId', data.get('accountId'))
        self.message.format('serviceName', data.get('serviceName'))
        self.message.format('requestTime', data.get('requestTime'))
        self.message.format('version', data.get('version'))

        # body 填充
        self.message.format('otaOrderId', data.get('otaOrderId'))
        self.message.format('vendorOrderId', data.get('vendorOrderId'))

        #encode
        self._bodyEnBase64()

        #签名 填充
        body_content = self._getBodyContent()
        tempStr = data.get('accountId') + data.get("serviceName") + data.get("requestTime") + data.get("version") + body_content
        hash_md5 = hashlib.md5(tempStr)
        sign = (hash_md5.hexdigest()).lower()
        self.message.format('sign', sign)


class API :
    def __init__(self):
        self._url = "http://uibp.uroaming.cn/open/order/"
        self.securityKey = '123456'
        self.accountId = 'Mioji'
        self.version = '2.0'
        self.requestTime = ''

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

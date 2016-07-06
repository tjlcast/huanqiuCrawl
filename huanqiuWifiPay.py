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
import testData
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# error
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
        self.errorCode = 0

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
        tempStr = "<body>{content}</body>".format(content=codedBody)
        self.message = pattern_body.sub(tempStr, self.message)

    def formatMessage(self, data):
        pass

    def getMessage(self, data):
        self.formatMessage(data)
        return self.message, self.errorCode


class VerifyMessage(Message):
    def __init__(self):
        self.message = """<request><header><accountId>{accountId}</accountId><serviceName>{serviceName}</serviceName><requestTime>{requestTime}</requestTime><version>{version}</version><sign>{sign}</sign></header><body><productId>{productId}</productId><price>{price}</price><count>{count}</count><contactName>{contactName}</contactName><contactMobile>{contactMobile}</contactMobile><useDate>{useDate}</useDate><useEndDate>{useEndDate}</useEndDate><extendInfo><takeAddress>{takeAddress}</takeAddress><returnAddress>{returnAddress}</returnAddress><deliveryMessages>{deliveryMessage}</deliveryMessages></extendInfo></body></request>"""
        self.message = self.message.replace(' ', '').replace('\n', '').replace('\t', '')

    def _addDeliveryMessage(self, data):
        totalStr = ''
        for deliver in data:
            tempStr = """<deliveryMessage><province>{province}</province><city>{city}</city><district>{district}</district><address>{address}</address></deliveryMessage>"""
            totalStr = totalStr + tempStr.format(**deliver)
        return totalStr

    def formatMessage(self, data):
        # 封装'deliveryMessage'的数据
        try:
            tempDeliveryMessage = self._addDeliveryMessage(data.get('deliveryMessage'))
            # 得到header body extendInfo deliveryMessage的 封装数据
            infoDict = dict(data.get('header').items() + data.get('body').items() + data.get('extendInfo').items())
            infoDict['deliveryMessage'] = tempDeliveryMessage
            self.message = self.message.format(**infoDict)
        except Exception, e:
            self.errorCode = 1
            logger.error('VeriyMessage: error occured in generating message dict! (%s)' % e)

        #encode
        try:
            self._bodyEnBase64()
        except Exception, e:
            self.errorCode = 1
            logger.error('VeriyMessage: messaeg encode base64 wrongly! (%s)' % e)

        #签名 填充
        try:
            body_content = self._getBodyContent()
            tempStr = data.get('header').get('accountId') + data.get('header').get("serviceName") + data.get(
                'header').get("requestTime") + data.get('header').get("version") + body_content
            hash_md5 = hashlib.md5(tempStr)
            sign = (hash_md5.hexdigest()).lower()
            self.message = self.message.replace('<sign></sign>', '<sign>' + sign + '</sign>')
        except Exception, e:
            self.errorCode = 1
            logger.error('VeriyMessage: error occured in generating sign! (%s)' % e)


class CreateMessage(Message):
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
        self.message = self.message.replace(' ', '').replace('\n', '').replace('\t', '')

    def _addDeliveryMessage(self, data):
        totalStr = ''
        for deliver in data:
            tempStr = """<deliveryMessage><province>{province}</province><city>{city}</city><district>{district}</district><address>{address}</address></deliveryMessage>"""
            totalStr = totalStr + tempStr.format(**deliver)
        return totalStr

    def formatMessage(self, data):
        # 封装'deliveryMessage'的数据
        try:
            tempDeliveryMessage = self._addDeliveryMessage(data.get('deliveryMessage'))
            # 得到header body extendInfo deliveryMessage的 封装数据
            infoDict = dict(data.get('header').items() + data.get('body').items() + data.get('extendInfo').items())
            infoDict['deliveryMessage'] = tempDeliveryMessage
        except Exception, e:
            self.errorCode = 1
            logger.error("CreateMessage: error occured in generating message dict! (%s)" % e)

        try:
            self.message = self.message.format(**infoDict)
        except Exception, e:
            self.errorCode = 1
            logger.error('CreateOrderMessage: format message occur error(%s)!' % e)

        # encode
        try:
            self._bodyEnBase64()
        except Exception, e:
            self.errorCode = 1
            logger.error('CreateOrderMessage: message encoded base64 wrongly! (%s)' % e)

        # 签名 填充
        try:
            body_content = self._getBodyContent()
            tempStr = data.get('header').get('accountId') + data.get('header').get("serviceName") + data.get(
                'header').get(
                "requestTime") + data.get('header').get("version") + body_content
            hash_md5 = hashlib.md5(tempStr)
            sign = (hash_md5.hexdigest()).lower()
            self.message = self.message.replace('<sign></sign>', '<sign>' + sign + '</sign>')
        except Exception, e:
            self.errorCode = 1
            logger.error('CreateOrderMessage: error occured in generating sign')


class CancelMessage(Message):
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
        self.message = self.message.replace(' ', '').replace('\n', '').replace('\t', '')

    def formatMessage(self, data):
        # 得到header body的 封装数据
        try:
            infoDict = dict(data.get('header').items() + data.get('body').items())
        except Exception, e:
            self.errorCode = 1
            logger.error('CancelMessageOrder: error occured in generating message dict! (%s)' % e)

        try:
            self.message = self.message.format(**infoDict)
        except Exception, e:
            self.errorCode = 1
            logger.error('CancelOrderMessage: format message occur error(%s)!' % e)

        # encode
        try:
            self._bodyEnBase64()
        except Exception, e:
            self.errorCode = 1
            logger.error('CancelOrderMessage: message encoded base64 wrongly! (%s)' % e)

        # 签名 填充
        try:
            body_content = self._getBodyContent()
            tempStr = data.get('header').get('accountId') + data.get('header').get("serviceName") + data.get(
                'header').get(
                "requestTime") + data.get('header').get("version") + body_content
            hash_md5 = hashlib.md5(tempStr)
            sign = (hash_md5.hexdigest()).lower()
            self.message = self.message.replace('<sign></sign>', '<sign>' + sign + '</sign>')
        except Exception, e:
            self.errorCode = 1
            logger.error('CancelOrderMessage: error occured in generating sign! (%s)' % e)


class QueryMessage(Message):
    def __init__(self):
        self.message = """
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
        self.message = self.message.replace(' ', '').replace('\n', '').replace('\t', '')

    def formatMessage(self, data):
        # 得到header body的 封装数据
        try:
            infoDict = dict(data.get('header').items() + data.get('body').items())
        except Exception, e:
            self.errorCode = 1
            logger.error('QueryMessage: error occured in generating message dict! (%s)' % e)

        try:
            self.message = self.message.format(**infoDict)
        except Exception, e:
            self.errorCode = 1
            logger.error('QueryOrderMessage: format message occur error(%s)!' % e)

        # encode
        try:
            self._bodyEnBase64()
        except Exception, e:
            self.errorCode = 1
            logger.error('QueryOrderMessage: error occured in base64 encoding! (%s)' % e)

        # 签名 填充
        try:
            body_content = self._getBodyContent()
            tempStr = data.get('header').get('accountId') + data.get('header').get("serviceName") + data.get(
                'header').get(
                "requestTime") + data.get('header').get("version") + body_content
            hash_md5 = hashlib.md5(tempStr)
            sign = (hash_md5.hexdigest()).lower()
            self.message = self.message.replace('<sign></sign>', '<sign>' + sign + '</sign>')
        except Exception, e:
            self.errorCode = 1
            logger.error('QueryOrderMessage: error occured in generating sign!(%s)' % e)


class API :
    def __init__(self):
        self._url = "http://uibp.uroaming.cn/open/order/"
        self.securityKey = '123456'
        self.accountId = 'Mioji'
        self.version = '2.0'
        self.requestTime = ''

        self.errorCode = 0
        self.data = None

    def _verifyOrder(self, inputData):
        # 需要对传入的data进行解析,并装配为标准格式
        data = {
            'header': '',
            'body': '',
            'extendInfo': '',
            'deliverMessage': ''
        }

        message = VerifyMessage()
        sendStr, errorCode = message.getMessage(data)
        if errorCode != 0:
            return None
        rstr = self._requestAction(self._url, sendStr)
        return rstr

    def _creatOrder(self, inputData):
        # 需要对传入的data进行解析,并装配为标准格式
        data = {
            'header': '',
            'body': '',
            'extendInfo': '',
            'deliverMessage': '',
        }
        message = CreateMessage()
        sendStr, errorCode = message.getMessage(data)
        if errorCode != 0:
            return None
        rstr = self._requestAction(self._url, sendStr)
        return rstr

    def _cancelOrder(self, inputData):
        # 需要对传入的data进行解析,并装配为标准格式
        data = {
            'header': '',
            'body': '',
        }
        message = CancelMessage()
        sendStr, errorCode = message.getMessage(data)
        if errorCode != 0 :
            return None
        rstr = self._requestAction(self._url, sendStr)
        return rstr

    def _queryOrder(self, inputData):
        # 需要对传入的data进行解析,并装配为标准格式
        data = {
            'header': '',
            'body': '',
        }
        message = QueryMessage()
        sendStr, errorCode = message.getMessage(data)
        if errorCode != 0:
            return None
        rstr = self._requestAction(self._url, sendStr)
        return rstr

    def _requestAction(self, url, sendStr):
        header = {'Content-Type': 'text/xml'}
        returnStr = requests.post(url, headers=header, data=sendStr)
        return returnStr

    def init_pay_info(self, data):
        result = {'error': '1', 'msg': 'init_pay_info failed!'}
        try:
            self.data = data
        except Exception, e:
            result['msg'] = 'init_pay_info failed, look at the log file in detail'
            raise
        return result

    def create_order(self):
        assert self.data != None and self.data.get('verigyData')!=None and self.data.get('createData')!=None
        # 验证成功后
        rVerify = self._verifyOrder(self.data['verifyData'])
            # if !(header > resultCode == '0000' and header > resultMessage == '验证成功'):
            #       return 下单失败
        #订单下单
        rCreate = self._creatOrder(self.data['createData'])

    def do_charge(self, data):
        # 目前环求wifi还未提供do_charge相关业务功能
        pass

    def query_order(self):
        assert self.data!=None and self.data.get('queryData')!=None
        #查询订单
        rQuery = self._queryOrder(self.data['queryData'])

    def cancel_order(self):
        assert self.data!=None and self.data.get('cancelData')!=None
        #取消订单
        rCancel = self._cancelOrder(self.data['cancelData'])

    def NoticeOrderConsumed(self, data):
        pass

if __name__ == '__main__' :
    data = {
        'verifyData': testData.VerifyTestData,
        'createData': testData.CreateTestData
    }
    api = API()
    api.init_pay_info(data)
    api.create_order()

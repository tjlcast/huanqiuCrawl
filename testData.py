#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)

sys.setdefaultencoding('utf-8')

#testData
VerifyTestData = {
    'header' : {
        'accountId': 'Mioji',
        'serviceName': 'VerifyOrder',
        'requestTime': '2015-10-19 16:05:31',
        'version': '2.0',
        'sign': ''
    },
    'body' : {
        'productId': '1',
        'price': '100',
        'count': '1',
        'contactName': 'test',
        'contactMobile': '13011111111',
        'useDate': '2015-05-20',
        'useEndDate': '2015-5-30',
    },
    'extendInfo' : {
        'takeAddress' : '2',
        'returnAddress' : '4',
    },
    'deliveryMessage' : [
        {
            'province' : '上海市' ,
            'city' : '上海市' ,
            'district' : '长宁区' ,
            'address' : '福泉路99号402室 200335'
        }
    ]
}


CreateTestData = {
    'header' : {
        'accountId': 'Mioji',
        'serviceName': 'VerifyOrder',
        'requestTime': '2015-10-19 16:05:31',
        'version': '2.0',
        'sign': ''
    },
    'body' : {
        'otaOrderId' : '123456',
        'productId': '1',
        'otaProductName': '测试产品',
        'price': '100',
        'count': '1',
        'contactName': 'test',
        'contactMobile': '13011111111',
        'useDate': '2015-05-20',
        'useEndDate': '2015-5-30',
    },
    'extendInfo': {
        'deposit' : '500',
        'depositMode' : '0',
        'disAmount': '10',
        'getAddress': '2',
        'returnAddress': '4',
    } ,
    'deliveryMessage' : [
        {
            'province': '上海市',
            'city': '上海市',
            'district': '长宁区',
            'address': '福泉路99号402室 200335'
        }
    ]
}


CancelTestData = {
    'header': {
        'accountId': 'Mioji',
        'serviceName': 'VerifyOrder',
        'requestTime': '2015-10-19 16:05:31',
        'version': '2.0',
        'sign': ''
    },
    'body' : {
        'otaOrderId' : '123456',
        'vendorOrderId' : '10001',
        'sequenceId' : '123456001',
        'cancelCount' : '1'
    }
}


QueryTestData = {
    'header' : {
        'accountId' : 'Mioji' ,
        'serviceName' : 'VerifyOrder' ,
        'requestTime' : '2015-05-19 16:05:31' ,
        'version' : '2.0' ,
        'sign' : ''
    },
    'body' : {
        'otaOrderId' : '123456' ,
        'vendorOrderId' : '10001' ,
    }
}

#!/usr/bin/env python
#encoding=utf-8
#  Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# author: liushun@alibaba-inc.com 2016.08.29

import time
import base64
import hashlib
import httplib
import uuid
import hmac

class SMSClient:
    def __init__(self, app_key, app_secret):
        self.__app_key, self.__app_secret = app_key, app_secret

    def send(self, receiver, sign, template_code, parameters='{}'):
        print receiver, sign, template_code, parameters
        self.__host = 'sms.market.alicloudapi.com'
        self.__str_uri = '/singleSendSms?ParamString=%s&RecNum=%s&SignName=%s&TemplateCode=%s' % (parameters, receiver, sign, template_code)
        print self.__str_uri
        self.build_headers()
        self.__connection = httplib.HTTPConnection(self.__host, 80)
        self.__connection.connect()
        print self.__headers
        self.__connection.request('GET', self.__str_uri, headers=self.__headers)
        response = self.__connection.getresponse()
        return response.status, response.getheaders(), response.read()

    def build_headers(self):
        headers = dict()
        headers['X-Ca-Key'] = self.__app_key
        headers['X-Ca-Nonce'] = str(uuid.uuid4())
        headers['X-Ca-Timestamp'] = str(int(time.time() * 1000))
        headers['X-Ca-Signature-Headers'] = 'X-Ca-Key,X-Ca-Nonce,X-Ca-Timestamp'
        str_header = '\n'.join('%s:%s' % (k, headers[k]) for k in ['X-Ca-Key','X-Ca-Nonce','X-Ca-Timestamp'])
        str_to_sign = '%s\n\n\n\n\n%s\n%s' % ('GET', str_header, self.__str_uri)
        headers['X-Ca-Signature'] = self.__get_sign(str_to_sign, self.__app_secret)
        self.__headers = headers

    def __get_sign(self, source, secret):
        h = hmac.new(secret, source, hashlib.sha256)
        signature = base64.encodestring(h.digest()).strip()
        return signature

if __name__ == '__main__':
    cli = SMSClient(app_key="2******6", app_secret="0******************************7")
    print cli.send('136********', '示例', 'SMS_1******2' )


#!/usr/bin/env bash
#数据市场短信发送shell示例
#author: liushun@alibaba-inc.com 2016.08.29

RECEIVER=136********      #接收方手机号
SIGN="示例"               #签名
TEMP_CODE="SMS_1*******"  #短信模板
PARAMS="{\"time\":\"`date +%Y%m%d%H%M%S`\"}" #参数（json）

K="2******6" #AppKey，从管理控制台获取，下同
S="0******************************7" #AppSecret

NL="
"
[ "x`uname`" = "xDarwin" ] && {
    NONCE="`uuidgen`"
    TIMESTAMP="`date +%s`500"
} || {
    NONCE="`uuid`"
    TIMESTAMP="`date +%s%3N`"
}
STR_HEADER="X-Ca-Key:$K${NL}X-Ca-Nonce:$NONCE${NL}X-Ca-Timestamp:$TIMESTAMP"
STR_URI="/singleSendSms?ParamString=$PARAMS&RecNum=$RECEIVER&SignName=$SIGN&TemplateCode=$TEMP_CODE"
STR_TO_SIGN="GET${NL}${NL}${NL}${NL}${NL}$STR_HEADER${NL}$STR_URI"
SIGN="`/bin/echo -n "$STR_TO_SIGN" | openssl dgst -sha256 -hmac "$S" | sed 's/.* //g' | xxd -r -p | base64`"
STR_URI="`echo "$STR_URI" | sed 's#{#\\\\{#g;s#}#\\\\}#g'`"
curl -H 'Accept:' \
	-H "X-Ca-Key: $K" \
	-H "X-Ca-Nonce: $NONCE" \
	-H "X-Ca-Timestamp: $TIMESTAMP" \
	-H "X-Ca-Signature-Headers: X-Ca-Key,X-Ca-Nonce,X-Ca-Timestamp" \
	-H "X-Ca-Signature: $SIGN" \
	"http://sms.market.alicloudapi.com$STR_URI"


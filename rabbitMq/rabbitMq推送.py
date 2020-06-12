import pika
import json

user_pwd = pika.PlainCredentials("umsMQ", '123456')
s_conn = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1', port='5672', virtual_host='/', credentials=user_pwd))
chan = s_conn.channel()

queuename = "UMS-CONTRACT-REMAINING-SUM-RECHARGE"
exchange = "UMS"
routkey = "UMS-CONTRACT-REMAINING-SUM-RECHARGE"
chan.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
chan.queue_declare(queue=queuename, durable=True)
chan.queue_bind(exchange=exchange, queue=queuename, routing_key=routkey)
subMap = {}
subMap["taskId"] = '07cbe62ecbc345cdafd7b52b0f4284b0'
# subMap["checkStatus"] = 2
# subMap["rate"] = 1000
# subMap["disclosureFee"] = 1000
# subMap["checkRemark"] = 'lalal'
# subMap["recheckUserRealName"] = 'ff8080816c949e6a016c9834a4b407a1'
# subMap["disclosureFeeId"] = ''
# subMap["chargeAgainstAmount"] = '200'
# subMap["afterRemainingSum"] = '200'
# body=json.dumps(subMap)
chan.basic_publish(exchange=exchange, routing_key=routkey, body=json.dumps(subMap))
s_conn.close()

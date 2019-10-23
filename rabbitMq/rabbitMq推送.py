import pika
import json

user_pwd = pika.PlainCredentials("umsMQ", '123456')
s_conn = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.5', virtual_host='/', credentials=user_pwd))
chan = s_conn.channel()

queuename = "UMS-SUBMIT-DISCLOSURE-FEE-RECHECK-STATUS"
exchange = "AMQP default"
routkey = "UMS-SUBMIT-DISCLOSURE-FEE-RECHECK-STATUS"
chan.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
chan.queue_declare(queue=queuename, durable=True)
chan.queue_bind(exchange=exchange, queue=queuename, routing_key=routkey)
subMap = {}
subMap["submitCode"] = '15120747620190910845'
subMap["checkStatus"] = 2
subMap["rate"] = 1000
subMap["disclosureFee"] = 1000
subMap["checkRemark"] = 'lalal'
subMap["recheckUserRealName"] = 'ff8080816c949e6a016c9834a4b407a1'
subMap["disclosureFeeId"] = ''
subMap["chargeAgainstAmount"] = '200'
subMap["afterRemainingSum"] = '200'

chan.basic_publish(exchange=exchange, routing_key=routkey, body=json.dumps(subMap))
s_conn.close()

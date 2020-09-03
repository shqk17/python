# coding=gbk
import pika
import json

user_pwd = pika.PlainCredentials('otms', '123456')
s_conn = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.0.5', port='5672', virtual_host='/',
                              credentials=user_pwd))
chan = s_conn.channel()

queuename = "UMS_ADJUST_NEWCLAIMRECORD"
exchange = "UMS"
routkey = "UMS_ADJUST_NEWCLAIMRECORD"
chan.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
chan.queue_declare(queue=queuename, durable=True)
chan.queue_bind(exchange=exchange, queue=queuename,
                routing_key=routkey
                )
subMap = {}
subMap['11'] = '22222'
body = json.dumps(subMap)
chan.basic_publish(exchange=exchange
                   , routing_key=routkey
                   , body=body)
s_conn.close()

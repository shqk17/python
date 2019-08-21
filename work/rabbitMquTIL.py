import pika
import os, sys, time, json


def Main():
    credentials = pika.PlainCredentials("umsMQ", "123456")
    parameters = pika.ConnectionParameters(host="192.168.0.5",
                                           port='5672',
                                           credentials=credentials)
    connection = pika.BlockingConnection(parameters)  # 连接 RabbitMQ

    channel = connection.channel()  # 创建频道

    dataMap = {"contractNum": "Q22222", "operationType": 3, "realName": "陶福兵啊"};
    channel.basic_publish(exchange='', routing_key='UMS-SCHOOL-TEST-OPEN',
                          body=str(json.dumps(dataMap, ensure_ascii=False)))
    #
    # queue = channel.queue_declare(queue='queuetest')  # 声明或创建队列
    #
    # while True:  # 循环向队列中发送信息
    #     message = time.strftime('%H:%M:%S', time.localtime())
    #     channel.basic_publish(exchange='exchangetest',
    #                           routing_key='rkeytest',
    #                           body=message)
    #
    #     print('send message: %s' % message)
    #
    #     while True:
    #         # 检查队列，以重新得到消息计数
    #         queue = channel.queue_declare(queue='queuetest', passive=True)
    #         '''
    #          queue.method.message_count 获取的为 ready 的消息数
    #          截至 2018-03-06（pika 0.11.2）
    #          walker 没找到利用 pika 获取 unack 或者 total 消息数的方法
    #         '''
    #         messageCount = queue.method.message_count
    #         print('messageCount: %d' % messageCount)
    #         if messageCount < 100:
    #             break
    #         connection.sleep(1)

    # 关闭连接
    connection.close()


if __name__ == '__main__':
    Main()

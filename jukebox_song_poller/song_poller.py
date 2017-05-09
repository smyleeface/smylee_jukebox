#!/usr/bin/python
import boto3
import RPi.GPIO as GPIO
import time
import json

QUEUE_NAME_PREFIX = 'jukebox_request_queue.fifo'

sqs_client = boto3.client('sqs')
queue_speed = 1  # number of seconds between polls

# get the queue info
list_of_queues = sqs_client.list_queues(
    QueueNamePrefix=QUEUE_NAME_PREFIX
)
queue_url = list_of_queues['QueueUrls'][0]

# TODO: check the type of message and act accordingly (song, skip, volume, etc.)
# TODO: setup an init boot to know it's on

# https://github.com/skiwithpete/relaypi/blob/master/16port/script16_1.py
GPIO.setmode(GPIO.BCM)
#
# init list with pin numbers
#
pinList = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 21, 20]
#
# # loop through pins and set mode and state to 'low'
#
for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.LOW)


try:
    while True:

        # get messages for the queue url
        messages = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            VisibilityTimeout=30
        )

        # if there were no messages returned stop run
        while 'Messages' in messages:

            # loop through all the messages received
            for message in messages['Messages']:

                message_body_str = message['Body']
                message_body = json.loads(message_body_str)['parameters']['key']
                receipt_handle = message['ReceiptHandle']
                list_of_numbers = [int(d) for d in str(message_body)]


                def relay_zero():
                    print('sending number 0')
                    #     GPIO.output(2, GPIO.LOW)
                    GPIO.setup(2, GPIO.OUT)
                    GPIO.output(2, GPIO.HIGH)
                    time.sleep(1)
                    GPIO.setup(2, GPIO.IN)
                def relay_one():
                    print('sending number 1')
                    #     GPIO.output(3, GPIO.LOW)
                    GPIO.setup(3, GPIO.OUT)
                    GPIO.output(3, GPIO.HIGH)
                    time.sleep(1)
                    GPIO.setup(3, GPIO.IN)
                def relay_two():
                    print('sending number 2')
                    #     GPIO.output(4, GPIO.LOW)
                    GPIO.setup(4, GPIO.OUT)
                    GPIO.output(4, GPIO.HIGH)
                    time.sleep(1)
                    GPIO.setup(4, GPIO.IN)
                def relay_three():
                    print('sending number 3')
                    #     GPIO.output(17, GPIO.LOW)
                    GPIO.setup(17, GPIO.OUT)
                    GPIO.output(17, GPIO.HIGH)
                    time.sleep(1)
                    GPIO.setup(17, GPIO.IN)
                def relay_four():
                    print('sending number 4')
                    #     GPIO.output(27, GPIO.LOW)
                    GPIO.setup(27, GPIO.OUT)
                    GPIO.output(27, GPIO.HIGH)
                    time.sleep(1)
                    GPIO.setup(27, GPIO.IN)
                def relay_five():
                    print('sending number 5')
                    #     GPIO.output(22, GPIO.LOW)
                    GPIO.setup(22, GPIO.OUT)
                    GPIO.output(22, GPIO.HIGH)
                    time.sleep(1)
                    GPIO.setup(22, GPIO.IN)
                def relay_six():
                    print('sending number 6')
                    #     GPIO.output(10, GPIO.LOW)
                    GPIO.setup(10, GPIO.OUT)
                    GPIO.output(10, GPIO.HIGH)
                    time.sleep(1)
                    GPIO.setup(10, GPIO.IN)
                def relay_seven():
                    print('sending number 7')
                    #     GPIO.output(9, GPIO.LOW)
                    GPIO.setup(9, GPIO.OUT)
                    GPIO.output(9, GPIO.HIGH)
                    time.sleep(1)
                    GPIO.setup(9, GPIO.IN)
                def relay_eight():
                    print('sending number 8')
                    #     GPIO.output(11, GPIO.LOW)
                    GPIO.setup(11, GPIO.OUT)
                    GPIO.output(11, GPIO.HIGH)
                    time.sleep(1)
                    GPIO.setup(11, GPIO.IN)
                def relay_nine():
                    print('sending number 9')
                    #     GPIO.output(5, GPIO.LOW)
                    GPIO.setup(5, GPIO.OUT)
                    GPIO.output(5, GPIO.HIGH)
                    time.sleep(1)
                    GPIO.setup(5, GPIO.IN)

                #     # Reset GPIO settings
                #     GPIO.cleanup()

                options = {
                    0: relay_zero,
                    1: relay_one,
                    2: relay_two,
                    3: relay_three,
                    4: relay_four,
                    5: relay_five,
                    6: relay_six,
                    7: relay_seven,
                    8: relay_eight,
                    9: relay_nine
                }

                for individual_number in list_of_numbers:
                    options[individual_number]()

                    # delete message; email processed ok.
                    response = sqs_client.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=receipt_handle
                    )

            # get messages for the queue url
            messages = sqs_client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=10,
                VisibilityTimeout=30
            )

        print('No songs in queue')
        time.sleep(queue_speed)

except KeyboardInterrupt:
    print("  Quit")

    # Reset GPIO settings
    GPIO.cleanup()
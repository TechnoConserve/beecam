'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */


 THIS FILE HAS BEEN MODIFIED FROM IT'S ORIGINAL FORM


 The original source from which this file was derived can be found at:
 https://github.com/aws/aws-iot-device-sdk-python/blob/master/samples/basicPubSub/basicPubSub.py

 Accessed on 4/29/2018
 commit 4b4f626fa58c36fdb9b038a4f8f8d277f30c73f0
'''
import os

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from sense_hat import SenseHat

import argparse
import datetime
import json
import logging
import subprocess
import time
import urllib2

AllowedActions = ['both', 'publish', 'subscribe']
sense = SenseHat()

SENSOR_READ_DELAY = 300  # Delay in seconds


# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")
parser.add_argument("-m", "--mode", action="store", dest="mode", default="both",
                    help="Operation modes: %s" % str(AllowedActions))

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
useWebsocket = args.useWebsocket
clientId = args.clientId
topic = args.topic

if args.mode not in AllowedActions:
    parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
    exit(2)

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, 443)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec


# Custom MQTT message callback
def custom_callback(client, userdata, msg):
    print("Received a new message: ")
    print(msg.payload)
    print("from topic: ")
    print(msg.topic)
    print("--------------\n\n")


def init():
    # Connect and subscribe to AWS IoT
    myAWSIoTMQTTClient.connect()
    if args.mode == 'both' or args.mode == 'subscribe':
        myAWSIoTMQTTClient.subscribe(topic, 1, custom_callback)
    time.sleep(2)


def start_stream():
    print("[*] Starting stream...")

    # Ensure no other instances of the stream are already running
    print("[*] Killing any existing video streams...")
    subprocess.call(['killall', 'raspivid'])
    subprocess.call(['killall', 'ffmpeg'])

    # Start the video stream
    raspivid = subprocess.Popen(['/usr/bin/raspivid', '-o', '-', '-t', '0', '-fps', '25', '-b', '4000000', '-rot',
                                 '270', '-vs'], stdout=subprocess.PIPE)

    # Give the buffer some time to fill
    time.sleep(1)

    # FFMPEG consumes the video stream and grabs an audio stream
    ffmpeg = subprocess.Popen(['/usr/bin/ffmpeg', '-f', 'alsa', '-acodec', 'pcm_u8', '-i', 'plughw:1', '-f', 'h264',
                               '-i', '-', '-vcodec', 'copy', '-acodec', 'aac', '-f', 'flv',
                               'rtmp://a.rtmp.youtube.com/live2/' + os.environ["YOUTUBE_KEY"]],
                              stdin=raspivid.stdout)

    start_time = datetime.datetime.now()
    print("[*] {:%Y-%b-%d %H:%M:%S} - Stream started!".format(start_time))
    return ffmpeg, start_time


def wait_for_internet_connection():
    while True:
        try:
            print("[!] Waiting for internet...")
            response = urllib2.urlopen('http://google.com', timeout=1)
            return
        except urllib2.URLError:
            pass


def main():
    # Script will fail if there is no internet connection
    wait_for_internet_connection()

    # Connect to AWS
    init()

    stream, stream_start = start_stream()

    # Publish to the same topic in a loop forever
    print("[*] Begin logging...")
    while True:
        if args.mode == 'both' or args.mode == 'publish':
            message = {'humidity': sense.humidity,
                       'pressure': sense.pressure,
                       'temperature': sense.temperature,  # in degrees Celsius
                       'deviceID': args.clientId,
                       'stream_began': '{:%Y-%b-%d %H:%M:%S}'.format(stream_start),
                       'time': '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())}
            messageJson = json.dumps(message)
            myAWSIoTMQTTClient.publish(topic, messageJson, 1)
            if args.mode == 'publish':
                print('Published topic %s: %s\n' % (topic, messageJson))

        code = stream.poll()
        if code is not None:
            print("[!] Stream stopped with code", code)
            print("[INFO] Restarting stream...")
            stream, stream_start = start_stream()

        time.sleep(SENSOR_READ_DELAY)


if __name__ == "__main__":
    main()

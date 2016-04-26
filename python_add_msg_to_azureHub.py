#!/usr/bin/env python

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import random, time, sys
import iothub_client
from iothub_client import *

timeout = 241000
minimumPollingTime = 9
receiveContext = 0
avgWindSpeed = 15.0
message_count = 3
received_count = 0
counter = 0
# global counters
receive_callbacks = 0
send_callbacks = 0

# transport protocol
Protocol = IoTHubTransportProvider.HTTP

# String containing Hostname, Device Id & Device Key in the format:
# "HostName=<host_name>;DeviceId=<device_id>;SharedAccessKey=<device_key>"
connectionString = "Enter you details from azure here"

msgTxt = "{\"device\": \"myHTTPDevice\",\"data\": %.2f}"


def receive_message_callback(message, counter):
    global receive_callbacks
    buffer = message.get_bytearray()
    size = len(buffer)
    print ("Received Message [%d]:" % counter)
    print ("    Data: <<<%s>>> & Size=%d" % (buffer[:size].decode('utf-8') , size))
    mapProperties = message.properties()
    keyValuePair = mapProperties.get_internals()
    print ("    Properties: %s" % keyValuePair)
    counter += 1
    receive_callbacks += 1
    print ("    Total calls received: %d" % receive_callbacks)
    return IoTHubMessageDispositionResult.ACCEPTED


def send_confirmation_callback(message, result, userContext):
    global send_callbacks
    print ("Confirmation[%d] received for message with result = %s" % (userContext, result))
    mapProperties = message.properties()
    print ("    message_id: %s" % message.message_id)
    print ("    correlation_id: %s" % message.correlation_id)
    keyValuePair = mapProperties.get_internals()
    print ("    Properties: %s" % keyValuePair)
    send_callbacks += 1
    print ("    Total calls confirmed: %d" % send_callbacks)


def iothub_client_init():
    # prepare iothub client
    iotHubClient = IoTHubClient(connectionString, Protocol)
    if iotHubClient.protocol == IoTHubTransportProvider.HTTP:
        iotHubClient.set_option("timeout", timeout)
        iotHubClient.set_option("MinimumPollingTime", minimumPollingTime)
    iotHubClient.set_message_callback(receive_message_callback, receiveContext)
    return iotHubClient


def print_last_message_time(iotHubClient):
    try:
        lastMessage = iotHubClient.get_last_message_receive_time()
        print ("Last Message: %s" % time.asctime(time.localtime(lastMessage)))
        print ("Actual time : %s" % time.asctime())
    except IoTHubClientError as e:
        if (e.args[0].result == IoTHubClientResult.INDEFINITE_TIME):
            print ("No message received")
        else:
            print (e)


def iothub_client_sample_run():
    global counter
    try:

        iotHubClient = iothub_client_init()
        a = True
        while True:
            # send a few messages every minute
            print ("IoTHubClient sending %d messages" % message_count)
            counter += 3
            for i in range(0, message_count):
                msgTxtFormatted = msgTxt % (i+counter)
                message = IoTHubMessage(msgTxtFormatted)
                # how to assign ids
                message.message_id = "message_%d" % i
                message.correlation_id = "correlation_%d" % i
                propMap = message.properties()
                propText = "PropMsg_%d" % i
                propMap.add_or_update("PropName", propText)
                iotHubClient.send_event_async(
                    message, send_confirmation_callback, i)
                print ("IoTHubClient.send_event_async accepted message [%d] for transmission to IoT Hub." % (i+counter))

            # Wait for Commands or exit
            print ("IoTHubClient waiting for commands, press Ctrl-C to exit")
            time.sleep(1)


    except IoTHubError as e:
        print ("Unexpected error %s from IoTHub" % e)
        return
    except KeyboardInterrupt:
        print ("IoTHubClient sample stopped")

    print_last_message_time(iotHubClient)

print ("\nPython %s\n" % sys.version)
print ("IoT Hub for Python SDK Version: %s\n" % iothub_client.__version__)
print ("Starting the IoT Hub Python sample using protocol %s..." % Protocol)

iothub_client_sample_run()

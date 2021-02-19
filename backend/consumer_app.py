from flask import Flask,request,jsonify,Response
import json
from pykafka.common import OffsetType


from kafka_client import get_kafka_client

app=Flask(__name__)


@app.route("/")
def index():
    return "Welcome to home page"

@app.route("/topic/<topicname>")
def topic_consumer(topicname):
    client=get_kafka_client()
    # cons = client.topics[topicname].get_simple_consumer(consumer_group="consumer_group",
    #                 auto_offset_reset=OffsetType.LATEST,
    #                 reset_offset_on_start=True)
    # print(cons)
    def events():
        for msg in client.topics[topicname].get_simple_consumer(consumer_group="consumer_group",
                    auto_offset_reset=OffsetType.LATEST,
                    reset_offset_on_start=True):
            yield f"{msg.value.decode('utf-8')}"
            # data=consumer.consume()
            # print(data)
    return Response(events(),mimetype="text/event-stream")
    # return "Success"

if __name__=="__main__":
    app.run("0.0.0.0",port=5050,debug=True)
from flask import Flask,request,jsonify,Response,render_template
import json
from pykafka.common import OffsetType


from kafka_client import get_kafka_client

app=Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

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
            #new line character is mandatory for server side events
            yield 'data: %s\n\n' % msg.value.decode('utf-8')
    return Response(events(),mimetype='text/event-stream')

if __name__=="__main__":
    app.run("0.0.0.0",port=5050,debug=True)
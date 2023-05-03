from flask import Flask, render_template
from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter
from rasa.utils.endpoints import EndpointConfig

app = Flask(__name__)

nlu_interpreter = RasaNLUInterpreter("path/to/nlu")
action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
agent = Agent.load("path/to/model", interpreter=nlu_interpreter, action_endpoint=action_endpoint)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

#!/usr/bin/env python
""" HIAS AI Agent.

HIAS AI Agents process data using local AI models and communicate
with HIAS IoT Agents using the MQTT protocol.

MIT License

Copyright (c) 2021 Asociación de Investigacion en Inteligencia Artificial
Para la Leucemia Peter Moss

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files(the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Contributors:
- Adam Milton-Barker - First version - 2021-5-1

"""

import sys

from abc import ABC, abstractmethod

from modules.AbstractAgent import AbstractAgent

from modules.helpers import helpers
from modules.server import server
from modules.model import model


class agent(AbstractAgent):
	""" ALL oneAPI Classifier 2021 HIAS AI Agent

	Represents a HIAS AI Agent that processes data
	using the ALL oneAPI Classifier 2021 model.
	"""

	def train(self):
		""" Creates & trains the model. """

		self.mqtt_start()

		self.model.prepare_data()
		self.model.prepare_network()
		self.model.train()
		self.model.evaluate()

	def set_model(self, mtype):

		self.model = model(self.helpers)

	def load_model(self):
		""" Loads the trained model """

		self.model.load()

	def server(self):
		""" Loads the API server """

		self.mqtt_start()

		self.load_model()
		self.server = server(self.helpers, self.model, self.mqtt)
		self.server.start()

	def inference(self):
		""" Loads model and classifies test data locally """

		self.load_model()
		self.model.test()

	def inference_http(self):
		""" Loads model and classifies test data via HTTP requests """

		self.model.test_http()

	def signal_handler(self, signal, frame):
		self.helpers.logger.info("Disconnecting")
		self.mqtt.disconnect()
		sys.exit(1)


agent = agent()


def main():

	if len(sys.argv) < 2:
		print("You must provide an argument")
		exit()
	elif sys.argv[1] not in agent.helpers.confs["agent"]["params"]:
		print("Mode not supported! server, train or inference")
		exit()

	mode = sys.argv[1]

	if mode == "train":
		agent.set_model("xDNN")
		agent.train()

	elif mode == "classify":
		agent.set_model("xDNN")
		agent.inference()

	elif mode == "server":
		agent.set_model("xDNN")
		agent.server()

	elif mode == "classify_http":
		agent.set_model("xDNN")
		agent.inference_http()


if __name__ == "__main__":
	main()

import pika
import json

class Model:
	def __init__(self, config, instance, messenger, preprocessor):
		assert 'input_attribute' in config
		assert 'output_attribute' in config
		assert messenger is not None
		assert preprocessor is not None
		self.input_attribute = config['input_attribute']
		self.output_attribute = config['output_attribute']
		self.model_fn = getattr(instance, config['method_name'])
		self.messenger = messenger
		self.preprocessor = preprocessor
		
	def run(self):
		self.messenger.start(self.process)

	def process(self, data):
		x = self.preprocessor.preprocess(data)

		# If there was an issue preprocessing (i.e. the JSON attribute was missing from the data), just discard this instance.
		if x == None:
			return

		# TODO: Make this handle more than just JSON
		data[self.output_attribute] = self.model_fn(x)
		if data:
			self.publish(data)

	def publish(self, message):
		self.messenger.publish(message)
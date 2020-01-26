from abc import ABC, abstractmethod

class AttributeParser(ABC):
	def __init__(self):
		pass
		
	def remove_multiple_spaces(self, text):
		while '  ' in text:
			text = text.replace('  ', ' ')
		return text
		
	def replace_bad_delimiters(self, text, bad_delimiters, good_delimiter):
		for bad_delimiter in bad_delimiters:
			text = text.replace(bad_delimiter, good_delimiter)
		return text
		
	def parse(self, text, bad_delimiters, good_delimiter):
		text = self.replace_bad_delimiters(text, bad_delimiters, good_delimiter)
		text = self.remove_multiple_spaces(text)
		items = [self.cast_item(item) for item in text.split(good_delimiter)]
		return items
		
	@abstractmethod
	def cast_item(self, item):
		pass
		
class StringListParser(AttributeParser):
	def __init__(self):
		super().__init__()
		
	def cast_item(self, item):
		return str(item)
		
class NumericalListParser(AttributeParser):
	def __init__(self):
		super().__init__()
		
	def cast_item(self, item):
		return float(item)
				
class MixedListParser(AttributeParser):
	def __init__(self):
		super().__init__()
		
	def cast_item(self, item):
		if item.isalpha():
			return item
		else:
			return float(item)
			
class FunctionParser(NumericalListParser):
	def __init__(self):
		super().__init__()
	
	def	extract_parameters(self, text):
		parameter_text = text[text.find("(")+1:text.find(")")]
		return self.parse(parameter_text, ',', ' ')
		
	def extract_name(self, text):
		return text[:text.find("(")]
		

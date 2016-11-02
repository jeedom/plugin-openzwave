def get_standard_value_type(value_type):
	if value_type == "Int":
		return 'int'
	elif value_type == "Decimal":
		return 'float'
	elif value_type == "Bool":
		return 'bool'
	elif value_type == "Byte":
		return 'int'
	elif value_type == "Short":
		return 'int'
	elif value_type == "Button":
		return 'bool'
	elif value_type == "Raw":
		return 'binary'
	else:
		return value_type

def change_instance(my_value):
	if my_value.instance > 1:
		return my_value.instance - 1
	return 0

def normalize_short_value(value):
	my_result = value
	# noinspection PyBroadException
	try:
		if int(value) < 0:
			my_result = 65536 + int(value)
	except:
		pass
	return my_result

def convert_fahrenheit_celsius(value):
	if value.precision is None or value.precision == 0:
		power = 1
	else:
		power = math.pow(10, value.precision)
	return int(((float(value.data_as_string) - 32) * 5.0 / 9.0) * int(power)) / power
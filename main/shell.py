import basic

while True:
	text = input('basic > ')
	if text.strip() == "": continue
	result, error = basic.run('<stdin>', text)

	if error:
		print(error.as_string())
	elif result:
		if len(result.elements) == 1:
			pass
		else:
			print(repr(result))

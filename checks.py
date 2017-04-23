
# def validateZipCode(before_validate):
	# sample = re.compile(r"\s*(\w\d\s*){3}\s*")

# 	return sample.match(before_validate)

import re

def validateZipCode(before_validate):

	if re.match(r"\b\d{5}\b", before_validate):
		return True
	else:
		return False

def validateEmailAddress(before_validate):

	if not isinstance(before_validate, str):
		raise Exception("Unexpected input type in validateEmailAddress()!", before_validate)

	if re.match(r"\S*[@]\S*[.]\S*", before_validate):
		return True
	else:
		return False

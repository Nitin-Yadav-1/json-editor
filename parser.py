

def toText(val):
	if( type(val) is str ):
		return val

	if( type(val) is list ):
		return ",".join(val)

	return str(val)


def toJSONValue(val):
	if( val == 'True' ):
		return True

	if( val == 'False' ):
		return False

	if( val.isnumeric() ):
		return int(val)

	if( val.count('.') == 1 ):
		temp = val.replace('.','')
		if( temp.isnumeric() ):
			return float(val)

	if( val.count(',') > 0 ):
		valList = val.split(',')
		for idx,s in enumerate(valList):
			valList[idx] = s.strip()
		return valList

	return val
	
	
	


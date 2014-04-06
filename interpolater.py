def getAvgColor(image_array,startX,startY,endX,endY):
	total = []
	for x in range(startX,endX+1):
		for y in range(startY,endY+1):
			if(x < len(image_array) and y < len(image_array[x])):
				total.append(image_array[x][y])
	return sum(total) / len(total)

def interpolate(image_array,X,Y,newX,newY):
	box_width = X // newX
	box_height = Y // newY
	col = 0
	newImageArray = []
	while(len(newImageArray) < newX):
		row = 0
		newRow = []
		while(len(newRow) < newY):
			avgColor = getAvgColor(image_array,col,row,col+box_width,row+box_height)
			row = row + box_height
			newRow.append(avgColor)
		col = col + box_width
		newImageArray.append(newRow)
	return newImageArray

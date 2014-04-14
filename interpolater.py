def getAvgColor(image_array,startX,startY,endX,endY):
	total = []
	for x in range(startX,endX+1):
		for y in range(startY,endY+1):
			if(x < len(image_array) and y < len(image_array[x])):
				rcomp = int(image_array[x][y][1:3],16)
				gcomp = int(image_array[x][y][3:5],16)
				bcomp = int(image_array[x][y][5:7],16)
				total.append([rcomp,gcomp,bcomp])
	return "#%02x%02x%02x" % (sum([c[0] for c in total]) / len(total),\
								sum([c[1] for c in total]) / len(total),\
								sum([c[2] for c in total]) / len(total))

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

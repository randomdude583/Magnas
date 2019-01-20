import json

#PULL DATA FROM JSON FILE
with open('data.txt') as json_file:
	readData = json.load(json_file)

	print("Author: " + readData["author"])
	print("DataSet Size: ")
	print("    Tweets: " + str(len(readData["tweets"])))
	counter = 0
	for tweet in readData["tweets"]:
		for reply in readData["tweets"][tweet]["replies"]:
			counter += 1
	print("    Replies: " + str(counter))
	print("")


	for tweet in readData["tweets"]:
		print("-----------------------------------------------------")
		print(readData["tweets"][tweet]["text"].encode("utf-8"))
		for reply in readData["tweets"][tweet]["replies"]:
			print("    " + reply.encode("utf-8"))
		print("")



# GENERATE TRAINING SET
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("######################################################")
currentMax = None

for tweet in readData["tweets"]:
	if currentMax == None:
		currentMax = readData["tweets"][tweet]
	else:
		if len(readData["tweets"][tweet]["replies"]) > len(currentMax["replies"]):
			currentMax = readData["tweets"][tweet]

print("Biggest set: " + currentMax["text"].encode("utf-8"))
print("    Size: " + str(len(currentMax["replies"])).encode("utf-8"))
print("")

file = open("trainingSet.txt","w") 

for reply in currentMax["replies"]:
	file.write(reply.encode("utf-8") + "\n")
 
file.close() 

print("Training set exported to trainingSet.txt")
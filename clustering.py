
def calculateCentroid (clusterMap, clusterNumber, queries):
	mergedMap = {}
	thisCluster = clusterMap[clusterNumber]
	queryCounter = 0
	for queryNumber in thisCluster:
		queryCounter = queryCounter + 1
		query = queries[queryNumber]
		for word in query:
			if word in mergedMap.keys():
				mergedMap[word] = mergedMap[word] + query[word]
			else:
				mergedMap[word] = query[word]				
	for word in mergedMap:
		mergedMap[word] = mergedMap[word] / queryCounter
	return mergedMap

def updateCentroid (centroidMap, clusterMap, queries):
	for clusterNumber in centroidMap:
		print "		updateCentroid: " + str(clusterNumber)
		centroidMap[clusterNumber] = calculateCentroid(clusterMap, clusterNumber, queries)
	return centroidMap


def updateClusters (centroidMap, queries):
	# centroidMap stores (clusterNumber -> centroid)
	# clusterMap stores (clusterNumber -> list of queries)
	# queries are the maps of queries
	clusterMap = {}
	for centroid in centroidMap:
		clusterMap[centroid] = []

	for queryNumber in queries:
		query = queries[queryNumber]
		if ((queryNumber/1000)*1000 == queryNumber):
			print "		updateClusters: " + str(queryNumber)
		maxDist = -10000 # choosing random small number
		closestCentroid = -1
		for centroid in centroidMap:
			#print "centroid is: " + str(centroid)
			centroidLocation = centroidMap[centroid]
			currentDotProduct = getDotProduct(centroidLocation, query)
			if (currentDotProduct > maxDist):
				maxDist = currentDotProduct
				closestCentroid = centroid
				clusterMap[centroid].append(queryNumber)
	return clusterMap


def getLength (mapQuery):
	sum = 0.0
	for word in mapQuery:
		sum = sum + mapQuery[word]*mapQuery[word]
	return sum**(0.5)


def getDotProduct (mapQuery1, mapQuery2):
	length1 = getLength(mapQuery1)
	length2 = getLength(mapQuery2)
	numerator = 0.0
	for word in mapQuery1:
		if word in mapQuery2.keys():
			#print "match: " + str(mapQuery1[word]) + ", " + str(mapQuery2[word])
			numerator = numerator + mapQuery1[word]*mapQuery2[word]
	if (length1 * length2 < 0.0001):
		return 1.0
	return numerator/(length1 * length2)

def getWordFrequency (query):
	queryArray = query.split()
	wordFrequency = {}
	for word in queryArray:
		if word in wordFrequency.keys():
			wordFrequency[word] = wordFrequency[word] + 1
		else:
			wordFrequency[word] = 1		
	return wordFrequency


if __name__ == '__main__':
	fname = "RawKeywords.txt"
	with open(fname) as f:
		content = f.readlines()

	#generate the inverse query map
	queryMap = {}
	clusterMap = {}
	centroidMap = {}	
	for i in range(0, len(content)):
		queryMap[i] = getWordFrequency(content[i])
	#generate random centroids
	for j in range(0,30):
		# as we need 30 centroids;
		centroidMap[j] = queryMap[j]
		clusterMap[j] = []
		clusterMap[j].append(j)

	for k in range(0, 10):
		# choosing 50,000 randomly
		print "at k = " + str(k)
		clusterMap = updateClusters (centroidMap, queryMap)
		centroidMap = updateCentroid (centroidMap, clusterMap, queryMap)

	f = open('clusters.txt','w')
	for l in range(0, 30):
		f.write('\n cluster map for:  ' + str(l) + '\n')
		for number in clusterMap[l]:
			f.write(str(content[number]))
		f.write('\n----------- \n')
	f.close();


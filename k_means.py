"""
Author: Kenneth Bello

"""
from collections import defaultdict
import random
import math
"""

READ IN DATA

"""
def readData():
	print "Reading data..."
	with open("tag_apps.txt", "r") as data_file:
		for line in data_file:
			fileLine = line.replace('\n', "").split('\t')
			yield {'URL': fileLine[2], "tag": fileLine[3]}

"""
This function creates the sparse vectors for each url's tag frequencies.
"""
def sparseVectors():
	print "Starting sparseVectors..."
	vectors = defaultdict(lambda: defaultdict(int))
	counter = defaultdict(int)
	for data in readData():
		vectors[data['URL']][data['tag']] += 1	
		counter[data['URL']]+= 1
	
	count = 0
	urlDict = {}
	for (k,v) in counter.iteritems():
		if v >= 700:
			urlDict[k] = vectors[k]
	#print len(urlDict)  235 urls
	return urlDict
"""
This function created the sparse vectors for each tag's url frequencies. 
I also threw out all tags that have been used less than a total of 3000 times 
of all URLs.
"""
def tagSparseVectors():
	print "Starting tagSparseVectors..."
	vectors = defaultdict(lambda: defaultdict(int))
	counter = defaultdict(int)
	for data in readData():
		vectors[data['tag']][data['URL']] += 1	
		counter[data['tag']]+= 1
	
	count = 0
	tagDict = {}
	for (k,v) in counter.iteritems():
		if v >= 3000:
			tagDict[k] = vectors[k]
	return tagDict

"""
Takes in a number that sets the amount of clusters, takes in either tagSparseVectors 
or sparseVectors, and True or False in the event that you want to print out the sum of 
the similarities.

I used the same kMeans function for the tag clusters and url clusters because I noticed 
that clustering by tags is the same as URLs, which means that I could just simply flip 
the way I sparse for each one. So for example, for sparseVectors I found the frequency of
each tag for each url, but in tagSparseVectors I found the frequency of each url for each tag.
"""
def kMeans(num, vectors, TF):
	spVex = vectors
	clusters = defaultdict(lambda: defaultdict(int))
	for url in spVex:
		clusters[random.randint(0,num-1)][url] = spVex[url]

	for i in range(10):
		clust_tag_freq = defaultdict(lambda: defaultdict(float))
		for clust_num in clusters:
			clust = clusters[clust_num]
			for url in clust:
				for tag in clust[url]:
					clust_tag_freq[clust_num][tag] += clust[url][tag]
		
		centroids = defaultdict(lambda: defaultdict(float))
		for clust_num in clusters:			
			clust = clusters[clust_num]
			for url in clust:
				for tag in clust[url]:					
					centroids[clust_num][tag] += (clust_tag_freq[clust_num][tag]/len(clust))

		sub_cluster = {}

		for clust_num in clusters:
			clusts = clusters[clust_num]
			for url in clusts:
				close_cluster = 0 
				similarity = 0.0
				similarity_sum = 0.0
				if TF == True:
					print '============================================================='
					print url
					print '============================================================='
				for centroid_num in centroids:
					cent = centroids[centroid_num]
					numerator = 0.0
					a_square = 0.0
					b_square = 0.0
					for tag in clusts[url]:
						a = cent[tag]
						b = clusts[url][tag]
						numerator += (a * b)
						a_square += (a * a)
						b_square += (b * b)
					cos_sim = numerator / (math.sqrt(b_square) * math.sqrt(a_square))
					if cos_sim > similarity:
						close_cluster = centroid_num 
						similarity = cos_sim
					similarity_sum += cos_sim
					if TF == True:
						print "Sum of similarities: ", similarity_sum, "\n" 
				if close_cluster not in sub_cluster:
					sub_cluster[close_cluster] = {}
				sub_cluster[close_cluster][url] = clusts[url]
		clusters = sub_cluster
		print "=======================================================================",i+1,"===========================================================================================\n"
		for (k,v) in clusters.iteritems():
			print "Cluster",k+1,":\n",v.keys()



def main():
	print "=================================================== Cluster URLs ==================================================================\n"
	kMeans(10, sparseVectors(), True)
	print
	print "=================================================== Cluster Tags ==================================================================\n"
	kMeans(10, tagSparseVectors(), False)

main()
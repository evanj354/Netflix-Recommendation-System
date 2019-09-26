import math
import sys
from scipy import spatial
import statistics
import numpy as np
from operator import itemgetter

inputs = ['test5.txt', 'test10.txt', 'test20.txt']
outputs = ['result5.txt', 'result10.txt', 'result20.txt']

train = open('train.txt','r')



numRatings = [1]*1000
test_users = []
train_users = []

mean_trains_iuf = []
mean_trains = []
mean_trains_item = []
# class Users:
# 	def __init__(self, id, movie, rating):
# 		self.movies = []
# 		self.id = id
# 		self.movies.append((movie, rating)) 

# class Train_Users:
# 	def __init__(self, id, rating):
# 		self.id = id
# 		self.movies = rating

def write(text):
	output.write(str(text[0]) + " " + str(text[1]) + " " + str(text[2]) + "\n")

def read_train():
	for text in train.readlines():
		sum = 0
		count = 0
		mean = 0.0

		ratings = text.strip().split("\t")
		ratings = list(map(int, ratings))
		train_users.append(ratings)

		
		for id in range(len(ratings)):
			if(ratings[id] != 0):
				numRatings[id] += 1 

		mean_trains_item.append(statistics.mean(ratings))
		# for rating in ratings:  #calculate mean of train
		# 	if(rating != 0):
		# 		sum += rating
		# 		count += 1
		# 		# numRatings[id] += 1 
		# 		# id+=1
		# mean = sum/count
		# mean_trains.append(mean)


		
		
	# calculate mean
	for user in range(len(train_users)):
		sum_base = 0.0
		mean_base = 0.0

		sum_iuf = 0.0
		mean_iuf = 0.0

		count = 0.0

		for movieID in range(len(train_users[user])):
			if(train_users[user][movieID] != 0):
				iuf_value = math.log(200/numRatings[movieID])
				sum_iuf += iuf_value*train_users[user][movieID]
				sum_base += train_users[user][movieID]
				count += 1.0

		mean_iuf = sum_iuf/count
		mean_base = sum_base/count
		mean_trains_iuf.append(mean_iuf)
		mean_trains.append(mean_base)


	# print(numRatings)
	# print(mean_trains)


	# print(mean_trains_iuf)
	# print("\n236: " + str(train_users[0][236]))
	

def compute_euclidean(vector_train, vector_test):
	return math.sqrt(sum([(a - b) ** 2 for a, b in zip(vector_train, vector_test)]))

def num_ratings(movieID):
	count = 0
	for each in train_users:
		if(each.movies[movieID-1] != 0):
			count+=1
	return count

def iuf(vector, movieIDs):
	new_vector = []
	for rating, ID in zip(vector, movieIDs):
		num_ratings = numRatings[ID-1]
		iuf_value = math.log(200/num_ratings)
		new_vector.append(rating*iuf_value)
	return new_vector

def compute_pearson(train_vector, test_vector, mean_train, mean_test, movieIDs):
	iuf_train = iuf(train_vector, movieIDs)
	# iuf_test = iuf(test_vector, movieIDs)

	train_vector[:] = [x - mean_train for x in iuf_train]
	test_vector[:] = [y - mean_test for y in test_vector]

	a = 1.0 - (spatial.distance.cosine(train_vector, test_vector))

	return a



def compute_cos(train_vector, test_vector):
	# train_vector[:] = [x - statistics.mean(train_vector) for x in train_vector]
	# test_vector[:] = [x - statistics.mean(test_vector) for x in test_vector]
	# for train, ratings in zip(vector_train, numRatings):
	#     if(ratings == 0):
	#         iuf = 1
	#     else:
	#         iuf = math.log(200/ratings)

	#     new_train.append(train * iuf)
	# print("train: " + str(train_vector) + "test: " + str(test_vector))
	a = 0.0
	a = 1.0 - (spatial.distance.cosine(train_vector, test_vector)) #computes the distance
	# print(a)
	# print(a)
	return a
	# num = 0
	# den = len(vector_train) * len(vector_test)
	# for train, test in zip(vector_train, vector_test):
	#   num += train*test
	# return num/den

def get_column(movieID):
	new_vector = []
	for userID in range(200):
		new_vector.append(train_users[userID][movieID])
	return new_vector

def compute_adj_cosine(movieTrainID, movieToFind, rating):
	train_vector = get_column(movieTrainID)
	test_vector = get_column(movieToFind)

	ntrain_vector = []
	ntest_vector = []

	for userID in range(len(train_vector)):
		if(train_vector[userID] != 0 and test_vector[userID] != 0):
			adj_train = train_vector[userID] - mean_trains_item[userID]
			adj_test = test_vector[userID] - mean_trains_item[userID]
			ntrain_vector.append(adj_train)
			ntest_vector.append(adj_test)

	if(len(ntrain_vector) == 0):
		return "0"
	else:
		# user_mean = mean_trains[movieTrainID]
		# test_mean = statistics.mean(ntest_vector)
		
		# ntrain_vector[:] = [x - user_mean for x in ntrain_vector]
		# ntest_vector[:] = [y - user_mean for y in ntest_vector]


		
		# train_vector[:] = [x - mean_train for x in iuf_train]
		# test_vector[:] = [y - mean_test for y in test_vector]
		
		a = 1.0 - (spatial.distance.cosine(ntrain_vector, ntest_vector))

		return (a, movieTrainID, rating)

	


def item_based_vectors(user, movieToFind):
	scores = []
	train_vector = []
	test_vector = []
	movieIDs = []

	
	
	
	for movieID, rating in user:
		score = compute_adj_cosine(movieID-1, movieToFind-1, rating)
		if(score != "0" and math.isnan(score[0]) != True):
			scores.append(score)
				

	
	return scores

def build_vectors(user, movieToFind):
	scores = []
	train_vector = []
	test_vector = []
	movieIDs = []

	# print(user)
	for userID in range(len(train_users)):	
		if(train_users[userID][movieToFind-1] != 0):
			train_rating = train_users[userID][movieToFind-1] 
			
			count_test = 0.0
			sum_test = 0.0
			mean_test = 0.0
			for movieID, rating in user:
				sum_test += rating
				count_test += 1
				if(train_users[userID][movieID-1] != 0):
					movieIDs.append(movieID)
					train_vector.append(train_users[userID][movieID-1])
					test_vector.append(rating)

			mean_test = sum_test/count_test

			if(len(train_vector) == 0):
				score = 0.0
			else:
				score = compute_pearson(train_vector, test_vector, mean_trains_iuf[userID], mean_test, movieIDs)
			if(math.isnan(score)):
				scores.append((userID+1, 0.0, train_rating, mean_trains[userID], mean_test))
			else:
				scores.append((userID+1, score, train_rating, mean_trains[userID], mean_test))
			# scores.append(score)
		
	# print(score)
	return scores


def sort_abs(a):
	return abs(a[1])

def get_k(movieToFind, scores):    #return a list of the closest ids
	# print(str(scores[0:5]) + "\n")
	

	scores = sorted(scores, reverse = True, key = sort_abs)
	# print(str(scores[0:5]) + "\n")
	top5 = []
	for each in scores:
		userID = each[0]
		weight = each[1]
		rating = each[2]
		mean_train = each[3]
		mean_test = each[4]
		top5.append( (weight, userID, rating, mean_train, mean_test) )
		if(len(top5) >= 5):
			break
	# print(top5)
	return top5
	# print(top5)

def getWeight(k_nearest, movieToFind):
	sum_ = 0.0
	bot = 0.0
	new_weight = []
	mean = 0.0
	for weight, userID, rating, mean_B, mean_A in k_nearest:
		# print("\nmeanA " + str(mean_A))
		mean = mean_A
		# if(weight < 1.0 and weight > -1.0):
		# weight = weight * math.pow(weight, 1.5)			
		sum_ += (weight**2)*(int(rating) - mean_B)
		bot += abs(weight)
	if(bot == 0.0):
		return 0.0
	return mean + (sum_/bot)


def sort_absItem(a):
	return abs(a[0])

def get_kItem(movieToFind, scores):    #return a list of the closest ids
	# print(str(scores[0:5]) + "\n")
	scores = sorted(scores, reverse = True, key = sort_absItem)
	# print(str(scores[0:5]) + "\n")
	top5 = []
	for each in scores:
		score = each[0]
		movieID = each[1]
		rating = each[2]
		# train_mean = each[3]
		# test_mean = each[4]
		top5.append( (score, movieID, rating) )
		if(len(top5) >= 15):
			break
	# print(top5)
	return top5
	# print(top5)

def getWeightItem(k_nearest, movieToFind):
	sum = 0.0
	bot = 0.0
	new_weight = []
	mean = 0.0
	for weight, movieID, rating in k_nearest:
		# print("\nmeanA " + str(mean_A))
		# if(weight < 1.0 and weight > -1.0):
		# weight = weight * math.pow(weight, 1.5)			
		sum += (weight**2)*(int(rating))
		bot += abs(weight)
	if(bot == 0.0):
		return 0.0
	return (sum/bot)

def read_test():
	prev_userID = 0
	user = []
	for text in test.readlines():
		# text = text.strip().split('\n')
		# line = text
		text = text.strip().split(" ")
		text = list(map(int, text))     #change text to list of ints
		userID = text[0];
		if(userID == prev_userID):
			if(text[2] != 0):   #users rating
				pair = (text[1], text[2])  #movie id, rating
				user.append(pair)
			else:   #movie hasn't been rated
				movieToFind = text[1]  #movie id of which rating to guess
				scores = []

				scores = build_vectors(user, movieToFind)
				scores_item = item_based_vectors(user, movieToFind)



					# scores.append( (score, train.id) )
				# print(str(scores) + "\n\n\n")
				

				k_nearest = get_k(movieToFind, scores) 
				k_nearest_item = get_kItem(movieToFind, scores_item)
				# print("KNEAREST \n " + str(k_nearest) + "\n\n")

				new_rating = getWeight(k_nearest, movieToFind)
				new_rating_item = getWeightItem(k_nearest_item, movieToFind)
				# print("NEW WEIGHTS \n " + str(new_weights) + "\n\n")
				# print(str(new_rating) + " " + str(new_rating_item))

				if(math.isnan(new_rating)): new_rating = 3
				adjusted_rating = (new_rating+new_rating_item)/2.0
				new_rating = int(round(adjusted_rating))
				if(new_rating == 0):
				    new_rating = 1

				if(new_rating > 5):
					new_rating = 5
				elif(new_rating < 0):
					new_rating = 1

				text[2] = new_rating
				write(text)  
	
		elif(userID != prev_userID):
			
			user = []
			pair = (text[1], text[2])
			user.append(pair)
			# print(user.id + " " + str(user.movies) + "\n")
		
			prev_userID = userID
			
def print_train():
	# for i in range(200):
		# for j in range(1000):
	# for i in range(10):
	print(len(train_users[1]))
# print(total_users[1].id)
# for user in total_users:
#   print(user.id + " " + str(len(user.movies)))
for inp, out in zip(inputs, outputs):

	test = open(inp, 'r')
	output = open(out, 'w')
	read_train()
	# print_train()
	# item_based()
	read_test()
# print(train_users[0].movies)

train.close()
output.close()
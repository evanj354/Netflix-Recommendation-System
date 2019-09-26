import math
import sys
from scipy import spatial
import statistics
import numpy as np
from operator import itemgetter

inputs = ['test5.txt', 'test10.txt', 'test20.txt']
outputs = ['item_result5.txt', 'item_result10.txt', 'item_result20.txt']

train = open('train.txt','r')



numRatings = [1]*1000
test_users = []
train_users = []

mean_trains_iuf = []
mean_trains = []
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

		mean_trains.append(statistics.mean(ratings))
		
	
	

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
			adj_train = train_vector[userID] - mean_trains[userID]
			adj_test = test_vector[userID] - mean_trains[userID]
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

	


def build_vectors(user, movieToFind):
	scores = []
	train_vector = []
	test_vector = []
	movieIDs = []

	
	
	
	for movieID, rating in user:
		score = compute_adj_cosine(movieID-1, movieToFind-1, rating)
		if(score != "0" and math.isnan(score[0]) != True):
			scores.append(score)
				

	# mean_test = sum_test/count_test

	# if(len(train_vector) == 0):
	# 	score = 0.0
	# else:
	# 	score = compute_pearson(train_vector, test_vector, mean_trains_iuf[userID], mean_test, movieIDs)
	# if(math.isnan(score)):
	# 	scores.append((userID+1, 0.0, train_rating, mean_trains[userID], mean_test))
	# else:
	# 	scores.append((userID+1, score, train_rating, mean_trains[userID], mean_test))
	# scores.append(score)

	# print(score)
	return scores

def sort_abs(a):
	return abs(a[0])

def get_k(movieToFind, scores):    #return a list of the closest ids
	# print(str(scores[0:5]) + "\n")
	scores = sorted(scores, reverse = True, key = sort_abs)
	# print(str(scores[0:5]) + "\n")
	top5 = []
	for each in scores:
		score = each[0]
		movieID = each[1]
		rating = each[2]
		# train_mean = each[3]
		# test_mean = each[4]
		top5.append( (score, movieID, rating) )
		if(len(top5) >= 5):
			break
	# print(top5)
	return top5
	# print(top5)

def getWeight(k_nearest, movieToFind):
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

					# scores.append( (score, train.id) )
				# print(str(scores) + "\n\n\n")
				# print("done scores")
				
				k_nearest = get_k(movieToFind, scores) 
				# print("KNEAREST \n " + str(k_nearest) + "\n\n")

				new_rating = getWeight(k_nearest, movieToFind)
				# print("NEW WEIGHTS \n " + str(new_weights) + "\n\n")
				# print(new_rating)

				# if(math.isnan(new_rating)): new_rating = 3
				new_rating = int(round(new_rating))
				if(new_rating == 0):
				    new_rating = 3

				if(new_rating > 5):
					new_rating = 5
				elif(new_rating < 0):
					new_rating = 1

				text[2] = new_rating
				write(text)  
	
		elif(userID != prev_userID):
			# print("NEW USER")
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
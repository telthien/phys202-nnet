from sklearn.datasets import load_digits
import numpy as np
import random, math

# The following functions split data into randomized subsets

def split_set(dataset, point):
    """Takes a raw data set, and splits it at a specified point, appending the solution in a tuple in the process.
    
    Data will be split at the same point consistently, but each set will be shuffled."""
    training_temp = list(zip(dataset.images[:point], dataset.target[:point]))
    test_temp = list(zip(dataset.images[point:], dataset.target[point:]))
    random.shuffle(training_temp)
    random.shuffle(test_temp)
    training_set, training_sols = zip(*training_temp)
    test_set, test_sols = zip(*test_temp)
    return list(zip(training_set, training_sols)), list(zip(test_set, test_sols))

def split_to_batch(trainset, size):
    """Takes a data set and splits it into subsets of a given size."""
    return [trainset[n*size:(n+1)*size] for n in range(0, math.floor(len(trainset)/size))]

def conv_to_col(vec, scale=1):
    """Converts a 2D matrix (typically an image) into a 1D column vector"""
    vec = np.array(vec)
    assert(len(vec.shape) == 2)
    return np.rot90([vec.reshape((vec.shape[0] * vec.shape[1]))])/scale

def rotate_list(vec):
    """Rotates a list into a numpy column vector"""
    return np.rot90([np.array(vec).reshape((len(vec)))])

def create_tgt_vec(pos, length=10):
    """Creates a target column vector of the form [0, 0, ..., 0, 1, 0, ... 0]T 
    
    length -- the length of the column vector to be created"""
    tmp = np.zeros(length)
    tmp[pos] = 1
    return np.rot90([tmp])

def read_outp_vec(vec):
    """Reads a column vector for the index of its max"""
    maxInd = 0;
    for i in range(1, len(vec)+1):
        if vec[-i][0] > vec[-maxInd][0]: maxInd = i
    if maxInd == 0: maxInd = len(vec)
    return maxInd - 1

def load_data(split_point, batch_size, test_size = None):
    """Loads test data into working memory.
    
    split_point -- splits the data into a training and a test set
    batch_size -- splits the training set into smaller batches of batch_size
    test_size -- caps the test set size (primarily for speed)"""
    digits = load_digits()
    train_set, test_set = split_set(digits, split_point)
    train_set = split_to_batch(train_set, batch_size)
    if not(test_size == None): test_set = test_set[0:test_size]
    return train_set, test_set

### ASSERT TESTING ###

# Batch creation testing
digits = load_digits()
train_set1, test_set1 = split_set(digits, 10)
train_set2, test_set2 = split_set(digits, 10)

assert(len(train_set1) == 10)
assert(len(test_set1) == len(digits.images) - len(train_set1))
assert(type(test_set1[0]) == tuple)
assert(not(np.allclose(test_set1[0][0], test_set2[0][0], 0)))

batch_1 = split_to_batch(train_set1, 2)
batch_2 = split_to_batch(train_set2, 2)
assert(len(batch_1) == 5)
assert(len(batch_1[0]) == 2)
assert(len(batch_1[0][0]) == 2)
assert(batch_1[0][0][0].shape == (8, 8))

image_1 = batch_1[0][0][0]
assert(np.allclose(conv_to_col([[1, 2], [3, 4]]), [[4],[3],[2],[1]], 0))
assert(conv_to_col(image_1).shape == (64, 1))

assert(len(load_data(400, 5)[0]) == 80)
assert(len(load_data(400, 5, 400)[1]) == 400)

# Output reads correctly
assert(read_outp_vec(create_tgt_vec(5)) == 5)
assert(read_outp_vec(create_tgt_vec(0)) == 0)
assert(read_outp_vec(create_tgt_vec(9)) == 9)
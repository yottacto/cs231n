import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train = X.shape[0]
  num_classes = W.shape[1]
  scores = X @ W
  scores -= np.max(scores, axis=1)[:, np.newaxis]
  for i in range(num_train):
    loss -= scores[i, y[i]]
    scores[i, :] = np.exp(scores[i, :])
    s = np.sum(scores[i, :])
    loss += np.log(s)
    scores[i, :] /= s
    scores[i, y[i]] -= 1
    for j in range(num_classes):
      dW[:, j] += scores[i, j] * X[i, :]
    
  loss /= num_train
  loss += reg * np.sum(W * W)
  dW /= num_train
  dW += 2 * reg * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train, dim = X.shape
  scores = X @ W
  scores -= np.max(scores, axis=1)[:, np.newaxis]
  loss -= np.sum(scores[np.arange(num_train), y])
  scores = np.exp(scores)
  # TAKEAWAY: save the intermediate results make it much slower
  # s = np.sum(scores, axis=1)
  loss += np.sum(np.log(np.sum(scores, axis=1)))
  loss /= num_train
  loss += reg * np.sum(W * W)
  # TAKEAWAY: too inefficient to use np.add.at
  # np.add.at(dW, (np.arange(dim)[:, np.newaxis], y), -X[np.arange(num_train), :].T)
  scores /= np.sum(scores, axis=1)[:, np.newaxis]
  scores[np.arange(num_train), y] -= 1
  dW = (scores.T @ X).T
  dW /= num_train
  dW += 2 * reg * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


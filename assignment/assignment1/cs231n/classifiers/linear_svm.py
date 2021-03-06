import numpy as np
from random import shuffle

def svm_loss_naive(W, X, y, reg):
  """
  Structured SVM loss function, naive implementation (with loops).

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
  dW = np.zeros(W.shape) # initialize the gradient as zero

  # compute the loss and the gradient
  num_classes = W.shape[1]
  num_train = X.shape[0]
  loss = 0.0
  for i in range(num_train):    
    scores = X[i].dot(W)
    dscores = np.zeros_like(scores)
    correct_class_score = scores[y[i]]
    
    for j in range(num_classes):
      if j == y[i]:
        continue
      margin = scores[j] - correct_class_score + 1 # note delta = 1

      dWi = X[i]
      if margin > 0:
        loss += margin
        dscores[j] = 1
        dscores[y[i]] -= 1
    dWi = X[i][:,None].dot(dscores[None,:])
    dW += dWi

  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train
  #print(dW)
  dW /= num_train

  # Add regularization to the loss.
  loss += reg * np.sum(W * W)
  dW += reg * 2*W

  #############################################################################
  # TODO:                                                                     #
  # Compute the gradient of the loss function and store it dW.                #
  # Rather that first computing the loss and then computing the derivative,   #
  # it may be simpler to compute the derivative at the same time that the     #
  # loss is being computed. As a result you may need to modify some of the    #
  # code above to compute the gradient.                                       #
  #############################################################################

  return loss, dW


def svm_loss_vectorized(W, X, y, reg):
  """
  Structured SVM loss function, vectorized implementation.

  Inputs and outputs are the same as svm_loss_naive.
  """
  loss = 0.0
  dW = np.zeros(W.shape) # initialize the gradient as zero

  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the structured SVM loss, storing the    #
  # result in loss.                                                           #
  #############################################################################
  scores = np.dot(X,W)
  margin = (scores-(scores[np.arange(len(scores)), y][:,None]))+1
  margin_clip = np.clip(margin, 0, margin.max())
  margin_sum = margin_clip.sum(1)-1
  loss = margin_sum.mean()
  loss += reg * np.sum(W * W)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################


  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the gradient for the structured SVM     #
  # loss, storing the result in dW.                                           #
  #                                                                           #
  # Hint: Instead of computing the gradient from scratch, it may be easier    #
  # to reuse some of the intermediate values that you used to compute the     #
  # loss.                                                                     #
  #############################################################################
  dloss = 1

  dmargin_clip = np.ones_like(margin_clip)
  dmargin = np.where(margin<0, 0, 1)
  dscores1 = np.ones_like(scores)
  dscores2 = np.full_like(scores, -1)
  dscores2[np.arange(len(scores)), y] = 0
  dW_local = X

  dloss_margin_sum = np.full_like(margin_sum,1/len(margin_sum))
  dloss_margin_clip = dloss_margin_sum[:,None] * dmargin_clip
  dloss_margin = dloss_margin_clip * dmargin
  dloss_scores1 = dloss_margin * dscores1
  dloss_scores2 = dloss_margin * dscores2
  dloss_scores1[np.arange(len(scores)), y] = dloss_scores2.sum(1)
  dW = dW_local.T.dot(dloss_scores1)
  #dW /= W.shape[0]
  dW += reg * 2 * W
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return loss, dW


def svm_loss_pytorch(W, X, y, reg):
  """
  Structured SVM loss function, pytorch implementation.

  Inputs and outputs are the same as svm_loss_naive.
  """
  import torch
  
  W = torch.from_numpy(W)
  W.requires_grad = True
  X = torch.from_numpy(X)
  y = torch.from_numpy(y).long()
  
  

  # compute the loss and the gradient
  num_classes = W.shape[1]
  num_train = X.shape[0]
  loss = torch.tensor(0.0, dtype=torch.float64)
  for i in range(num_train):    
    scores = X[i][None,:].mm(W)
    correct_class_score = scores[0,y[i]]
    for j in range(num_classes):
      if j == y[i].item():
        continue
      margin = scores[0,j] - correct_class_score + 1 # note delta = 1
      if margin > 0:
        loss += margin
  
  loss /= num_train   
  loss += reg * torch.sum(W**2)
  loss.backward()
  loss = loss.detach().numpy()
  
  dW = W.grad.detach().numpy()
  #dW += reg * 2*(W.detach().numpy())


  return loss, dW
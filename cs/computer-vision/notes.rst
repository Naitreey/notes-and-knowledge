General
=======
- 交叉学科. physics, math, neuroscience, computer science.

- ImageNet
  图形验证码都干嘛去了?? 叫你们拿去做机器视觉了...

- WordNet

- topics:
  image classification
  object detection
  image captioning

- ConvNet is very important for image related problems.

image classification
====================

- a core task

- assume given set of discrete labels, given an image, output one of the labels.

problem
-------
semantic gap

challenges
----------
  
- viewpoint variation

- illumination

- deformation

- background clutter

- intraclass variation

solution
--------
data-driven approach

1. collect a dataset of images and labels

2. use ML to train a classifier

3. evaluate the classifier on new images

dataset
-------
CIFAR10

classifier
----------

K-nearest neighbor
~~~~~~~~~~~~~~~~~~

- distance metric:
  
  * L1 (Manhattan) distance. ``d_1(I_1,I_2) = \sum_p \abs{I_1^p-I_2^p}``

    square is a circle by definition: points with the same distance to origin.

    L1 distance of a fixed point and origin depends on orientation of
    coordinate system.

    如果 vector 的每一项有固定的意义, 可能使用 L1 更好.

  * L2 (Euclidean) distance. ``d_2(I_1,I_2) = \sqrt{\sum_p(I_1^p-I_2^p)^2}``

    circle is a circle.

    L2 distance is independent of orientation of coordinates.

- algorithm:

  1. train: do nothing, just memorize dataset

  2. predict:
         
     opt1: find min of L1 distance (nearest neighbor).

     opt2: take majority vote from K closest points (K-nearest neighbor).

- performance:

  1. train: O(1)

  2. predict: O(N)

- decision boundary

- remarks.

  very general. useful for many kinds of problems. only needs to define
  a proper way to compute distance.

  first thing to try when solving a new problem.

- choices of K and distance metric.

  very problem-dependent. must try them all out and see what works best.

- setting hyperparameters.
 
  choices about the algorithm that we set rather than learn.

  1. BAD: choose hyperparameters that work best on the data.
     why: model always works perfectly on data itself being trained.

  2. BAD: split data to train & test. choose hyperparams that perform best on test.
     why: no data to test the model's performance on fresh untouched data.

  3. better: split data to train & val & test. choose hyperparams that perform
     best on val and evaluate it *only once* on test. (for each model? what if
     test failed?)

  4. cross-validation: split data into folds, try each fold as validation and
     average the results. Useful for small datasets, not very often in deep learning.

- never used on images in practice.

  * very slow at test time.

  * distance metrics on pixels are not informative.

  * curse of dimensionality. training data must be densely covered in space, otherwise
    the result may be far off.

linear classifier
~~~~~~~~~~~~~~~~~

- the most fundamental building blocks for neutral network.

- parametric model

  ``f(x, W)`` -> array of scores for each class
 
  ``x`` input, ``W`` parameters or weights.

  ``x`` 是图片的所有像素点的值构成的一个 vector.

  parametric model:
  in training time, summarize the knowledge of training data into parameters ``W``;
  then in test time, we no longer need training data, just input ``x`` and ``W``,
  therefore very fast.

  finding correct ``f`` is the important thing of deep learning. It corresponds
  to different network architecture.

- for linear classifier, we just define ``f(x,W) = Wx + b``.

  从而, ``W`` 是一个 ``class`` 行 ``pixel-number`` 列的矩阵.

  where ``b`` is constant bias term, which does not interact with training data,
  just some data independent preferences of one class over another.

- think linear classifier like template matching.

  each row of ``W`` is like the template for one of the classes. the inner product
  somehow gives the similarity between image and class.
  
  Only one template is allowed for each class. So it's an averaged result of
  possibly different appearances for different training examples in one class.
  So different possible shapes superposed and looks blury and weird.

  other classifiers may not have this one-template-only restriction. So may looks
  better.

- 如果把像素值矢量 ``x`` 看作是一个 N 维座标平面上的点, 则 ``W`` 的每一行 (即一个 class
  template 图像) 是斜率. ``f(x,W) = Wx+b`` 定义了一个 N+1 维平面. 这个面与 N 维座标
  平面的交线就是该类的 decision boundary. 也就是说在这条线的一边是这类的图像, 另一边不是.
  
- hard cases
  
  由于这是线性的区分, 如果图像在这个平面上的分布无法用一条或多条线性的 decision boundary
  来划分的话, 就使用 linear classifier 就会失败.

  例如,
  
  * 一个分类有多个独立模式的情况, 在上述高维平面中以多个独立的 point cluster 形式出现.

  * 一个分类在高维平面中以环状出现.

- 如何选择 W. 即如何选择各个斜率最终让所有的训练数据点的分数 ``f(x,W)`` 合理,
  decision boundary ``Wx+b=0`` 位置合理.

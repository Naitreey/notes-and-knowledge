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
     best on val and evaluate it *only once* on test. (Q: for each model? what if
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

- a basic example of parametric classifiers.

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

- 如果把像素值矢量 ``x`` 看作是一个 N 维座标平面上的点 (每个像素点的强度是都是一个
  座标轴), 则 ``W`` 的每一行 (即一个 class template 图像) 是斜率.
  ``f(x,W) = Wx+b`` 定义了一个 N+1 维平面. 这个面与 N 维座标 平面的交线就是该类的
  decision boundary. 也就是说在这条线的一边是这类的图像, 另一边不是.

  这也是对 linear classification 的线性特性的一种理解. 即 ``Wx+b=0`` 的 decision boundary
  在 N 维座标面上是一条直线.
  
- hard cases
  
  由于这是线性的区分, 如果图像在这个平面上的分布无法用一条或多条线性的 decision boundary
  来划分的话, 就使用 linear classifier 就会失败.

  例如,
  
  * 一个分类有多个独立模式的情况, 在上述高维平面中以多个独立的 point cluster 形式出现.

  * 一个分类在高维平面中以环状出现.

- loss function definition.
 
  解决: 如何通过 training data 得到合适的 W. 即如何选择各个斜率最终让所有的训练数据点的
  分布 ``f(x,W)`` 合理, decision boundary ``Wx+b=0`` 位置合理.

  这需要量化 badness of different choices of W. 即一个函数, 它输入 W, 根据 W 计算对
  各个训练样本的分数, 然后得出 badness value. 这就是 loss function 的概念.

  寻找 loss function 的极小值点, 即得到了最合适的 W 参数值.

  definition:

  Given a dataset of examples ``{(x_i, y_i)}_{i=1}^N``, where ``x_i`` is image and
  ``y_i`` is integer label, loss over the dataset is a sum of loss over examples:
  ``L = \frac{1}{N}\sum_i L_i (f(x_i, W), y_i)``. This is a very general definition.

  在实际中, 选择 ``L_i`` 即 loss function 的形式是很重要的. 它体现作者对不同 score
  的 badness 情况的糟糕程度判断. 例如, hinge loss 是线性的, score 差别一点造成的
  badness 差别并不那么大; 若选择 square loss, 一点 score 差别造成的 badness
  可能很大.

  训练时经常选择 random W 作为初始值.

- multiclass SVM loss. (Q: SVM?)

  Given ``(x_i, y_i)``, let ``s = f(x_i, W)``, we define the SVM loss:
  ``L_i= \piecewise{0, s_j - s_{y_i} + 1} = \sum_{\ne y_i}\max(0, s_j - s_{y_i} + safety)``

  需要一个 safety value 的原因是去除 W 的一种错误情况: 即 W 的值导致每个样本的分数
  都差不多, 此时若没有 safety value, 将是得到 L = 0 的合理 W 值.

  Hinge loss. the shape of the graph.

  * value range of L: ``[0, \infty)``

  * 已经正确标记的训练样本分数 (在 threshold 以上时) 贡献 loss 0.

  * 当 W 很小时, 所有样本的 ``s \approx 0``, 此时 ``L = 样本数 - 1``.
    这是一个很有用的 debugging strategy, 即初始时检验是否符合预期.

  * 去掉 ``s_j = s_{y_i}`` 的求和项是为了将最小 L = 0, 否则最小 L = 1.

  * L = 0 的 W 值不是唯一的, 尤其是 ``W -> N*W`` 总能令 L = 0, scale up/down 
    不影响模型 (线性).

- overfitting & regularization. 训练的过程本质上是拟合 ``f(x, W)`` 的过程. 所以存在
  过拟合问题. 过拟合的效果是, 拟合曲线 (或者说 ``f(x, W)``) 完美匹配训练数据点,
  但对测试数据预测能力很差.

  解决过拟合问题, 直觉上我们需要对拟合曲线做一个 "矫正", "平滑化", 操作,
  penalizing your model. 假设 我们已经得到一个过拟合的 ``f``, 则应该在 ``y =
  f(x, W)`` 后面加一项补偿项, ``y = f(x, W) + c h(x) = f'(x, W)``. 这是在 x
  空间的描述. 为了求解这个新的 ``f'``, 对应在 W
  空间定义损失函数后面添加一个正则项 (regularization) ``\lambda R(W)``,
  得到新的 loss function 形式: ``L(W) = \frac{1}{N}\sum_{i=1}^N L_i(f(x_i, W),
  y_i) + \lambda R(W)``.

  hyperparameter lambda trades off between the two.

  * common regularizations

    - L2 regularization

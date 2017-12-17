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

  ``f(x, W)`` -> array of scores for each class. (Q: how can score be negative?)
 
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

- overfitting & regularization.

  只根据一些分立已知的数据点去求 W 矩阵, 显然是一个 underdetermined question (因为
  可以找到无数种方式靠近或穿过样本数据点). 也就是说, 训练的过程本质是根据已知数据
  拟合 ``f(x, W)`` 的过程. 因此这种拟合算法求得的令 L = 0 的 W 值不是唯一的.
  例如, ``W -> N*W`` 总能令 L = 0. 不同的 W 对应着不同的拟合曲线, 因此可能存在
  overfitting 问题. 过拟合的结果是, 拟合曲线 (或者说 ``f(x, W)``) 完美匹配训练数据点,
  但对测试数据预测能力很差.

  解决过拟合问题, 直觉上我们需要对拟合曲线做一个 "矫正", "平滑化" 操作,
  penalizing your model. (最简单的模型才是最通用的. (ocaccm's razor)) 假设我们已经得到
  一个过拟合的 ``f``, 则应该在 ``y = f(x, W)`` 后面加一项补偿项,
  ``y = f(x, W) + c h(x) = f'(x, W)``. 这是在 x 空间的描述. 为了求解这个新的
  ``f'``, 对应在 W 空间定义损失函数后面添加一个正则项 (regularization)
  ``\lambda R(W)``, 得到新的 loss function 形式:
  ``L(W) = \frac{1}{N}\sum_{i=1}^N L_i(f(x_i, W), y_i) + \lambda R(W)``.

  hyperparameter lambda trades off between the two.

  * common regularizations

    - L2: squared norm, half squared norm (for nicer derivative)
      ``R(W) = \sum_k\sum_l W_{k,l}^2`` (Q: what is L1, L2?)

      L2 norm 的特点大致可理解为, 当 W 的值各项分散在它的各个项时, 得到的
      loss 相对于 W 的值集中在少数几个项时的 loss 更小. 也就是说, L2
      regularization 倾向于比较分散的 W, 而不是集中的 W. 也就是说, 它可能
      更适用于当 x 的各维度都具有一定影响时, 而不是仅有少数几个维度有影响.

      L2 regularization 与 Bayesian inference 有关.

    - L1: ``R(W) = \sum_k\sum_l \abs{W_{k,l}}``, encouraging sparsity (Q: why?).

      L1 的倾向与 L2 相反, 即它更倾向于较集中的 W, 而不是更分散的 W. 这就是
      encouraging sparsity 的意思. 它容易让 W 的值倾向于大量的 0, 除了少数
      一些值之外. (more thoughts on this:
      https://stats.stackexchange.com/questions/45643/why-l1-norm-for-sparse-models
      https://en.wikipedia.org/wiki/Elastic_net_regularization
      http://www.chioka.in/differences-between-l1-and-l2-as-loss-function-and-regularization/)

    - Elastic net (L1+L2): ``R(W) = \sum_k\sum_l \beta W_{k,l}^2 + \abs{W_{k,l}}``

    - Max norm.

    - Dropout.

    - Batch normalization.

    - stochastic depth.

- cross entropy loss (softmax loss) (multinomial logistic regression)
  (Q: WTF?
  https://en.wikipedia.org/wiki/Multinomial_logistic_regression
  https://en.wikipedia.org/wiki/Cross_entropy)

  * softmax function (Q: what is it?)
    ``\frac{e^{s_k}}{\sum_j e^{s_j}}``
    where ``s = f(x_j; W)``
    (Q: semicolon?
    https://math.stackexchange.com/questions/342268/what-does-the-semicolon-mean-in-a-function-definition)

  * 对 score 进行定义. score = unnormalized log probabilities of the classes.
    (Q: log probability?)
    经过 softmax 操作后得到的是该样本 ``x_i`` 被识别为某个 class ``k`` 的概率分布.
    即 ``P(Y=k|X=x_i) = \frac{e^{s_k}}{\sum_j e^{s_j}}``

  * log probability 比原始的概率分布更容易在计算机上计算. 因此, 对该条件概率做 log
    运算. 我们希望最大化这个 log probability. 构建 loss function ``Li = - log p(Y|x)``
    即我们希望最小化这个 Li 损失 (这么构建是因为 loss 应该是正的).

  * 最终得到 loss function 形式:
    ``L = \frac{1}{N}\sum_i^N Li = - \frac{1}{N}\sum_i^N log(\frac{e^{s_{y_i}}}{\sum_j e^{s_j}})``

  * Li 的值域: ``[0, \infty]``

  * 为了得到 Li = 0, 除了 yi 之外的 ``s_j`` 必须是无限趋于 ``-\infty``. 而 ``s_{y_i}``
    应该是很大的正值. (Q: 需要是 infinity 么?)
    由于计算机无法做到 infinity, 在有限的时间下, 得不到 Li = 0 的结果, 只能很小.
    即得不到完全的 ``(1,0,0,...)`` 式的 softmax 概率分布. 类似的, 也无法在有限时间
    资源和精度下, 得到 ``Li -> \infty`` 的情形, 因为需要 ``e^{s_{y_i}} -> -\infty`` .

  * 初始时, W 很小, ``s\approx 0``, 此时 ``Li = -log(\frac{1}{C})``, 可用于 debug.

- SVM vs cross entropy

  * SVM loss 中, 当正确和错误的分类分数差达到一定的 threshold 之后, loss 就 = 0 了.
    因此, 在 SVM 中, 参数优化到一定程度就会停止.

  * cross entropy loss 中, 要达到 L = 0, 要求错误分类的分数达到 ``-\infty``,
    正确分类的分数足够大. 因此系统会不断优化参数, 一直将错误分类的分数向负无穷
    靠近, 正确分类的分数向正无穷靠近.

  * 虽然在理论上两者有这些区别, 但在实际使用中, 结果区别并不大.

optimization of W
-----------------

现在的任务是寻找一个能够让 loss 取最小值的 W. 有多种优化解法.

为什么不直接去解 ``\gradient F(x) = 0`` 的解析解呢?
因为:

setting derivatives to 0 is only useful when the system ∇F(x)=0 happens to be a
linear one (or at least, an explicit system of equations in which x can be
isolated). Otherwise, one may have to solve a system of nonlinear equations,
which entails the use of some gradient-descent or Newton type method.

when your first-order derivative system is a linear system of equations,
solving this system directly is typically much more computationally attractive
than using gradient-descent (whose convergence can be slow). When your
first-order derivative system is not a linear system, then alternative
strategies (including, but not limited to, gradient descent) may be more
attractive.

random search
~~~~~~~~~~~~~
of course not.

gradient descent
~~~~~~~~~~~~~~~~
simple and effective.

- numerical gradient: 假设步长, 对每个分量做有限差分, 求得梯度分量值, 选取负梯度
  最大的方向对应的 W 是新的 W.

  approximate, slow, easy to write.

- analytic gradient: 根据 loss function 解析形式给出它的梯度解析形式. 梯度给出了
  x 的变化方向, 所以 W 矢量减去步长*梯度就得到了下一个 W 值.

  exact, fast, error-prone.

use analytic gradient in practice, but check implementation with
numerical gradient (common debugging strategy: gradient check).

- 步长是一个重要 hyperparameter.

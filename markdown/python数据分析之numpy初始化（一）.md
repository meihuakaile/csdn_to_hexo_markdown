---
title: python数据分析之numpy初始化（一）
tags: ['numpy', '数据分析']
categories: ['cnn图片数据处理、显示', 'python数据分析']
copyright: true
---
以下都用numpy的标准“import numpy as np”  
1.numpy是同构数据多维容器，同构即数据类型相同  
2.初始化：  

2.1  np.arange([start,] end [, step])  #与list的range相似

    
    
     >>> np.arange(10)
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> np.arange(1, 10, 2)
    array([1, 3, 5, 7, 9])

  
2.2  np.zeros(tupleA)  #产生一个tupleA维度大小的矩阵，且初始全为0  

    
    
    >>> np.zeros((4))
    array([ 0.,  0.,  0.,  0.])
    >>> np.zeros((4,2))
    array([[ 0.,  0.],
           [ 0.,  0.],
           [ 0.,  0.],
           [ 0.,  0.]])

  

2.3  np.ones(tupleA)  #与上面类似，只是初始化全为1

    
    
    >>> np.ones((4))
    array([ 1.,  1.,  1.,  1.])
    >>> np.ones((4,2))
    array([[ 1.,  1.],
           [ 1.,  1.],
           [ 1.,  1.],
           [ 1.,  1.]])

  
2.4  np.empty(tupleA)  #与上面类似，只是初始化值是不确定的（并不是你以为的0！！！！）  

    
    
    >>> np.empty((4))
    array([  1.73154357e-316,   4.71627160e-317,   0.00000000e+000,
             4.94065646e-324])
    >>> np.empty((3,2))
    array([[  0.00000000e+000,   0.00000000e+000],
           [  6.94647584e-310,   6.94647586e-310],
           [  6.94647586e-310,   6.94647586e-310],

  
2.5  np.array(listA)  #把listA转成np，listA只是一个统称，只要是序列化的都可以，还可以是其他np  

    
    
    >>> np.array([[1, 2, 3], [4, 3, 2]])
    array([[1, 2, 3],
           [4, 3, 2]])
    >>> npA = np.array([[1, 2, 3], [4, 3, 2]])
    >>> npA
    array([[1, 2, 3],
           [4, 3, 2]])
    >>> npB = np.array([[1, 2, 3], [4, 3, 2.0]])
    >>> npB
    array([[ 1.,  2.,  3.],
           [ 4.,  3.,  2.]])
      np.array会自动找到最适合listA数据类型转给np:
    >>> npA.dtype
    dtype('int64')
    >>> npB.dtype
    dtype('float64')

但其实，  np初始化时没有特别说明都会被默认是float64  ，如前四种

  

2.6其他：  ones_like(npA);zeros_like(npA);empty_like(npA)  

    
    
    >>> npB = np.array([[1, 2, 3], [4, 3, 2.0]])
    >>> np.ones_like(npB)
    array([[ 1.,  1.,  1.],
           [ 1.,  1.,  1.]])
    >>> np.zeros_like(npB)
    array([[ 0.,  0.,  0.],
           [ 0.,  0.,  0.]])
    >>> np.empty_like(npB)
    array([[  0.00000000e+000,   0.00000000e+000,   1.56491143e-316],
           [  6.94647850e-310,   6.94635322e-310,   1.72361006e-316]])
    >>> np.identity(3)
    array([[ 1.,  0.,  0.],
           [ 0.,  1.,  0.],
           [ 0.,  0.,  1.]])
    >>> np.eye(3, k = -1)#变化k的值试试看
    array([[ 0.,  0.,  0.],
           [ 1.,  0.,  0.],
           [ 0.,  1.,  0.]])
    

  
  
  
  


import numpy as np

def custom_distance(x, y):
    # 计算自定义距离 (x1-y1)^2 + (x2-y2)^2 + ...
    return np.sum((x - y)**2)

def find_closest_vector(A, a):
    # 计算每个向量与a之间的自定义距离
    distances = np.sum((A - a)**2, axis=1)
    
    # 找到距离最小的向量的索引
    closest_index = np.argmin(distances)
    
    # 返回距离最小的向量和其索引
    closest_vector = A[closest_index]
    return closest_vector, closest_index
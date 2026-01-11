from typing import List
import math


class Solution:
  def hclus_single_link(self, X: List[List[float]], K: int) -> List[int]:
    # Single link hierarchical clustering
    res = [0] * len(X)
    distances = {}
    clusters = []
    
    if len(X) == K:
      return list(range(K))
    for i in range(len(X)):
      clusters.append([i])
    for point1 in range(len(X)):
      for point2 in range(point1 + 1, len(X)):
        distance = math.sqrt((X[point1][0] - X[point2][0])**2 + 
                             (X[point1][1] - X[point2][1])** 2)
        distances[(point1, point2)] = distance
        distances[(point2, point1)] = distance
    
    while len(clusters) > K:
      minDistance = float("inf")
      for point1 in range(len(clusters)):
        for point2 in range(point1 + 1, len(clusters)):
          dist = float("inf")
          for p in clusters[point1]:
              for q in clusters[point2]:
                if distances[(p, q)] < dist:
                  dist = distances[(p, q)]
          if dist < minDistance:
            minDistance = dist
            merge1, merge2 = point1, point2
      newClust = clusters[merge1] + clusters[merge2]
      clusters.append(newClust)
      
      if merge1 > merge2:
        clusters.pop(merge1)
        clusters.pop(merge2)
      else:
        clusters.pop(merge2)
        clusters.pop(merge1)
      for index, cluster in enumerate(clusters):
        for point in cluster:
          res[point] = index
    
    return res
    

  def hclus_average_link(self, X: List[List[float]], K: int) -> List[int]:
    """Complete link hierarchical clustering"""
    res = [0] * len(X)
    distances = {}
    clusters = []
    
    if len(X) == K:
      return list(range(K))
    for i in range(len(X)):
      clusters.append([i])
    for point1 in range(len(X)):
      for point2 in range(point1 + 1, len(X)):
        distance = math.sqrt((X[point1][0] - X[point2][0])**2 + 
                             (X[point1][1] - X[point2][1])** 2)
        distances[(point1, point2)] = distance
        distances[(point2, point1)] = distance
    
    while len(clusters) > K:
      minDistance = float("inf")
      for point1 in range(len(clusters)):
        for point2 in range(point1 + 1, len(clusters)):
          count, total = 0, 0
          for p in clusters[point1]:
              for q in clusters[point2]:
                total += distances[(p, q)]
                count += 1
          dist = total / count
          if dist < minDistance: 
            minDistance = dist
            merge1, merge2 = point1, point2
      newClust = clusters[merge1] + clusters[merge2]
      clusters.append(newClust)
      
      if merge1 > merge2:
        clusters.pop(merge1)
        clusters.pop(merge2)
      else:
        clusters.pop(merge2)
        clusters.pop(merge1)
      for index, cluster in enumerate(clusters):
        for point in cluster:
          res[point] = index
    
    return res


  def hclus_complete_link(self, X: List[List[float]], K: int) -> List[int]:
    """Average link hierarchical clustering"""
    res = [0] * len(X)
    distances = {}
    
    if len(X) == K:
      return list(range(K))
    clusters = []
    for i in range(len(X)):
      clusters.append([i])
    for point1 in range(len(X)):
      for point2 in range(point1 + 1, len(X)):
        distance = math.sqrt((X[point1][0] - X[point2][0])**2 + 
                             (X[point1][1] - X[point2][1])** 2)
        distances[(point1, point2)] = distance
        distances[(point2, point1)] = distance
    
    while len(clusters) > K:
      minDistance = float("inf")
      for point1 in range(len(clusters)):
        for point2 in range(point1 + 1, len(clusters)):
          dist = 0
          for p in clusters[point1]:
              for q in clusters[point2]:
                if distances[(p, q)] > dist:
                  dist = distances[(p, q)]
          if dist < minDistance:
            minDistance = dist
            merge1, merge2 = point1, point2
      newClust = clusters[merge1] + clusters[merge2]
      clusters.append(newClust)
      if merge1 > merge2:
        clusters.pop(merge1)
        clusters.pop(merge2)
      else:
        clusters.pop(merge2)
        clusters.pop(merge1)
    
    for index, cluster in enumerate(clusters):
      for point in cluster:
        res[point] = index
    
    return res

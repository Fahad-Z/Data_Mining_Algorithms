from typing import List
import math

class Node:
  def __init__(self):
    self.split_dim = -1
    self.split_point = -1
    self.label = -1
    self.left = None
    self.right = None


class Solution:
  def split_node(self, node, data, label, depth=0):
    labelCount = {}
    for i in label:
      if i not in labelCount:
        labelCount[i] = 0
      labelCount[i] += 1
    bestL, bestCount = None, -1
    for l in labelCount:
      count = labelCount[l]
      if count > bestCount:
        bestL = l
        bestCount = count
      elif count == bestCount:
        if  bestL is None or l < bestL:
          bestL = l
    node.label = bestL

    if depth == 2 or len(labelCount) == 1:
      return
    entro = self.entropy(label)
    topGain, topDim, splitPoint = -float("inf"), -1, float("inf")
    for i in range(len(data[0])):
      columnVal = [row[i] for row in data]
      columnVal.sort()
      splits = []
      for j in range(len(columnVal) - 1):
        mid = (columnVal[j] + columnVal[j + 1]) /2
        splits.append(mid)
      splits.sort()
      for point in splits:
        infoA = self.split_info(data, label, i, point)
        gain = entro - infoA
        change = False
        if gain > topGain:
          change = True
        elif gain == topGain:
          if i < topDim:
            change = True
          elif i == topDim and i < splitPoint:
              change = True
        if change:
          topGain,  topDim, splitPoint = gain, i, point
    if topDim == -1:
      return
    node.split_dim, node.split_point = topDim, splitPoint

    lData, lLabels, rData, rLabels = [], [], [], []
    for i, j in zip(data, label):
        if i[topDim] <= splitPoint:
          lData.append(i)
          lLabels.append(j)
        else:
          rData.append(i)
          rLabels.append(j)
    if len(rData) == 0 or len(lData) == 0:
      return
    node.left, node.right = Node(), Node()

    self.split_node(node.left, lData, lLabels, depth + 1)
    self.split_node(node.right, rData, rLabels, depth + 1)

  def entropy(self, label):
      count, res = {}, 0
      for i in label:
        if i not in count:
          count[i] = 0
        count[i] += 1
      for j in count.values():
        res -= (j/len(label) * math.log2(j/len(label)))

      return res

  def split_info(self, data: List[List[float]], label: List[int], split_dim: int, split_point: float) -> float:
    left, right = [], []
    for i, j in zip(data, label):
        if i[split_dim] <= split_point:
          left.append(j)
        else:
          right.append(j)
    if len(right) == 0 or len(left) == 0:
       return float("inf")
    res = ((len(left)/ len(label))* self.entropy(left) + 
           (len(right)/ len(label))* self.entropy(right))
    
    return res


  def fit(self, train_data: List[List[float]], train_label: List[int]) -> None:
    self.root = Node()
    self.split_node(self.root, train_data, train_label, 0)


  def classify(self, train_data: List[List[float]], train_label: List[int], test_data: List[List[float]]) -> List[int]:
    self.fit(train_data, train_label)
    res = []
    
    for i in test_data:
        node = self.root
        while node.right is not None and node.left is not None:
          if i[node.split_dim] <= node.split_point:
            node = node.left
          else:
            node = node.right
        res.append(node.label)
        
    return res

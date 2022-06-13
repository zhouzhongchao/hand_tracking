用torch数据时 .max()返回两个值，一个是最大数据一个是index

gather()

import torch

b = torch.Tensor([[1, 2, 3], [4, 5, 6]])

index_1 = torch.LongTensor([[0, 1], [2, 0]])

print(torch.gather(b, dim=1, index=index_1))

# 输出

tensor([[1., 2.],

[6., 4.]])
index_1的意思是第一行的0个，第一行的第一个
第二行的第2个 第二行的第0个
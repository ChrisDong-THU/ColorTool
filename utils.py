# This Python file uses the following encoding: utf-8
import numpy as np
from sklearn.cluster import KMeans


class ColorTool():
    def __init__(self) -> None:
        pass
        # 初始化参数
        self.color_num = 2
        # 色卡数量
        self.color_list = np.array([
            [0, 0, 255],
            [237, 173, 158],
            [140, 199, 181],
            [120, 205, 205],
            [79, 148, 205],
            [205, 150, 205]
        ])
        # 颜色类型
        self.color_type = 3 # 1: [0, 1], 2: [0, 255], 3: #hex, 4: hsv
        # 读入的原始图片
        self.ori_pic = None # RGB格式
        # 处理后所得各色块
        self.rgb_list = None
    
    def updatedata(self):
        Rchannel = self.ori_pic[:, :, 0]
        Gchannel = self.ori_pic[:, :, 1]
        Bchannel = self.ori_pic[:, :, 2]
        
        self.rgb_list = np.vstack((Rchannel, Gchannel, Bchannel), dtype=np.double)
    
    def kmeanscore(self):
        self.updatedata()
        
        kmeans = KMeans(n_clusters=self.color_num, init='k-means++', max_iter=1000, n_init=10)
        kmeans.fit(self.rgb_list)
        C = kmeans.cluster_centers_
        
        # 以下为聚类结束后的重排序，依据RGB矩阵均值最大列为正权重
        # RGB均值次大、最小列为负权重
        # 对颜色数组进行重排序[为了更好的视觉效果]
        C = np.round(C)
        cmean = np.mean(C, axis=0)
        cindex = np.argsort(cmean)[::-1]
        coe = np.zeros((3,1))
        coe[cindex[0]] = 1
        coe[cindex[1]] = -0.4
        coe[cindex[2]] = -0.6
        index = np.argsort(np.dot(C, coe))[::-1]
        C = C[index,:]

        self.color_list = C
# if __name__ == "__main__":
#     pass

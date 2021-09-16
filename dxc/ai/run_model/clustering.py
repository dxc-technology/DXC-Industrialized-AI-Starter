# from numpy import unique
# from numpy import where
# from math import sqrt
# from sklearn.datasets import make_classification
# from sklearn.cluster import AffinityPropagation
# from matplotlib import pyplot
# from sklearn.metrics import silhouette_samples, silhouette_score,davies_bouldin_score
# from math import sqrt
# from sklearn.cluster import KMeans
# from sklearn.cluster import DBSCAN

# def Clustering(X,num_clusters=None):
#     AP = AffinityPropagation(damping=0.9)
#     AP.fit(X)
#     # assign a cluster to each example
#     yhat_AP = AP.predict(X)
#     silhouette_AP = silhouette_score(X, yhat_AP)
    
#     def optimal_number_of_clusters(wcss):
#         x1, y1 = 2, wcss[0]
#         x2, y2 = 20, wcss[len(wcss)-1]

#         distances = []
#         for i in range(len(wcss)):
#             x0 = i+2
#             y0 = wcss[i]
#             numerator = abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1)
#             denominator = sqrt((y2 - y1)**2 + (x2 - x1)**2)
#             distances.append(numerator/denominator)    
#         return distances.index(max(distances)) + 2
#     if num_clusters!=None:
#         model_KM=KMeans(n_clusters=num_clusters)
#         model_KM.fit(X)
#         # assign a cluster to each example
#         yhat_KM = model_KM.predict(X)
#         silhouette_KM = silhouette_score(X, yhat_KM)
#     else:
#         wcss = []
#         for n in range(2, 21):
#             kmeans = KMeans(n_clusters=n)
#             kmeans.fit(X)
#             wcss.append(kmeans.inertia_)
#         clusters=optimal_number_of_clusters(wcss)
#         model_KM=KMeans(n_clusters=clusters)
#         model_KM.fit(X)
#         # assign a cluster to each example
#         yhat_KM = model_KM.predict(X)
#         silhouette_KM = silhouette_score(X, yhat_KM)
    
#     model_DB = DBSCAN(eps=9.5, min_samples=2)
#     # fit model and predict clusters
#     yhat_DB = model_DB.fit_predict(X)
#     silhouette_DB = silhouette_score(X, yhat_DB)
    
#     silhouette=[silhouette_DB,silhouette_KM,silhouette_AP]
#     algo=[model_DB,model_KM,AP]
#     maxi=algo[silhouette.index(max(silhouette))]
    
#     return maxi.fit(X)
    
    
        

## https://www.michelecoscia.com/?page_id=734 ## 
## unipartite projections of bipartite networks ##

import numpy as np
import networkx as nx
from scipy import sparse
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import normalize

def ycn(network, nodes, directed = False):
   T = nx.algorithms.bipartite.matrix.biadjacency_matrix(network, row_order = nodes)
   T_norm = normalize(T, norm = 'l1', axis = 1) # Divide each row element with the row sum (Eq. [1] in the paper)
   T_t_norm = normalize(T.T, norm = 'l1', axis = 1) # Divide each row element of the transpose with the transposed row sum (Eq. [2] in the paper) 
   T = T_norm.dot(T_t_norm) # Multiply (Eq. [3] in the paper)
   _, stdistr = sparse.linalg.eigs(T.T, k = 1)
   stdistr /= stdistr.sum()
   stdistr = np.real(stdistr[:,0])
   U = T.T.multiply(sparse.csr_matrix(stdistr).T).T
   U.setdiag(0)
   U.eliminate_zeros()
   if directed:
      G = nx.from_scipy_sparse_matrix(U, create_using = nx.DiGraph())
   else:
      U += U.T
      G = nx.from_scipy_sparse_matrix(U / 2)
   return nx.relabel_nodes(G, {i: nodes[i] for i in range(len(nodes))})

def simple(network, nodes):
   T = nx.algorithms.bipartite.matrix.biadjacency_matrix(network, row_order = nodes)
   U = T * T.T
   U.setdiag(0)
   U.eliminate_zeros()
   G = nx.from_scipy_sparse_matrix(U)
   return nx.relabel_nodes(G, {i: nodes[i] for i in range(len(nodes))})

def hyperbolic(network, nodes):
   T = nx.algorithms.bipartite.matrix.biadjacency_matrix(network, row_order = nodes)
   T /= T.sum(axis = 0)
   T = sparse.csr_matrix(T)
   U = T * T.T
   U.setdiag(0)
   U.eliminate_zeros()
   G = nx.from_scipy_sparse_matrix(U)
   return nx.relabel_nodes(G, {i: nodes[i] for i in range(len(nodes))})

def jaccard(network, nodes):
   T = nx.algorithms.bipartite.matrix.biadjacency_matrix(network, row_order = nodes)
   j_dist = 1.0 - pairwise_distances(T.todense(), metric = "jaccard", n_jobs = -1)
   np.fill_diagonal(j_dist, 0)
   G = nx.from_numpy_matrix(j_dist)
   return nx.relabel_nodes(G, {i: nodes[i] for i in range(len(nodes))})

def euclidean(network, nodes): #TODO: ???
   T = nx.algorithms.bipartite.matrix.biadjacency_matrix(network, row_order = nodes)
   j_dist = 1.0 / pairwise_distances(T, metric = "euclidean", n_jobs = -1)
   j_dist[j_dist == np.inf] = 1
   np.fill_diagonal(j_dist, 0)
   G = nx.from_numpy_matrix(j_dist)
   return nx.relabel_nodes(G, {i: nodes[i] for i in range(len(nodes))})

def cosine(network, nodes):
   T = nx.algorithms.bipartite.matrix.biadjacency_matrix(network, row_order = nodes)
   j_dist = 1.0 - pairwise_distances(T, metric = "cosine", n_jobs = -1)
   np.fill_diagonal(j_dist, 0)
   G = nx.from_numpy_matrix(j_dist)
   return nx.relabel_nodes(G, {i: nodes[i] for i in range(len(nodes))})

def pearson(network, nodes):
   T = nx.algorithms.bipartite.matrix.biadjacency_matrix(network, row_order = nodes)
   j_dist = (2.0 - pairwise_distances(T.todense(), metric = "correlation", n_jobs = -1)) / 2
   np.fill_diagonal(j_dist, 0)
   j_dist[j_dist < .5] = 0
   G = nx.from_numpy_matrix(j_dist)
   return nx.relabel_nodes(G, {i: nodes[i] for i in range(len(nodes))})

def probs(network, nodes, directed = False):
   T = nx.algorithms.bipartite.matrix.biadjacency_matrix(network, row_order = nodes)
   T_norm = normalize(T, norm = 'l1', axis = 1) # Divide each row element with the row sum (Eq. [1] in the paper)
   T_t_norm = normalize(T.T, norm = 'l1', axis = 1) # Divide each row element of the transpose with the transposed row sum (Eq. [2] in the paper) 
   T = T_norm.dot(T_t_norm) # Multiply (Eq. [3] in the paper)
   T.setdiag(0)
   T.eliminate_zeros()
   if directed:
      G = nx.from_scipy_sparse_matrix(T, create_using = nx.DiGraph())
   else:
      T += T.T
      G = nx.from_scipy_sparse_matrix(T / 2)
   return nx.relabel_nodes(G, {i: nodes[i] for i in range(len(nodes))})

def heats(network, nodes, directed = False):
   T = nx.algorithms.bipartite.matrix.biadjacency_matrix(network, row_order = nodes)
   T_norm = normalize(T, norm = 'l1', axis = 1) # Divide each row element with the row sum (Eq. [1] in the paper)
   T_t_norm = normalize(T.T, norm = 'l1', axis = 1) # Divide each row element of the transpose with the transposed row sum (Eq. [2] in the paper) 
   T = T_norm.dot(T_t_norm).T # Multiply (Eq. [3] in the paper)
   T.setdiag(0)
   T.eliminate_zeros()
   if directed:
      G = nx.from_scipy_sparse_matrix(T, create_using = nx.DiGraph())
   else:
      T += T.T
      G = nx.from_scipy_sparse_matrix(T / 2)
   return nx.relabel_nodes(G, {i: nodes[i] for i in range(len(nodes))})

def hybrid(network, nodes, l, directed = False):
   T = nx.algorithms.bipartite.matrix.biadjacency_matrix(network, row_order = nodes)
   probs_norm = normalize(T, norm = 'l1', axis = 1) # Divide each row element with the row sum (Eq. [1] in the paper)
   heats_norm = normalize(T, norm = 'l1', axis = 1) # Divide each row element with the row sum (Eq. [1] in the paper)
   probs_norm.data **= l
   heats_norm.data **= (1 - l)
   T_t_norm = normalize(T.T, norm = 'l1', axis = 1) # Divide each row element of the transpose with the transposed row sum (Eq. [2] in the paper) 
   probs_norm = probs_norm.dot(T_t_norm)
   heats_norm = heats_norm.dot(T_t_norm).T
   T = probs_norm.multiply(heats_norm)
   if directed:
      G = nx.from_scipy_sparse_matrix(T, create_using = nx.DiGraph())
   else:
      T += T.T
      G = nx.from_scipy_sparse_matrix(T / 2)
   return nx.relabel_nodes(G, {i: nodes[i] for i in range(len(nodes))})


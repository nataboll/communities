#include <iostream>
#include <vector>
#include <memory>
#include <utility>
#include <algorithm>
#include <map>
#include <set>

/*
 * Class Vertex represents agents
 * T is a type for vertexes number (edges number for dense graph)
 * W is a type for weights and profit
 * u is importance
 */
template<class T, class W>
class Vertex {

public:
    using Ref = std::shared_ptr<Vertex>;
    using Neighbor = std::pair<Ref, W>;

private:
	T num;
	T cluster;
	W u;
	std::vector<Neighbor> in_neighbors;
	std::vector<Neighbor> out_neighbors;
	W profit;

public:
	W compute_profit(T new_cluster) {
		W d = 0;
        for (auto neigh : out_neighbors) {
		    if (neigh.first->cluster == new_cluster)
			    d += (neigh.first->u) * neigh.second;
		    else 
			    d += (1 - neigh.first->u) * (1 - neigh.second);
        }
		return d;
	}

	Vertex(T _num) : num(_num)
			, cluster(_num)
			, profit(0)
	{}

	W step(bool directed, std::vector<Ref> &vertexes) {	
		W new_profit = profit;
		T new_cluster = cluster;
		W delta = 0;

		for (auto next : out_neighbors) {
            T tmp_new_cluster = next.first->get_cluster();
			W d = compute_profit(tmp_new_cluster);
			if (d > new_profit) {
                W voter = 0; 

                if (tmp_new_cluster != cluster) {
                    for (auto vertex : vertexes) {
                        if (vertex->cluster == tmp_new_cluster) {
                            for (auto neigh : vertex->get_out_neighbors()) {
                                if (neigh.first->get_num() == num) {
                                    voter += u*neigh.second - (1 - u) * (1 - neigh.second); 
                                }
                            }
                        }   
                    }
                }
                if (voter >= 0) {
            		new_profit = d;
                    new_cluster = tmp_new_cluster;
                }
			}
		}

        if (new_profit == 0) { 
            new_cluster = num;
            new_profit = 0;
        }

        std::vector<Neighbor> in_neigh = directed ? in_neighbors : out_neighbors;
        
        if (new_cluster != cluster) {
            for (auto next : in_neigh) {
                if (next.first->cluster == new_cluster) 
                    next.first->profit += (u * next.second - (1 - u)*(1 - next.second));
                else if (next.first->cluster == cluster)
                    next.first->profit += ((1 - u) * (1 - next.second) - u * next.second);
            }
        }

		delta = new_profit - profit;
		profit = new_profit;
		cluster = new_cluster;
		return delta;
	}

	T get_num() const {
		return num;
	}

	void add_in_neighbor(Ref i, W w) {
		in_neighbors.push_back(std::make_pair(i, w));
	}

	std::vector<Neighbor> get_in_neighbors() const {
		return in_neighbors;
	}

	void add_out_neighbor(Ref i, W w) {
		out_neighbors.push_back(std::make_pair(i, w));
	}

	std::vector<Neighbor> get_out_neighbors() const {
		return out_neighbors;
	}

	void set_u(float _u) {
		u = _u;
	}

	float get_u() const {
		return u;
	}

	void set_cluster(T _c) {
		cluster = _c;
	}

	T get_cluster() const {
		return cluster;
	}

	void set_profit(W _p) {
		profit = _p;
	}

	W get_profit() const {
		return profit;
	}
};

template<class T, class W>
class Compare {
public:
    bool operator() (const typename Vertex<T, W>::Ref &v1, const typename Vertex<T, W>::Ref &v2) const {
        return v1->get_cluster() < v2->get_cluster();
    }
};

/*
 * Class Graph represents agents network
 * Templates parameters are for Vertex
 */
template<class T, class W>
class Graph {

public:
    using Ref = std::shared_ptr<Vertex<T, W>>;
    using Neighbor = std::pair<T, W>;

private:
	std::vector<Ref> vertexes;
	bool directed = true;
    std::map<int, std::set<Vertex<T, W>>> clusters;

	void read_edges(T m, bool _directed = true) {
		for (T i = 0; i < m; i++) {
            T out_ver = 0, in_ver = 0;
            W w = 0;
            std::cin >> out_ver >> in_ver >> w;
            vertexes[out_ver]->add_out_neighbor(vertexes[in_ver], w);
            if (_directed) {
                vertexes[in_ver]->add_in_neighbor(vertexes[out_ver], w);
                directed = true;
            } else {
                vertexes[in_ver]->add_out_neighbor(vertexes[out_ver], w);
            }
        }
	}

    void read_centralities() {
        for (auto vertex : vertexes) {
            float u = 0;
            std::cin >> u;
            vertex->set_u(u);
        }   
    }

	void compute_importances() {
        read_centralities();
    }

public:
	Graph(T n, T m, bool _directed = true) : vertexes(n), directed(_directed)
	{
		for (T i = 0; i < n; i++) {
			vertexes[i] = std::shared_ptr<Vertex<T, W>>(new Vertex<T, W>(i));
		}

		read_edges(m, _directed);
	}

	void print_g() const {
		for (auto vertex : vertexes) {
			std::cout << "Vertex " << vertex->get_num() << "(" << vertex->get_u() << "): ";
			for (auto neighbor : vertex->get_out_neighbors()) {
				std::cout << neighbor.first->get_num() << "(" << neighbor.second << "), ";
			}
			std::cout << std::endl;
		}
		std::cout << std::endl;
	}

	void find_communities() {
		compute_importances();
		bool stop = false;
        W feedback = 0;
        auto order = vertexes; //
		while (!stop) {
            stop = true;
            std::random_shuffle(order.begin(), order.end()); //
			for (auto vertex : order) { //
                feedback = vertex->step(directed, vertexes);
                if (feedback) {
                    stop = false;
                }
            }
		}
	}

	std::vector<T> get_clusters() const {
		std::vector<T> cl(vertexes.size());
		for (int i = 0; i < cl.size(); i++) {
			cl[i] = vertexes[i]->get_cluster();
		}
		return cl;
	}

    void set_status(std::vector<T> &clusters, std::vector<W> &profits) {
        for (T i = 0; i < clusters.size(); i++) {
            vertexes[i]->set_cluster(clusters[i]);
            vertexes[i]->set_profit(profits[i]);
        }
    }

    T get_clusters_num() const {
        std::vector<Ref> tmp = vertexes;
        std::sort(tmp.begin(), tmp.end(), Compare<T, W>());
        T curr = -1;
        T counter = 0;
        for (T i = 0; i < tmp.size(); i++) {
            if (tmp[i]->get_cluster() != curr) {
                curr = tmp[i]->get_cluster();
                counter++;
            }
        }
        return counter;
    }

    std::vector<float> get_utilities() const {
        std::vector<float> utils(vertexes.size());
        for (int i = 0; i < utils.size(); i++) {
            utils[i] = vertexes[i]->get_u();
        }
        return utils;
    }

    std::vector<W> get_profits() const {
        std::vector<W> profits(vertexes.size());
        for (int i = 0; i < profits.size(); i++) {
            profits[i] = vertexes[i]->get_profit();
        }
        return profits;
    }
};

void show_differences(std::vector<int> &clusters_i, std::vector<int> &clusters_f, std::vector<float> &profits_i, std::vector<float> &profits_f) {
    for (int i = 0; i < clusters_i.size(); i++) {
        if (clusters_i[i] != clusters_f[i])
            std::cout << i << ": " << clusters_i[i] << " -> " << clusters_f[i] << ": p_1 = " << profits_i[i] << ", p_2 = " << profits_f[i] 
                << std::endl;
    }
}

int main() {
	int n, m = 0;
	std::cin >> n >> m;
	Graph<int, float> g(n, m, false);
    Graph<int, float> g_d(n, m, true);

//    std::cout << n << " vertices" << std::endl;
//    std::cout << m << " edges" << std::endl;

/*    std::vector<int> clusters_d = g_d.get_clusters();
    std::cout << std::endl;
    std::cout << "Directed:" << std::endl;
    for (int i = 0; i < clusters_d.size(); i++) {
        std::cout << clusters_d[i] << "(i = " << utilities_d[i] << ", p = " << profits_d[i] << "), ";
    }   */

/*    std::cout << "Undirected:" << std::endl;
    for (int i = 0; i < clusters.size(); i++) {
        std::cout << clusters[i] << "(i = " << utilities[i] << ", p = " << profits[i] << "), ";
    } */

    g_d.find_communities();


//    std::vector<float> utilities_d = g_d.get_utilities();
//    std::vector<float> profits_d = g_d.get_profits();
    
//    g.set_status(clusters_d, profits_d);
//    g.find_communities();
//    std::vector<int> clusters = g.get_clusters();
//    std::vector<float> utilities = g.get_utilities();
//    std::vector<float> profits = g.get_profits();



    std::cout << g_d.get_clusters_num() << std::endl;

    std::vector<int> clusters_d = g_d.get_clusters();
    for (int i = 0; i < clusters_d.size(); i++) {
        std::cout << clusters_d[i] << " ";
    }



//   std::cout << g_d.get_clusters_num() << std::endl;

//    std::cout << "Directed: " << g_d.get_clusters_num() << " clusters" << std::endl;
//    std::cout << "Undirected: " << g.get_clusters_num() << " clusters" << std::endl;
//    std::cout << std::endl;
//    std::cout << "Jumps:" << std::endl;
//    show_differences(clusters_d, clusters, profits_d, profits); 

//    g_d.print_g();

	return 0;
}


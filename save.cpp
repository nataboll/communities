    void closeness_centrality() {
        for (auto vertex : vertexes) {
            W util = 0;
            for (auto neighbor : vertex->get_out_neighbors()) {
                util = std::max(util, (float)1 / (float)neighbor.second);
            }
            vertex->set_u(util);
        }
    }

    void degree_centrality() {
        int max_degree = 1;
        for (auto vertex : vertexes) {
            if ((vertex->get_out_neighbors()).size() > max_degree)
                max_degree = (vertex->get_out_neighbors()).size();
            }
        for (auto vertex : vertexes) {
            vertex->set_u((float)((vertex->get_out_neighbors()).size()) / (float)max_degree);
        }
    }

    void weighted_degree_centrality() {
        for (auto vertex : vertexes) {
            W util = 0;
            for (auto neighbor : vertex->get_out_neighbors()) {
                util += neighbor.second;
            }
            vertex->set_u(util);
        }
    }

    void random_importances() {
        srand(time(0));
        for (auto vertex : vertexes)
            vertex->set_u((float)(rand() % 1000)/(float)1000);
    }

    void static_importances() {
        for (auto vertex : vertexes) 
            vertex->set_u(0.5);
    }


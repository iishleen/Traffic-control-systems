// Compile with c++ ece650-a2cpp -std=c++11 -o ece650-a2
#include <iostream>
#include <sstream>
#include <vector>
#include<ctype.h>
#include<bits/stdc++.h>
using namespace std;
vector<int> adj[]={};
// utility function to form edge between two vertices
// source and dest
void add_edge(vector<int> adj[], int src, int dest)
{
    adj[src].push_back(dest);
    adj[dest].push_back(src);
}
// a modified version of BFS that stores predecessor
// of each vertex in array p
// and its distance from source in array d
bool BFS(vector<int> adj[], int src, int dest, int v,
							int pred[], int dist[])
{

	list<int> queue;
	bool visited[v];

	for (int i = 0; i < v; i++) {
		visited[i] = false;
		dist[i] = INT_MAX;
		pred[i] = -1;
	}

	visited[src] = true;
	dist[src] = 0;
	queue.push_back(src);

	// standard BFS algorithm
	while (!queue.empty()) {
		int u = queue.front();
		queue.pop_front();
		for (int i = 0; i < adj[u].size(); i++) {
			if (visited[adj[u][i]] == false) {
				visited[adj[u][i]] = true;
				dist[adj[u][i]] = dist[u] + 1;
				pred[adj[u][i]] = u;
				queue.push_back(adj[u][i]);

				if (adj[u][i] == dest)
				return true;
			}
		}
	}

	return false;
}

// utility function to print the shortest distance
// between source vertex and destination vertex
vector<int> printShortestDistance(vector<int> adj[], int s,
									int dest, int v)
{
	vector<int> path;
	// predecessor[i] array stores predecessor of
	// i and distance array stores distance of i
	// from s
	int pred[v], dist[v];

	if (BFS(adj, s, dest, v, pred, dist) == false)
	{
		return path;
	}

	// vector path stores the shortest path

	int crawl = dest;
	path.push_back(crawl);
	while (pred[crawl] != -1) {
		path.push_back(pred[crawl]);
		crawl = pred[crawl];
	}
	return path;

}


//Split function
size_t split(const std::string &txt, std::vector<std::string> &strs, char ch)
{
    size_t pos = txt.find( ch );
    size_t initialPos = 0;
    strs.clear();

    // Decompose statement
    while( pos != std::string::npos ) {
        strs.push_back( txt.substr( initialPos, pos - initialPos ) );
        initialPos = pos + 1;

        pos = txt.find( ch, initialPos );
    }

    // Add the last one
    strs.push_back( txt.substr( initialPos, std::min( pos, txt.size() ) - initialPos + 1 ) );
    return strs.size();
}


int main() {
    // Test code. Replaced with your code
    // read from stdin until EOF
    int vertex = 0;
    vector<int> path;
    while (!std::cin.eof()) {
        // read a line of input until EOL and store in a string
        std::string line;
        std::getline(std::cin, line);

        //Split input with " "
        std::vector<std::string> line_words;
        split(line, line_words, ' ');

        //Vector first element
        if(line_words[0]=="V"){
            //Printing input
            cout<<line<<endl;
            for(int io =1;io <= std::stoi(line_words[1]);io++)
					{	adj[io].clear();
					 }
            vertex = std::stoi(line_words[1]);
            if(vertex<2)
                std::cout<< "Error: The vertex must be greater than 1\n";
        }

        //Edge first element
        //Adjacency list
        //std::vector<int> adj[vertex+1];
        if(line_words[0]=="E"){
            //Printing input
            cout<<line<<endl;
            std::vector<std::string> edge;

            //Get the edges and check
            split(line_words[1], edge, ',');

            for(int i=0; i<edge.size()-1;i+=2){
                //iterate over each element of edge list and extract edges
                //Node 1 of edge
                std::string node1;
                for(char &c : edge[i]){
                    if(isdigit(c))
                        node1+=c;
                }
                //Node 2 of edge
                std::string node2;
                for(char &c : edge[i+1]){
                    if(isdigit(c))
                        node2+=c;
                }
                //Error if Node greater than edge
                if(std::stoi(node1)>vertex || std::stoi(node2)>vertex){
                    std::cout<<"Error: The node cannot have a value greater than V\n";
                    break;
                }

                //Add to adjacency list
                adj[std::stoi(node1)].push_back(std::stoi(node2));
                adj[std::stoi(node2)].push_back(std::stoi(node1));
            }
        }

        //Source and destination Logic
        if(line_words[0]=="s"){
            if(std::stoi(line_words[1])>vertex || std::stoi(line_words[2])>vertex)
                cout<<"Error: Invalid source or destination\n";
            else{
                path = printShortestDistance(adj, std::stoi(line_words[1]), std::stoi(line_words[2]), vertex+1);
                if (path.size() != 0){
                    int i;
                    for (i = path.size() - 1; i >= 0; i--)
                        {
                            if (i == path.size()-1) cout << path[i];
                            else cout << "-" << path[i];
                        }
                            cout << endl;
                }
                else cerr << "Error: Path does not exist"<< endl;
            }
        }
    }
    return 0;
}

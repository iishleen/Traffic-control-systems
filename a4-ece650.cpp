#include <iostream>
#include <sstream>
#include <vector>
#include <regex>
#include <algorithm>
// defined std::unique_ptr
#include <memory>
// defines Var and Lit
#include "minisat/minisat/core/SolverTypes.h"
// defines Solver
#include "minisat/minisat/core/Solver.h"

using namespace std;
                  
class Graph{
public:
    size_t Vert;
    std::vector<unsigned> Edges;
    std::vector<int> *graph;
    // constructor for class
    Graph(int Vert){
        this -> Vert = Vert;
        graph = new std::vector<int> [Vert];
    }
    void EdgesStore(std::vector<unsigned> edges);
    void GraphBuild(); 
    std::vector<int> vertexCover(size_t Vertexcover, std::vector<unsigned> Edges);
};



void Graph::GraphBuild(){
    //loop through vertices and figure out what vert is connected to what
    for(size_t i = 0; i < Edges.size(); i = i + 1){
        if( (i % 2) != 0){
            graph[Edges[i]].push_back(Edges[i-1]);
        }
        else{
            graph[Edges[i]].push_back(Edges[i+1]);
        }
    }
}

void Graph::EdgesStore(std::vector<unsigned> edges){
    Edges = edges;
}

std::vector<int> Graph::vertexCover(size_t Vertexcover, std::vector<unsigned> Edges){
    
    Minisat::Solver solver;

    std::vector<std::vector<Minisat::Lit>> Vertices(Vert);


    for(size_t i = 0; i < Vert; ++i){
        for(size_t j = 0; j < Vertexcover; ++j){
            Minisat::Lit literal = Minisat::mkLit(solver.newVar());
            Vertices[i].push_back(literal);
        }
    }

    // Clause 1
    for(size_t i = 0; i < Vertexcover; ++i){
        Minisat::vec<Minisat::Lit> Literalsn;
        for(size_t j = 0; j < Vert; ++j){
            Literalsn.push(Vertices[j][i]);
        }
        solver.addClause(Literalsn);
        Literalsn.clear();
    }
    // Clause 2
    for(size_t m = 0; m < Vert; ++m){
        for(size_t p = 0; p < (Vertexcover-1); ++p){
            for(size_t q = p+1; q < Vertexcover; ++q){
                solver.addClause(~Vertices[m][p],~Vertices[m][q]);
            }
        }
    }
    // Clause 3
    for(size_t m = 0; m < Vertexcover; ++m){
        for(size_t p = 0; p < (Vert-1); ++p){
            for(size_t q = p+1; q < Vert; ++q){
                solver.addClause(~Vertices[p][m],~Vertices[q][m]);
            }
        }
    }
    // Clause 4
    for(size_t i = 0; i < Edges.size(); i = i + 2){
        Minisat::vec<Minisat::Lit> Literalsn;
        for(size_t k = 0; k < Vertexcover; ++k){
            Literalsn.push(Vertices[Edges[i]][k]);
            Literalsn.push(Vertices[Edges[i+1]][k]);
        }
        solver.addClause(Literalsn);
        Literalsn.clear();
    }
    auto res = solver.solve();
    std::vector<int> cover;

    if(res){
        for(size_t i = 0; i < Vert; ++i){
            for(size_t j = 0; j < Vertexcover; ++j){
                int result = Minisat::toInt(solver.modelValue(Vertices[i][j]));
                if(result == 0){
                    cover.push_back(i);
                }
            }
        }
        return cover;
    }
    else{
        return {0};
    }
}

std::vector<unsigned> FindNumbers(std::string line,std::vector<unsigned> nums){
    int i = 1;
    std::smatch ematch;
    regex E("([0-9]+)");
    while (regex_search(line, ematch, E)) {   
        nums.push_back(std::stoi(ematch.str(0)));
        i++; 
        // suffix to find the rest of the string. 
        line = ematch.suffix().str();    
    }  
    return(nums); 
}


int main() {

    // Variables
    std::string line;
    std::smatch ematch;
    Graph street(0);

    // read from stdin until EOF
    while (!std::cin.eof()) {
        std::vector<unsigned> nums;
        std::vector<int> SP;
        // read a line of input until EOL and store in a string 
        std::getline(std::cin, line);

        // Use regex to detect command characters and numbers
        regex C("^\\w");
        regex E("([0-9]+)");
        regex V("[0-9]+");
        std::smatch cmatch;

        if (regex_search(line,cmatch,C)){

            if (cmatch[0] == 'E'){
                nums = FindNumbers(line,nums);
                if(nums.size()){
                    size_t Vertcomp = street.Vert;
                    if ((street.Vert > 1) && (*std::max_element(std::begin(nums) ,std::end(nums))<Vertcomp)){
                        street.EdgesStore(nums);
                      
                        street.GraphBuild();
                        std::vector<int> Cover;
                        size_t i = 1;
                        while(i < street.Vert){
                            Cover = street.vertexCover(i,street.Edges);
                            if(Cover[0] == -1){
                                i = i + 1;
                                continue;
                            }
                            else{
                                break;
                            }
                        }
                        sort(Cover.begin(),Cover.end());
                        for(size_t i = 0; i < Cover.size(); ++i){
                            std::cout << Cover[i] << " ";
                        }
                        std::cout << std::endl;
                    }
                    else if(street.Vert == 1){
                        continue;
                    }
                    else{
                        std::cerr << "Error: Not enough vertices to compute edges" << std::endl;
                    }
                }
                else{
                    std::vector<unsigned> zero;
                    street.EdgesStore(zero);
                    std::cout << std::endl;
                }
            }
            else if (cmatch[0] == 'V'){
                nums = FindNumbers(line,nums);
                if(nums[0]>0){
                    street = Graph(nums[0]);
                }
                else{
                    std::cerr << "Error: Need to enter at least 1 Vertice" << std::endl;
                }
            }
            else{
                std::cerr << "Error: No command match" << std::endl;
            }
        }
        else{
            continue;
        }
    }
    return 0;
}

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
    sizet Vertices;
    std::vector<unsigned> Edges;
    std::vector<int> *graph;
    // constructor for class
    Graph(int Vertices){
        this -> Vertices = Vertices;
        graph = new std::vector<int> [Vertices];
    }
 //Declaring the other functions
    void EdgesStore(std::vector<unsigned> edges);
    void GraphBuild(); 
    std::vector<int> vertexCover(sizeOf Vcover, std::vector<unsigned> Edges);
};


void Graph::GraphBuild(){
        for(size_t i = 0; i < Edges.size(); i = i + 1){
        if( (i % 2) != 0){
            graph[Edges[i]].push_back(Edges[i-1]);
        }
        else {
            graph[Edges[i]].push_back(Edges[i+1]);
        }
    }
}

void Graph::EdgesStore(std::vector<unsigned> edges){
    Edges = edges;
}

std::vector<int> Graph::vertexCover(sizeOf Vcover, std::vector<unsigned> Edges){
       Minisat::Solver solver;

    std::vector<std::vector<Minisat::Lit>> Vertices(Vert);
    for(sizeOf i = 0; i < Vert; ++i){
        for(sizeOf j = 0; j < Vcover; ++j){
            Minisat::Lit literal = Minisat::mkLit(solver.newVar());
            Vertices[i].push_back(literal);
        }
    }

//Clause 1
for(sizeOf i = 0; i < Vcover; ++i){
        Minisat::vec<Minisat::Lit> Literals;
        for(sizeOf j = 0; j < Vert; ++j){
            Literals.push(Vertices[j][i]);
        }
        solver.addClause(Literals);
        Literals.clear();
    }

//Clause 2

for(sizeOf m = 0; m < Vert; ++m){
        for(sizeOf p = 0; p < (Vcover-1); ++p){
            for(sizeOft q = p+1; q < Vcover; ++q){
                solver.addClause(~Vertices[m][p],~Vertices[m][q]);
            }
        }
    }

//Clause 3

 for(sizeOf m = 0; m < Vcover; ++m){
        for(sizeOf p = 0; p < (Vert-1); ++p){
            for(sizeOf q = p+1; q < Vert; ++q){
                solver.addClause(~Vertices[p][m],~Vertices[q][m]);
            }
        }
    }


//Clause 4

 for(sizeOf i = 0; i < Edges.size(); i = i + 2){
        Minisat::vec<Minisat::Lit> Literals;
        for(sizeOf k = 0; k < Vcover; ++k){
            Literals.push(Vertices[Edges[i]][k]);
            Literals.push(Vertices[Edges[i+1]][k]);
        }
        solver.addClause(Literals);
        Literals.clear();
    }

    auto res = solver.solve();
    std::vector<int> cover;

    if(res){
        for(sizeOf i = 0; i < Vert; ++i){
            for(sizeOf j = 0; j < Vcover; ++j){
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

std::vector<unsigned> FindNumber(std::string line,std::vector<unsigned> nums){
    int i = 1;
    std::match_s match_e;
    regex E("([0-9]+)");
    while (regex_search(line, match_e, E)) {   
        nums.push_back(std::stoi(match_e.str(0)));
        i++; 
        // suffix to find the rest of the string. 
        line = match_e.suffix().str();    
    }  
    return(nums); 
}

int main() {

    // Variables
    std::string line;
    std::match_s match_e;
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
        std::match_e match_c;

        if (regex_search(line,match_c,C)){

            // Depending on command character, do different regex extractions
            if (match_c[0] == 'E'){
                nums = FindNumber(line,nums);
                if(nums.size()){
                    sizeOf Vertcomp = street.Vert;
                    if ((street.Vert > 1) && (*std::max_element(std::begin(nums) ,std::end(nums))<Vertcomp)){
                        street.EdgesStore(nums);
                        // Build connected vertice graph (adjacent nodes)
                        street.GraphBuild();
                        std::vector<int> Cover;
                        sizeOf i = 1;
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
            else if (match_c[0] == 'V'){
                nums = FindNumber(line,nums);
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


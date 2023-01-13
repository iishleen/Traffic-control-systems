#include <iostream>
#include <unistd.h>
#include <vector>
#include <signal.h>
#include <sys/wait.h>

int procCin(void) {

    while (!std::cin.eof()) {
        // read a line of input until EOL and store in a string
        std::string line;
        std::getline(std::cin, line);
        std::cout << line << std::endl;
    }
    return 0;
}


int main (int argc, char **argv) {
    pid_t kid1,kid2,kid3;

    //generate pipe
    int RtoA[2];
    int A1BtoA2[2];
    pipe(RtoA);
    pipe(A1BtoA2);
    pid_t child_pid;

    child_pid = fork();
    if(child_pid == 0)
    {
        
        dup2(RtoA[1], STDOUT_FILENO);
        close(RtoA[0]);
        close(RtoA[1]);

        int rgen = execv("rgen",argv);
        return rgen;
    }

    kid1 = child_pid;
    
    child_pid = fork();
    if(child_pid == 0)
    {
        dup2(RtoA[0], STDIN_FILENO);
        close(RtoA[0]);
        close(RtoA[1]);

        dup2(A1BtoA2[1], STDOUT_FILENO);
        close(A1BtoA2[0]);
        close(A1BtoA2[1]);

        char *argv1[3];

        argv1[0] = (char *)"python3";// it is just a program name
        argv1[1] = (char *)"ece650-a1.py";
        argv1[2] = 0;

        return execvp("python3", argv1);
    }
    kid2 = child_pid;

    //conncet a1 to a2
    child_pid = fork();
    if(child_pid == 0)
    {
        
        
       dup2(A1BtoA2[0], STDIN_FILENO);
       close(A1BtoA2[0]);
       close(A1BtoA2[1]);
  
        int a2 = execv("ece650-a2",argv);
        return a2;
    }
    kid3 = child_pid;


        dup2(A1BtoA2[1], STDOUT_FILENO);
        close(A1BtoA2[1]);
        int res = procCin();



    // send kill signal to all children
        int status;
        kill(kid1, SIGTERM);
        waitpid(kid1, &status, 0);

        kill(kid2, SIGTERM);
        waitpid(kid2, &status, 0);

        kill(kid3, SIGTERM);
        waitpid(kid3, &status, 0);




return res;
    
}
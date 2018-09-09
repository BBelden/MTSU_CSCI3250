// project 1
// due 14:00:00, September 15, 2014

#include <string>
#include <iostream>
#include <fstream>
#include "stdlib.h"

int main(int argc, const char * argv[])
{
    const int ROWS = 50;
    const int COLS = 3;
    std::string symbolTable[ROWS][COLS];
    int ttlSymbls = 0;
    int locCtr = 0;  // location counter
    int temp;
    char op;
    std::ifstream inFile;
    inFile.open(argv[1]);
    std::string line;
    getline(inFile,line);
    std::string type;
    //std::cout << line;
    while (inFile)
    {
        // clean up the input line by removing any trailing 
        // comments and/or whitespace
        if (line.find('#') != std::string::npos)
        {
            line = line.substr(0,line.find('#'));
        }
        while (line[line.length()-1] == ' ' ||
                line[line.length()-1] == '\n' ||
                line[line.length()-1] == '\t')
        {
            line = line.substr(0,line.length()-2);
        }
        std::cout << line << std::endl;
       
        // break up the line into an array of strings
        std::string lineArray [3] = "";
        std::string brkLn = line;
        // if first column is blank
        if (brkLn[0] == ' ')
        {
            lineArray[0] = "";
            brkLn = brkLn.substr(brkLn.find_first_not_of(' '));
        }
        else
        {
            lineArray[0] = brkLn.substr(0,brkLn.find(' '));
            brkLn = brkLn.substr(brkLn.find(' '));
            brkLn = brkLn.substr(brkLn.find_first_not_of(' '));
        }
        // if third column is blank
        if (brkLn.find(' ') == std::string::npos)
        {
            lineArray[1] = brkLn;
            lineArray[2] = "";
        }
        else
        {
            lineArray[1] = brkLn.substr(0,brkLn.find(' '));
            brkLn = brkLn.substr(brkLn.find(' '));
            brkLn = brkLn.substr(brkLn.find_first_not_of(' '));
            lineArray[2] = brkLn; 
        }
        //std::cout << lineArray[0]<<lineArray[1]<<lineArray[2]<<std::endl;

        if (lineArray[1] == "EQU")
        {
            std::string op1,op2;
            int iOp1, iOp2;
            if ( lineArray[2].find('+') == std::string::npos &&
                 lineArray[2].find('-') == std::string::npos)
            {
                temp = locCtr;
                locCtr = atoi(lineArray[2].c_str());
            }
            else if (lineArray[2].find('+') != std::string::npos)
            {
                op1 = lineArray[2].substr(0,lineArray[2].find('+'));
                op2 = lineArray[2].substr(lineArray[2].find('+')+1);
                std::cout << "op1= " << op1 << "\top2= " << op2 << std::endl;
                op = '+';
            }
            else if (lineArray[2].find('-') != std::string::npos)
            {
                op1 = lineArray[2].substr(0,lineArray[2].find('-'));
                op2 = lineArray[2].substr(lineArray[2].find('-')+1);
                std::cout << "op1= " << op1 << "\top2= " << op2 << std::endl;
                op = '-';
            }
                
            if (isdigit(op1[0]))
            {    
                iOp1 = atoi(op1.c_str());
                op1 = "int";
            }
            else 
                iOp1 = 0;
            if (isdigit(op2[0]))
            {
                iOp2 = atoi(op2.c_str());
                op2 = "int";
            }
            else 
                iOp2=0;

            temp = locCtr;
           
            type = "abs";
            locCtr = atoi(lineArray[2].c_str());
        }     
        
        // output label and location counter
        if (lineArray[0] != "")
        {
            std::cout << lineArray[0] << "\t" << locCtr << "\t"<<type<<"\n";
        }
        
        
        getline(inFile,line);
    }
    return 0;
}

#include <iostream> 
#include <fstream> 
using namespace std; 


struct Trade //size-fixed structure
{
    uint64_t timestamp;
    uint64_t index;
    bool buy;
    char padding[7];
};


int main() { 
    // open and read file binary
    fstream file;
    file.open("output.dat", ios::in | ios::binary);
    
    // output content of file
    Trade trade;
    while(!file.eof()){
        file.read((char*)&trade, sizeof(trade));
        cout << trade.timestamp << '\t' << trade.index << '\t' << (trade.buy ? "BUY" : "SELL") << endl ;
    }
    file.close();
    
    return 0; 
}
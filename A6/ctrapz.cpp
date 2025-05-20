#include <bits/stdc++.h>

using namespace std;

double f(double x){
    return x*x;
}

int main(){

    double a=0; 
    double b=2;
    int n=100000000;
    double x;

    double area = 0, dx = (b-a)/(n-1);
    cout << dx << endl;

    auto start = chrono::high_resolution_clock::now();
    for(int i=0;i<n-1;i++){
        x = a+i*dx;
        area += (f(x)+f(x+dx))*dx/2;
    }

    auto stop = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(stop - start);

    cout << setprecision(17)<< area << endl;

    cout << "time taken : " <<duration.count() << "ms" << endl;

    return 0;
}
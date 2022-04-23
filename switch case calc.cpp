#include<iostream>
 using namespace std;

int main(){
    
    float a, b;
    char op;
    
    cout<<"input a number: "<<endl;
    cin>>a;
    
    cout<<"input operator: "<<endl;
    cin>>op;
    
    cout<<"input another number: "<<endl;
    cin>>b;
    
    switch(op) {
        
        case'+':
            cout<<a<<" + "<<b<<" = "<<a+b<<endl; 
            break;
         
        case'-' :
           cout<<a<<" – "<<b<<" = "<<a-b<<endl;
           break;
        
        case'*':
            cout<<a<<" × "<<b<<" = "<<a*b<<endl; 
            break;        
       
        case'/':
            cout<<a<<" ÷ "<<b<<" = "<<a/b<<endl; 
            break;
      }
    return 0;
    }
    
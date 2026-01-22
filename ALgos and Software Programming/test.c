#include <stdio.h>
#include <stdbool.h>

void swap(int a,int b){
    int temp=a;
    a=b;
    b=temp;
    printf("a: %d",a);
    printf("\n");
    printf("b: %d",b);
}

int sumn(int n){
    int sum=0;
    for (int i=1;i<=n;i++){
        sum+=i;
    }
    return sum;
}

int fact(int n){
    int f=1;
    for (int i=1;i<=n;i++){
        f*=i;
    }
    return f;
}

void divide(int n){
    while(n>5){
        printf("\n %d",n);
        n/=2;
    }
}

void evenOdd(int n){
    if(n%2==0)
        printf("\n Number is even");
    else
        printf("\n Number is odd");
}

void checkPrime(int n){
    bool flag=true;
    for (int i=2;i<=n/2;i++){
        if (n%i==0){
            flag=false;
            printf("Number is not prime");
            return;
        }
        else
            continue;
    }
    if(flag)
        printf("Number is prime");
}

bool checkPalindrome(char s[]){
    int n=strlen(s);

    for(int i=0;i<=n/2;i++){
        if(s[i]!=s[n-i-1])
            return false;
    }
    return true;
}

int main() {
    // printf() displays the string inside the quotation marks
    
    // int a=10,b=20;
    // swap(a,b);

    //print sum of n natural numbers
    int n;
    // printf("Enter the value of n: ");
    // scanf("%d",&n);
    // int sum=sumn(n);
    // printf("\n The sum is: %d",sum);
    // int factorial=fact(n);
    // printf("\n The factorial is: %d",factorial);

    //int div till <=5
    // divide(n);
    // evenOdd(n);
    // checkPrime(n);
    bool res=checkPalindrome("madam");
    printf("%d",res);
    return 0;
}

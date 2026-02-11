#include <iostream>
#include<ctime>
using namespace std;
int main(){
    int n;
    cin >> n;
    int arr[n];
    //sorted input
    for (int i = 0; i < n;i++){
        arr[i] = i;
    }
    // //sorted in reversed order
    // for (int i = 0; i < n;i++){
    //     arr[i] = n - i - 1;
    // }
    // //random input
    // srand(time(0));
    // for (int i = 0; i < n;i++){
    //     arr[i] = rand() % 100;
    // }
     for (int i = 0; i < n;i++){
        cout << arr[i] << " ";
    }
    //insertion sort

    int cnt = 0;
    int swap_cnt = 0;
    for (int i = 0; i < n-1;i++){
        int min = i;
        for (int j = i + 1; j < n;j++){
            if( cnt++ && arr[j]<arr[min]){
                min = j;
            }
        }
        swap(arr[min], arr[i]);
        swap_cnt++;
    }
    cout << endl;
    for (int i = 0; i < n;i++){
        cout << arr[i] << " ";
    }
    cout << endl<< "No of total Comparisons:"<< cnt << endl<<"No of swaps:" << swap_cnt << " ";
}
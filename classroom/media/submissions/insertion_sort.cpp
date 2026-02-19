#include <iostream>
#include<ctime>
using namespace std;
int main(){
    int n;
    cin >> n;
    int arr[n];
    // //sorted input
    // for (int i = 0; i < n;i++){
    //     arr[i] = i;
    // }
    // //sorted in reversed order
    // for (int i = 0; i < n;i++){
    //     arr[i] = n - i - 1;
    // }
    for (int i = 0; i < n;i++){
        cin >> arr[i];
    }
        // //random input
        // srand(time(0));
        // for (int i = 0; i < n;i++){
        //     arr[i] = rand() % 100;
        // }
        // insertion sort
        int cnt = 0;
    int shift_cnt = 0;
    for (int j = 1; j < n;j++){
        int key = arr[j];
        int i = j - 1;
        while (i >= 0 && ++cnt && arr[i]>key){
            arr[i + 1] = arr[i];
            shift_cnt++;
            i--;
        }
        arr[i + 1] = key;
    }
    for (int i = 0; i < n;i++){
        cout << arr[i] << " ";
    }
    cout << endl<< "No of total Comparisons:"<< cnt << endl<<"No of shifts:" << shift_cnt << " ";

    return 0;
}
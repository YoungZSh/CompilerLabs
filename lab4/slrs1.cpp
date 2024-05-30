#include <iostream>
#include <stack>
#include <string>
#include <cstdlib>

using namespace std;

string action[11][4] = {"S1", "0", "0", "0",
                        "r3", "r3", "0", "0",
                        "0", "0", "0", "acc",
                        "S4", "S5", "0", "0",
                        "r2", "r2", "0", "0", 
                        "0", "r5", "r5", "0", 
                        "0", "S7", "S8", "0",
                        "0", "r4", "r4", "0",
                        "0", "0", "r7", "r7", 
                        "0", "0", "S10", "r1",
                        "0", "0", "r6", "r6"};
int gotoarr[11][4] = {2, 3, 0, 0, // GOTO 表
                      0, 0, 0, 0,
                      0, 0, 0, 0,
                      0, 0, 6, 0,
                      0, 0, 0, 0,
                      0, 0, 0, 0,
                      0, 0, 0, 9,
                      0, 0, 0, 0,
                      0, 0, 0, 0,
                      0, 0, 0, 0,
                      0, 0, 0, 0};
char vt[4] = {'a', 'b', 'c', '#'};                                   // 存放终结符
char vn[4] = {'S', 'A', 'B', 'C'};                                                  // 存放非终结符
string Production[7] = {"S->ABC","A->Aa","A->a","B->Bb","B->b","C->Cc","C->c"}; // 产生式集合
int com = 0;
int line = 1; // 记录处理的步骤数
bool flag = false;
int StatusNumber = 1;     // 栈中状态数
string StackString = "#"; // 记录符号栈中内容
int Status[50] = {0};     // 记录状态栈
stack<char> Stack;        // 创建一个符号栈
stack<int> status;        // 创建一个状态栈
void Judge(int &i, int j, const char arr[], char ch, string s)
{ // 判断输入串是否由文法终结符组成
    flag = false;
    for (int l = 0; l < j; l++)
    {
        if (ch == arr[l])
        {
            flag = true;
            i = l;
            break;
        }
    }
    if (!flag)
    {
        cout << "\tError" << endl;
        com = s.size();
    }
}

void OutputStatus()
{ // 输出状态集
    for (int i = 0; i < StatusNumber; i++)
        cout << Status[i];
}

void OutputString(string s)
{ // 输出未处理的字符串
    for (int i = com; i < s.size(); i++)
        cout << s.at(i);
}

void Output(string s)
{ // 输出步骤、 状态集、 符号集、 输入串
    cout << line << "\t";// 输出步骤数
    OutputStatus();
    cout << "\t" << StackString << "\t";
    OutputString(s);
    cout << "\t\t";
    line++;
}

void Shift(int i, string s)
{ // 移进函数 S
    Output(s);
    cout << "ACTION[" << status.top() << "," << s.at(com) << "]=S" << i << ",状态" << i << "入栈" << endl;
    status.push(i);                        // 将状态 i 压进状态
    Status[StatusNumber] = i;              // Status 记录状态栈的内容
    Stack.push(s.at(com));                 // 将当前面临的输入串符号压进符号栈
    StackString = StackString + s.at(com); // StackString 记录符号栈的内容
    com++;                                 // 当前面临的输入串字符往后移一位
    StatusNumber++;                        // 状态数加一
}

void Goto(stack<int> st1, stack<char> st2, string s)
{ // GoTo 语句
    int j = -1;
    int ch1 = st1.top();
    char ch2 = st2.top();
    Judge(j, 4, vn, ch2, s); // 求得 ch2 在非终结符表中的位置
    if (gotoarr[ch1][j] == 0)
    {
        cout << "\tError" << endl;
        com = s.size();
    }
    else
    {
        status.push(gotoarr[ch1][j]); // 新状态进栈
        Status[StatusNumber] = gotoarr[ch1][j];
        StatusNumber++;
    }
}

void Reduction(int i, string s)
{ // 归约函数 R
    Output(s);
    cout << "r" << i << ":" << Production[i - 1] << "归约， GoTo(";
    int N = Production[i - 1].length() - 3;
    for (int j = 0; j < N; j++)
    { // 消除要归约的状态及符号
        status.pop();
        Stack.pop();
        StatusNumber--;
        StackString.erase(StackString.length() - 1);
    }
    cout << status.top() << "," << Production[i - 1].at(0) << ")=";
    Stack.push(Production[i - 1].at(0)); // 符号进栈
    StackString = StackString + Stack.top();
    Goto(status, Stack, s);
    cout << status.top() << "入栈" << endl;
    Status[StatusNumber] = status.top();
}

void Analyse(string s)
{                    // 具体分析函数
    Stack.push('#'); // 初始化
    status.push(0);
    s = s + "#";
    int t = -1; // 记录 ch 在数组 vt 的位置
    while (com < s.size())
    {
        int i = status.top();
        char ch = s.at(com);
        Judge(t, 4, vt, ch, s);
        if (flag)
        {
            if (action[i][t] != "acc" && action[i][t] != "0")
            {
                if (action[i][t].at(0) == 'S')
                {
                    action[i][t].erase(0, 1);             // 删除 action[i][t]的首字母 S
                    Shift(atoi(action[i][t].c_str()), s); // atoi(action[i][t].c_str())， 将action[i][t]转换为整型
                    action[i][t].insert(0, "S");          // 将 S 添加回 action[i][t]
                }
                else if (action[i][t].at(0) == 'r')
                {
                    action[i][t].erase(0, 1);                 // 删除 action[i][t]的首字母 r
                    Reduction(atoi(action[i][t].c_str()), s); // atoi(action[i][t].c_str())， 将action[i][t]转换为整型
                    action[i][t].insert(0, "r");              // 将 r 添加回 action[i][t]
                }
            }
            else if (action[i][t] == "0")
            {
                cout << "\tError" << endl;
                break;
            }
            else if (action[i][t] == "acc")
            {
                Output(s);
                cout << "acc" << "\t 分析成功" << endl;
                break;
            }
        }
        else if (!flag)
            break;
    }
}

int main()
{
    string s;
    cout << "输入的文法" << endl;
    for (int j = 0; j < 6; j++)
        cout << Production[j] << endl;
    cout << "VT:" << endl;
    for (int i = 0; i < 6; i++)
        cout << vt[i] << " ";
    cout << endl;
    cout << "VN:" << endl;
    for (int i = 0; i < 3; i++)
        cout << vn[i] << " ";
    cout << endl;
    cout << "****************************LR(1)****************************" << endl;
    char T;
    cout << "Enter String" << endl;
    cin >> s;
    //s="aabcc";
    cout << "**************************Analyzer***************************" << endl;
    cout << "Step" << "\t" << "StateStack" << "\t" << "SymbolStack" << "\t" << "RemainingString" << "\t" << "Info"
         << endl;
    Analyse(s);
    com = 0;
    line = 1;
    StackString = "#";
    StatusNumber = 1;
    while (!Stack.empty())
        Stack.pop();
    while (!status.empty())
        status.pop();
    return 0;
}
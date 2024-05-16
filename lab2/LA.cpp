#include <iostream>
#include <string>
#include <cstring>
#include <fstream>

using namespace std;

const string keywords[] = {"main", "int", "char", "if", "else", "for", "while", "return", "void", "ID", "INT"};

string input;
int token_code;
string token_value;

int i = 0;

int flag;

bool is_letter(char ch)
{
    if ((ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z'))
    {
        return true;
    }
    else
    {
        return false;
    }
}

bool is_digit(char ch)
{
    if (ch >= '0' && ch <= '9')
    {
        return true;
    }
    else
    {
        return false;
    }
}

string delete_comment(string str)
{
    size_t pos;
    bool in_comment = false;
    while ((pos = str.find("/*")) != string::npos)
    {
        size_t end_pos = str.find("*/");
        if (end_pos != string::npos)
        {
            str.erase(pos, end_pos - pos + 2);
        }
        else
        {
            in_comment = true;
            str.erase(pos);
            break;
        }
    }

    if (in_comment)
    {
        size_t end_pos = str.find("*/");
        if (end_pos != string::npos)
        {
            in_comment = false;
            str.erase(0, end_pos + 2);
        }
        else
        {
            str = "";
        }
    }

    while ((pos = str.find("//")) != string::npos)
    {
        size_t end_pos = str.find("\n", pos);
        if (end_pos != string::npos)
        {
            str.erase(pos, end_pos - pos);
        }
        else
        {
            str.erase(pos);
            break;
        }
    }

    return str;
}

void scan(string str)
{
    if (str[i] == ' ')
    {
        i++;
        token_code = -2;
        return;
    }

    token_value = "";

    if (is_digit(str[i]))
    {
        int num = 0;
        while (is_digit(str[i]))
        {
            num = num * 10 + (str[i] - '0');
            i++;
        }
        token_value = to_string(num);
        token_code = 20;
    }
    else if (is_letter(str[i]) || str[i] == '_')
    {
        while ((is_letter(str[i]) || is_digit(str[i])) || str[i] == '_')
        {
            token_value += str[i];
            i++;
        }
        token_code = 10;
        for (int j = 0; j < 11; j++)
        {
            if (token_value == keywords[j])
            {
                token_code = j + 1;
                break;
            }
        }
    }
    else
    {
        switch (str[i])
        {
        case '=':
            token_code = 21;
            i++;
            token_value = "=";
            if (str[i] == '=')
            {
                token_code = 39;
                i++;
                token_value = "==";
            }
            break;
        case '+':
            token_code = 22;
            i++;
            token_value = "+";
            break;
        case '-':
            token_code = 23;
            i++;
            token_value = "-";
            break;
        case '*':
            token_code = 24;
            i++;
            token_value = "*";
            break;
        case '/':
            token_code = 25;
            i++;
            token_value = "/";
            break;
        case '(':
            token_code = 26;
            i++;
            token_value = "(";
            break;
        case ')':
            token_code = 27;
            i++;
            token_value = ")";
            break;
        case '[':
            token_code = 28;
            i++;
            token_value = "[";
            break;
        case ']':
            token_code = 29;
            i++;
            token_value = "]";
            break;
        case '{':
            token_code = 30;
            i++;
            token_value = "{";
            break;
        case '}':
            token_code = 31;
            i++;
            token_value = "}";
            break;
        case ',':
            token_code = 32;
            i++;
            token_value = ",";
            break;
        case ':':
            token_code = 33;
            i++;
            token_value = ":";
            break;
        case ';':
            token_code = 34;
            i++;
            token_value = ";";
            break;
        case '>':
            token_code = 35;
            i++;
            token_value = ">";
            if (str[i] == '=')
            {
                token_code = 37;
                i++;
                token_value = ">=";
            }
            break;
        case '<':
            token_code = 36;
            i++;
            token_value = "<";
            if (str[i] == '=')
            {
                token_code = 38;
                i++;
                token_value = "<=";
            }
            break;
        case '!':
            token_code = -1;
            i++;
            if (str[i] == '=')
            {
                token_code = 40;
                i++;
                token_value = "!=";
            }
            break;
        case '"':
            token_code = -1;
            i++;
            flag = 1;
            while (str[i] != '"')
            {
                if (str[i] == '#')
                {
                    flag = 0;
                    break;
                }
                else
                {
                    token_value += str[i];
                    i++;
                }
            }
            if (flag == 1)
            {
                i++;
                token_code = 50;
            }
            else
            {
                token_code = -1;
                cout << "Error: Unterminated string constant" << endl;
            }
            break;
        case '#':
            token_code = 0;
            cout << "Lexical Analyzer: End of file reached" << endl;
            break;
        default:
            token_code = -1;
            i++;
            break;
        }
    }
}

int main()
{
    string line;
    ifstream code_file("input.txt");
    if (code_file.is_open())
    {
        while (getline(code_file, line))
        {
            input += delete_comment(line);
        }
        code_file.close();
        cout << "Input code(after deleting comments): " << endl;
        cout << input << endl;
        cout << "Lexical Analyze result:" << endl;
        input += "#";
        do
        {
            scan(input);
            switch (token_code)
            {
            case -1:
                cout << "Lexical Analyzer: Invalid character found" << endl;
                break;
            case -2:
                break;
            default:
                if (token_code != 0)
                {
                    cout << "(" << token_code << "," << token_value << ")" << endl;
                }
                break;
            }
        } while (token_code != 0 && i < input.length());
    }
    else
    {
        cout << "Error: File not found" << endl;
    }
    return 0;
}
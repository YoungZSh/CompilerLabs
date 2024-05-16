flex calculator.l
bison -d parser.y
gcc lex.yy.c parser.tab.c -o calculator -lm
# echo "3.3 + (5 - 2) * 4" | ./calculator
# 读取input.txt文件中的每一行
# while IFS= read -r line
# do
#     # 将每行作为输入传递给计算器命令
#     echo "$line" | ./calculator
# done < input.txt
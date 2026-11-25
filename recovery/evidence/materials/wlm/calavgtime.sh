#!/bin/bash

# 用法：./extract_nonzero.sh 源文件路径 新文件路径
if [ $# -ne 1 ]; then
    echo "请传入 源文件路径！示例：./extract_nonzero.sh input.txt"
    exit 1
fi

src_file=$1
dest_file=$2

# 核心逻辑：提取所有非0数字（整数/小数/正负），一行一个写入新文件
result=$(grep -oE '[+-]?[0-9]+\.?[0-9]*|[0-9]*\.[0-9]+|[0-9]+)' "$src_file" | 
	sed '/^[0]*\(\.[0]*\)*$/d' | awk '{sum+=$1; count++} END{if(count>0) print "trt:" sum/count; else print "没有非0数字可计算平均响应时间"}') 
#sort -n > "$dest_file" # 可选：按数字大小排序（注释此行则保留原顺序）

echo "$result"
#echo "提取完成！非0数字已写入 $dest_file（共 $(wc -l < "$dest_file") 个）"

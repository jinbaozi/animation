#!/bin/bash



# 检查是否提供了文件路径作为参数

if [ "$#" -ne 1 ]; then

    echo "Usage: $0 <log_file_path>"

    exit 1

fi



log_file="$1"



# 使用 sed 命令转换换行符从 CRLF 到 LF

sed -i 's/\r$//' "$log_file"



# 初始化变量

total_seconds=0

first_seconds=0

total_data=0



# 读取文件中的每一行

while read -r line; do

  # 使用IFS（内部字段分隔符）来分隔时间和数据

  IFS=$'\t' read -r time data <<< "$line"



  # 将时间字符串转换为秒

  current_seconds=$(date -u -d "$time" +%s)



  # 如果是第一行，则记录时间

  if [ $first_seconds -eq 0 ]; then

    first_seconds=$current_seconds

  fi



  # 计算时间差（以秒为单位）

  time_diff=$((current_seconds - first_seconds))



  # 累加时间差到总秒数

  total_seconds=$((total_seconds + time_diff))



  # 累加数据列的值

  total_data=$(echo "$total_data + $data" | bc)



  # 更新 last_seconds 为当前秒数

  last_seconds=$current_seconds

done < "$log_file"



# 计算时间差（秒）

total_time_seconds=$((last_seconds - first_seconds + 1))



# 计算平均值

if [ $total_time_seconds -ne 0 ]; then

  average=$(echo "scale=2; $total_data / $total_time_seconds" | bc)

else

  average=0

fi



# 输出结果

echo "tps:$average"



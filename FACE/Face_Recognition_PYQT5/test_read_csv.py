import csv

# 读取csv文件方式1
csvFile = open("ordinary.csv", "r")
reader = csv.reader(csvFile)  # 返回的是迭代类型
data = []
for item in reader:
    print(item)
    data.append(item)
print(data)
csvFile.close()
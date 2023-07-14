def split_list(lst, num_chunks):
    chunk_size = len(lst) // num_chunks  # 每个部分的大小

    # 使用切片操作将列表分割成多个部分
    chunks = [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

    # 处理余下的元素
    remainder = len(lst) % num_chunks
    for i in range(remainder):
        chunks[i].append(lst[num_chunks * chunk_size + i])

    return chunks

# 示例数据
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

# 分为10份
result = split_list(my_list, 10)

# 输出结果
for i, chunk in enumerate(result):
    print(f"Chunk {i + 1}: {chunk}")
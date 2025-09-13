def process_ip_addresses(input_file, output_file):
    # 存储处理后的IP地址，使用集合自动去重
    unique_ips = set()

    try:
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                # 去除每行首尾的空白字符
                ip = line.strip()

                # 跳过空行
                if not ip:
                    continue

                # 剔除包含冒号的IPv6地址
                if ':' not in ip:
                    unique_ips.add(ip)

        # 将处理后的IP写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            # 按顺序写入（虽然集合是无序的，但这里只是为了保持一致性）
            for ip in sorted(unique_ips):
                f.write(ip + '\n')

        print(f"处理完成！共处理{len(unique_ips)}个唯一的IPv4地址，已保存到{output_file}")

    except FileNotFoundError:
        print(f"错误：找不到文件 {input_file}")
    except Exception as e:
        print(f"处理过程中发生错误：{str(e)}")


if __name__ == "__main__":
    # 输入文件和输出文件的文件名
    input_filename = "ips.txt"
    output_filename = "ips_only.txt"

    # 调用处理函数
    process_ip_addresses(input_filename, output_filename)

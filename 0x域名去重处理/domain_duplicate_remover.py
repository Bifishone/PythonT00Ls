import sys
import os


def process_domains(input_file_path):
    try:
        # 检查输入文件是否存在
        if not os.path.exists(input_file_path):
            print(f"错误：文件 '{input_file_path}' 不存在")
            return

        # 读取文件内容
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 输出原文件内容
        print(f"文件 '{input_file_path}' 的内容如下：")
        print("----------------------------------------")
        print(content)
        print("----------------------------------------\n")

        # 提取域名并去重
        domains = content.splitlines()
        # 过滤空行并去重
        unique_domains = list({domain.strip() for domain in domains if domain.strip()})
        unique_domains.sort()  # 排序，保持结果一致性

        # 输出去重后的域名数量
        print(f"去重前域名数量：{len([d for d in domains if d.strip()])}")
        print(f"去重后域名数量：{len(unique_domains)}\n")

        # 写入结果文件
        output_file = "SubDomainsResult.txt"
        with open(output_file, 'w', encoding='utf-8') as file:
            for domain in unique_domains:
                file.write(domain + '\n')

        print(f"处理完成！去重后的域名已保存到 {os.path.abspath(output_file)}")

    except Exception as e:
        print(f"处理过程中发生错误：{str(e)}")


if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("用法：python domain_duplicate_remover.py <输入文件路径>")
        print("示例：python domain_duplicate_remover.py domains.txt")
        sys.exit(1)

    input_file_path = sys.argv[1]
    process_domains(input_file_path)

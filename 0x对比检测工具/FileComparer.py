import argparse
from colorama import Fore, Style, init
from collections import Counter


def read_file(file_path):
    """读取文件内容并返回行的集合、有序列表、计数器和行数统计"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取所有行，保留原始行（包括空行）
            all_lines = [line.strip() for line in file]
            # 过滤空行的内容行
            content_lines = [line for line in all_lines if line]

            # 统计每行出现的次数
            line_counter = Counter(content_lines)

            total_lines = len(all_lines)  # 包括空行的总行数
            content_count = len(content_lines)  # 实际内容行数（去空行）

            return (set(content_lines), content_lines, line_counter,
                    total_lines, content_count)
    except FileNotFoundError:
        print(f"{Fore.RED}错误: 文件 '{file_path}' 不存在{Style.RESET_ALL}")
        return None, None, None, 0, 0
    except Exception as e:
        print(f"{Fore.RED}读取文件 '{file_path}' 时出错: {str(e)}{Style.RESET_ALL}")
        return None, None, None, 0, 0


def find_differences(file1_lines, file1_counter, file2_lines, file2_counter):
    """找出两个文件之间的所有差异，包括内容和重复次数"""
    # 所有出现过的行
    all_lines = set(file1_counter.keys()).union(set(file2_counter.keys()))

    # 内容差异（只在一个文件中出现的行）
    only_in_file1 = []
    only_in_file2 = []

    # 重复次数差异（两行都有但出现次数不同）
    count_diff = []

    for line in all_lines:
        count1 = file1_counter.get(line, 0)
        count2 = file2_counter.get(line, 0)

        if count1 > 0 and count2 == 0:
            # 只在file1中出现的行
            only_in_file1.extend([line] * count1)
        elif count2 > 0 and count1 == 0:
            # 只在file2中出现的行
            only_in_file2.extend([line] * count2)
        elif count1 != count2:
            # 两行都有但出现次数不同
            count_diff.append((line, count1, count2))

    # 按原文件顺序排列仅在file1中出现的行
    ordered_only_in_file1 = [line for line in file1_lines if line in set(only_in_file1)]

    # 按原文件顺序排列仅在file2中出现的行
    ordered_only_in_file2 = [line for line in file2_lines if line in set(only_in_file2)]

    return ordered_only_in_file1, ordered_only_in_file2, count_diff


def print_differences(file1_path, file2_path, diff1, diff2, count_diff,
                      file1_total, file2_total, file1_content, file2_content):
    """打印差异，包括文件大小比较和多出的内容"""
    init(autoreset=True)

    print(f"\n{Fore.CYAN}📊 文件基本信息:{Style.RESET_ALL}")
    print("─" * 80)
    print(f"{Fore.WHITE}{file1_path}: 总行数={file1_total}, 有效内容行数={file1_content}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{file2_path}: 总行数={file2_total}, 有效内容行数={file2_content}{Style.RESET_ALL}")
    print("─" * 80 + "\n")

    # 显示内容数量对比
    print(f"{Fore.CYAN}📈 内容数量对比:{Style.RESET_ALL}")
    print("─" * 80)
    if file1_content > file2_content:
        diff_count = file1_content - file2_content
        print(f"{Fore.GREEN}{file1_path} 比 {file2_path} 多 {diff_count} 行内容{Style.RESET_ALL}")
    elif file2_content > file1_content:
        diff_count = file2_content - file1_content
        print(f"{Fore.GREEN}{file2_path} 比 {file1_path} 多 {diff_count} 行内容{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}两个文件的有效内容行数相同{Style.RESET_ALL}")
    print("─" * 80 + "\n")

    # 检查是否有任何差异
    has_differences = len(diff1) > 0 or len(diff2) > 0 or len(count_diff) > 0

    if not has_differences:
        print(f"{Fore.GREEN}✅ 两个文件内容完全相同（包括相同的重复行）{Style.RESET_ALL}\n")
        return

    print(f"{Fore.CYAN}🔍 详细差异内容:{Style.RESET_ALL}\n")

    # 打印只在file1中存在的内容
    if diff1:
        print(f"{Fore.YELLOW}📄 仅在 {file1_path} 中存在的内容 ({len(diff1)} 行):{Style.RESET_ALL}")
        print("─" * 80)
        for i, line in enumerate(diff1, 1):
            print(f"{Fore.BLUE}{i}. {line}{Style.RESET_ALL}")
        print("─" * 80 + "\n")

    # 打印只在file2中存在的内容
    if diff2:
        print(f"{Fore.YELLOW}📄 仅在 {file2_path} 中存在的内容 ({len(diff2)} 行):{Style.RESET_ALL}")
        print("─" * 80)
        for i, line in enumerate(diff2, 1):
            print(f"{Fore.MAGENTA}{i}. {line}{Style.RESET_ALL}")
        print("─" * 80 + "\n")

    # 打印出现次数不同的内容
    if count_diff:
        print(f"{Fore.YELLOW}🔄 内容相同但出现次数不同的行:{Style.RESET_ALL}")
        print("─" * 80)
        for line, count1, count2 in count_diff:
            print(f"{Fore.YELLOW}{line}{Style.RESET_ALL}")
            print(f"  {Fore.BLUE}{file1_path}: 出现 {count1} 次{Style.RESET_ALL}")
            print(f"  {Fore.MAGENTA}{file2_path}: 出现 {count2} 次{Style.RESET_ALL}")
            print("  " + "-" * 76)
        print("─" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(description='比较两个文本文件的内容差异并显示多出的内容')
    parser.add_argument('--case1', required=True, help='第一个要比较的文件路径')
    parser.add_argument('--case2', required=True, help='第二个要比较的文件路径')

    args = parser.parse_args()

    # 读取两个文件
    file1_set, file1_lines, file1_counter, file1_total, file1_content = read_file(args.case1)
    file2_set, file2_lines, file2_counter, file2_total, file2_content = read_file(args.case2)

    # 检查文件读取是否成功
    if not file1_set or not file2_set or not file1_counter or not file2_counter:
        return

    # 找出差异
    diff1, diff2, count_diff = find_differences(file1_lines, file1_counter,
                                                file2_lines, file2_counter)

    # 打印差异
    print_differences(args.case1, args.case2, diff1, diff2, count_diff,
                      file1_total, file2_total, file1_content, file2_content)


if __name__ == "__main__":
    main()

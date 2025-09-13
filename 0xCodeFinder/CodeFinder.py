import os
import sys


class Colors:
    """终端颜色定义类"""
    RESET = '\033[0m'  # 重置颜色
    RED = '\033[31m'  # 红色
    GREEN = '\033[32m'  # 绿色
    YELLOW = '\033[33m'  # 黄色
    BLUE = '\033[34m'  # 蓝色
    MAGENTA = '\033[35m'  # 品红
    CYAN = '\033[36m'  # 青色
    WHITE = '\033[37m'  # 白色
    BOLD = '\033[1m'  # 加粗
    UNDERLINE = '\033[4m'  # 下划线


def print_separator():
    """打印青色分隔线，增强视觉分隔"""
    print(f"\n{Colors.CYAN}" + "=" * 60 + f"{Colors.RESET}\n")


def print_header(text):
    """打印带边框的蓝色加粗标题"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}" + "=" * 60)
    print(f"{' ' * 10}{text}{' ' * 10}")
    print("=" * 60 + f"{Colors.RESET}\n")


def is_binary_file(file_path):
    """判断文件是否为二进制文件（含空字节则视为二进制）"""
    try:
        with open(file_path, 'rb') as f:
            return b'\x00' in f.read(1024)
    except Exception:
        return True


def matches_file_extension(filename, extensions):
    """检查文件是否匹配指定的后缀"""
    if not extensions:  # 如果没有指定后缀，匹配所有文件
        return True

    # 检查文件是否以任何指定的后缀结尾（不区分大小写）
    filename_lower = filename.lower()
    for ext in extensions:
        if filename_lower.endswith(ext.lower()):
            return True
    return False


def search_keywords_in_file(file_path, keywords):
    """检查文件内容是否包含任意关键词（跳过二进制文件）"""
    if is_binary_file(file_path):
        return False

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()
            return any(keyword.lower() in content for keyword in keywords)
    except Exception as e:
        print(f"{Colors.RED}⚠️ 无法读取文件: {file_path}{Colors.RESET}")
        print(f"{Colors.RED}   错误详情: {str(e)}{Colors.RESET}")
        return False


def search_files(root_dir, keywords, extensions):
    """递归遍历目录，返回含关键词且匹配后缀的文件路径列表"""
    matched_files = []

    if not os.path.exists(root_dir):
        print(f"{Colors.RED}❌ 错误: 路径 '{root_dir}' 不存在{Colors.RESET}")
        return []

    if not os.path.isdir(root_dir):
        print(f"{Colors.RED}❌ 错误: '{root_dir}' 不是有效目录{Colors.RESET}")
        return []

    print(f"{Colors.GREEN}🔍 正在搜索目录: {root_dir}{Colors.RESET}")
    print(f"{Colors.GREEN}🔑 搜索关键词: {', '.join(keywords)}{Colors.RESET}")
    if extensions:
        print(f"{Colors.GREEN}📄 文件后缀过滤: {', '.join(extensions)}{Colors.RESET}")
    else:
        print(f"{Colors.GREEN}📄 文件后缀过滤: 所有文件{Colors.RESET}")
    print("\n请稍候，正在递归搜索文件...\n")

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # 检查文件后缀是否匹配
            if not matches_file_extension(filename, extensions):
                continue

            file_path = os.path.join(dirpath, filename)
            if search_keywords_in_file(file_path, keywords):
                matched_files.append(file_path)
                print(f"{Colors.CYAN}✅ 找到匹配文件: {file_path}{Colors.RESET}")

    return matched_files


def main():
    """主函数：处理用户输入并执行搜索"""
    os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
    print_header("文件关键词搜索工具")

    # 获取关键词（循环确保非空）
    while True:
        keywords_input = input(
            f"{Colors.YELLOW}请输入要搜索的关键词（多个用英文逗号分隔）: {Colors.RESET}"
        ).strip()
        if keywords_input:
            break
        print(f"{Colors.RED}⚠️ 关键词不能为空，请重新输入！{Colors.RESET}")
    keywords = [kw.strip() for kw in keywords_input.split(',') if kw.strip()]

    # 获取文件夹路径（循环确保非空且有效）
    while True:
        folder_path = input(
            f"{Colors.YELLOW}请输入要搜索的文件夹路径: {Colors.RESET}"
        ).strip()
        if folder_path:
            folder_path = os.path.expanduser(folder_path)  # 处理波浪号路径
            break
        print(f"{Colors.RED}⚠️ 文件夹路径不能为空，请重新输入！{Colors.RESET}")

    # 获取文件后缀（可以为空）
    extensions_input = input(
        f"{Colors.YELLOW}请输入要搜索的文件后缀（多个用英文逗号分隔，不输入则搜索所有文件）: {Colors.RESET}"
    ).strip()

    # 处理文件后缀，统一格式（确保带点号）
    extensions = []
    if extensions_input:
        extensions = [ext.strip() for ext in extensions_input.split(',') if ext.strip()]
        # 确保每个后缀都以点号开头
        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]

    # 执行搜索
    matched_files = search_files(folder_path, keywords, extensions)

    # 展示最终结果 - 只显示文件名，并用绿色输出
    print_separator()
    if matched_files:
        result_title = f"搜索完成 - 找到 {len(matched_files)} 个匹配文件"
        if extensions:
            result_title += f"（后缀: {', '.join(extensions)}）"
        print_header(result_title)
        for i, file_path in enumerate(matched_files, 1):
            # 只提取文件名并使用舒适的绿色输出
            file_name = os.path.basename(file_path)
            print(f"{i}. {Colors.GREEN}{file_name}{Colors.RESET}")
    else:
        no_result_msg = "搜索完成 - 未找到匹配的文件"
        if extensions:
            no_result_msg += f"（后缀: {', '.join(extensions)}）"
        print_header(no_result_msg)

    print_separator()
    print(f"{Colors.GREEN}感谢使用文件关键词搜索工具！{Colors.RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}程序被用户中断。{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}程序发生错误: {str(e)}{Colors.RESET}")
        sys.exit(1)

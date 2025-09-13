import os
import re


def get_md_files():
    """获取当前目录下所有的markdown文件"""
    md_files = []
    for file in os.listdir('.'):
        if file.lower().endswith('.md'):
            md_files.append(file)
    return md_files


def show_color_options():
    """显示可用的颜色选项并返回颜色字典"""
    colors = {
        "浅粉红": "#FFB6C1",
        "猩红": "#DC143C",
        "紫色": "#800080",
        "靛青": "#4B0082",
        "纯蓝": "#0000FF",
        "道奇蓝": "#1E90FF",
        "青色": "#00FFFF",
        "森林绿": "#228B22",
        "纯黄": "#FFFF00",
        "金": "#FFD700",
        "浅灰色": "#D3D3D3"
    }

    print("\n🎨 可用颜色选项:")
    for i, (name, code) in enumerate(colors.items(), 1):
        print(f"  {i}. {name} 🟥" if i == 1 else
              f"  {i}. {name} 🟪" if i <= 4 else
              f"  {i}. {name} 🟦" if i <= 7 else
              f"  {i}. {name} 🟩" if i == 8 else
              f"  {i}. {name} 🟨" if i <= 10 else
              f"  {i}. {name} 🟫")
        print(f"     代码: {code}")

    return colors


def modify_md_file(filename, target_text, color_code, color_name):
    """修改markdown文件，为目标文字添加背景色"""
    try:
        # 读取文件内容
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # 构建替换模式，精准匹配目标文本
        pattern = re.compile(re.escape(target_text))

        # 按要求格式添加背景色标签
        replacement = f'<font style="background-color: {color_code}">{target_text}</font>'
        new_content = pattern.sub(replacement, content)

        # 写回文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print("\n" + "=" * 40)
        print("✅ 处理成功完成！")
        print("📄 当前处理文件: " + filename)
        print("🔍 目标文字: " + target_text)
        print("🎨 应用颜色: " + color_name + " (" + color_code + ")")
        print("=" * 40 + "\n")
        return True

    except Exception as e:
        print("\n" + "=" * 40)
        print(f"❌ 处理文件时出错: {str(e)}")
        print("=" * 40 + "\n")
        return False


def select_file():
    """选择要处理的文件，只在程序开始时执行一次"""
    md_files = get_md_files()
    if not md_files:
        print("⚠️ 当前目录下没有找到Markdown文件(.md)")
        return None

    print("📂 找到以下Markdown文件:")
    for i, file in enumerate(md_files, 1):
        print(f"  {i}. {file}")

    while True:
        try:
            file_choice = int(input("\n🔢 请选择要处理的文件编号 (1-{}): ".format(len(md_files))))
            if 1 <= file_choice <= len(md_files):
                selected_file = md_files[file_choice - 1]
                print(f"\n📌 已选择文件: {selected_file}")
                print(f"   后续将持续对该文件操作，输入空文本可退出\n")
                return selected_file
            else:
                print(f"❌ 请输入1到{len(md_files)}之间的数字")
        except ValueError:
            print("❌ 请输入有效的数字")


def process_single_modification(selected_file):
    """处理单次修改操作，使用已选择的文件"""
    # 1. 输入目标文字，空文本退出
    target_text = input("✏️ 请输入要添加背景色的文字（输入空文本退出）: ").strip()
    if not target_text:
        return None  # 返回None表示要退出

    # 2. 选择背景色
    colors = show_color_options()
    while True:
        try:
            color_choice = int(input("\n🔢 请选择颜色编号 (1-{}): ".format(len(colors))))
            if 1 <= color_choice <= len(colors):
                color_name = list(colors.keys())[color_choice - 1]
                color_code = colors[color_name]
                break
            else:
                print(f"❌ 请输入1到{len(colors)}之间的数字")
        except ValueError:
            print("❌ 请输入有效的数字")

    # 3. 执行修改（无确认步骤）
    print("\n🚀 开始处理...")
    return modify_md_file(selected_file, target_text, color_code, color_name)


def main():
    print("\n" + "=" * 40)
    print("📝 Markdown 文本背景色修改工具")
    print("🔄 一次选择文件，连续修改直至输入空文本")
    print("=" * 40 + "\n")

    # 只选择一次文件
    selected_file = select_file()
    if not selected_file:
        return

    while True:
        # 执行单次修改（使用已选择的文件）
        result = process_single_modification(selected_file)

        # 如果返回None，表示用户输入了空文本，退出程序
        if result is None:
            print(f"\n👋 感谢使用，已完成对 {selected_file} 的修改！")
            break

        # 清空屏幕（跨平台支持）
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "=" * 40)
        print(f"📝 继续修改文件: {selected_file}")
        print("   输入空文本可退出程序")
        print("=" * 40 + "\n")


if __name__ == "__main__":
    main()

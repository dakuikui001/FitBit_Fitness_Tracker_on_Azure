import os
import shutil

def organize_files_by_date(source_root, target_root="organized_by_date"):
    # 确保目标根目录存在
    if not os.path.exists(target_root):
        os.makedirs(target_root)

    # 定义要扫描的文件夹（对应你图中的分类）
    categories = ['calories', 'heartrate', 'intensities', 'METs', 'sleep', 'steps', 'weight']
    
    count = 0
    for category in categories:
        category_path = os.path.join(source_root, category)
        
        # 检查文件夹是否存在
        if not os.path.exists(category_path):
            continue
            
        print(f"正在处理文件夹: {category}")
        
        for filename in os.listdir(category_path):
            if filename.endswith(".csv"):
                # 假设文件名格式: activity_2016-03-12.csv
                # 通过分割字符串获取日期部分
                try:
                    # 按照下划线分割，取第二部分并去掉 .csv
                    date_part = filename.split('_')[1].replace('.csv', '')
                    
                    # 创建对应的日期文件夹
                    date_folder = os.path.join(target_root, date_part)
                    if not os.path.exists(date_folder):
                        os.makedirs(date_folder)
                    
                    # 执行复制操作
                    src_file = os.path.join(category_path, filename)
                    dst_file = os.path.join(date_folder, filename)
                    
                    shutil.copy2(src_file, dst_file) # copy2 会保留元数据（如修改日期）
                    count += 1
                except IndexError:
                    print(f"跳过格式不符的文件: {filename}")

    print(f"\n整理完成！共复制了 {count} 个文件到目录: {target_root}")

if __name__ == "__main__":
    # 在当前目录下运行
    organize_files_by_date(".")
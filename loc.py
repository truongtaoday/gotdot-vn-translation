import os
import re

def extract_import_paths(input_directory, output_file="extracted_paths.txt"):
    """
    Đọc tất cả các file .txt trong thư mục, tìm kiếm dòng chứa 'path="res://.import/',
    trích xuất đường dẫn và ghi vào một file .txt tổng hợp.

    Args:
        input_directory (str): Đường dẫn đến thư mục chứa các file .txt.
        output_file (str, optional): Tên của file .txt đầu ra. Mặc định là "extracted_paths.txt".
    """
    extracted_paths = []
    for filename in os.listdir(input_directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(input_directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        if "path=\"res://.import/" in line:
                            # Sử dụng regex để trích xuất giá trị đường dẫn
                            match = re.search(r'path="([^"]*)"', line)
                            if match:
                                path = match.group(1)
                                extracted_paths.append(path)
            except Exception as e:
                print(f"Lỗi khi đọc file {filename}: {e}")

    if extracted_paths:
        try:
            with open(output_file, 'w', encoding='utf-8') as outfile:
                for path in extracted_paths:
                    outfile.write(path + "\n")
            print(f"Đã trích xuất và lưu các đường dẫn vào file: {output_file}")
        except Exception as e:
            print(f"Lỗi khi ghi vào file đầu ra: {e}")
    else:
        print("Không tìm thấy đường dẫn nào chứa 'path=\"res://.import/' trong các file .txt.")

if __name__ == "__main__":
    # Thay thế đường dẫn thư mục chứa các file .txt của bạn vào đây
    input_directory = "đường_dẫn_đến_thư_mục_chứa_file_txt"
    extract_import_paths(input_directory)

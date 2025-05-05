import os
import sys

def extract_messages(folder_path):
    try:
        if not os.path.isdir(folder_path):
            print("Thư mục không tồn tại!")
            return

        with open("dich.txt", "w", encoding="utf-8") as out_file, \
             open("vitri.txt", "w", encoding="utf-8") as pos_file:

            msg_count = 0
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.endswith(".tres"):
                        file_path = os.path.join(root, file)
                        file_path = os.path.normpath(file_path)  # CHUẨN HÓA ĐƯỜNG DẪN

                        with open(file_path, "r", encoding="utf-8") as f:
                            lines = f.readlines()

                        for i, line in enumerate(lines):
                            if line.strip().startswith('message = '):
                                try:
                                    # Lấy chuỗi bên trong dấu nháy kép
                                    start = line.index('"') + 1
                                    end = line.rindex('"')
                                    message = line[start:end]
                                    out_file.write(f"{msg_count + 1}. {message}\n")
                                    pos_file.write(f"{msg_count + 1}: {file_path} | Line {i}\n")
                                    msg_count += 1
                                except ValueError:
                                    print(f"Lỗi định dạng ở dòng: {line.strip()}")

        print(f"Đã trích xuất {msg_count} thông điệp.")
    except Exception as e:
        print(f"Lỗi khi trích xuất: {e}")

def update_messages(input_file):
    try:
        if not os.path.isfile("vitri.txt"):
            print("Không tìm thấy file vitri.txt!")
            return

        # Đọc bản dịch đã chỉnh sửa
        translations = {}
        with open(input_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() and line.split(".")[0].isdigit():
                    parts = line.strip().split(".", 1)
                    idx = int(parts[0])
                    text = parts[1].strip()
                    translations[idx] = text

        # Đọc ánh xạ vị trí
        mapping = {}
        with open("vitri.txt", "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() and line.split(":")[0].isdigit():
                    idx = int(line.split(":")[0])
                    rest = line.strip().split(":", 1)[1].strip()
                    path_part = rest.split("|")[0].strip()
                    line_part = rest.split("Line ")[1].strip() if "Line " in rest else "0"
                    try:
                        line_num = int(line_part)
                    except:
                        line_num = 0
                    mapping[idx] = (os.path.normpath(path_part), line_num)  # CHUẨN HÓA ĐƯỜNG DẪN

        # Cập nhật từng file
        updated_files = set()
        for idx in translations:
            if idx not in mapping:
                print(f"Số thứ tự {idx} không hợp lệ hoặc không tồn tại trong vitri.txt.")
                continue

            file_path, line_num = mapping[idx]
            if not os.path.isfile(file_path):
                print(f"File {file_path} không tồn tại.")
                continue

            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            if line_num >= len(lines):
                print(f"Dòng {line_num} trong {file_path} vượt quá số dòng của file.")
                continue

            original_line = lines[line_num].strip()
            if not original_line.startswith('message = '):
                print(f"Dòng {line_num} trong {file_path} không phải là dòng chứa message.")
                continue

            # Giữ nguyên phần trước dấu nháy và thay nội dung sau đó
            before_quote = original_line.split('"', 1)[0]
            new_line = f'{before_quote}"{translations[idx]}"\n'

            lines[line_num] = new_line
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

            updated_files.add(file_path)

        print(f"Đã cập nhật {len(updated_files)} file .tres.")
    except Exception as e:
        print(f"Lỗi khi cập nhật: {e}")

def main():
    print("=== CHƯƠNG TRÌNH XỬ LÝ FILE TRES ===")
    print("1. Trích xuất thông điệp")
    print("2. Cập nhật thông điệp đã dịch")
    choice = input("Chọn chế độ (1 hoặc 2): ").strip()

    if choice == "1":
        folder = input("Nhập đường dẫn thư mục chứa file .tres: ").strip()
        extract_messages(folder)
    elif choice == "2":
        file_input = input("Nhập đường dẫn file văn bản chứa bản dịch (ví dụ: dich.txt): ").strip()
        if not os.path.isfile(file_input):
            print("File đầu vào không tồn tại!")
        else:
            update_messages(file_input)
    else:
        print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()

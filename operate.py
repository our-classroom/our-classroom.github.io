import json
import os
import sys
import base64
from datetime import datetime

class YearbookManager:
    def __init__(self, data_file="data/data.json"):
        self.data_file = data_file
        self.data = {
            "students": [],
            "teachers": [],
            "schoolInfo": {},
            "messages": {}
        }
        self.load_data()

    def load_data(self):
        """从JSON文件加载数据"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                print(f"成功加载数据文件: {self.data_file}")
            else:
                print(f"数据文件不存在，将创建新文件: {self.data_file}")
                # 确保目录存在
                os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
                self.save_data()
        except Exception as e:
            print(f"加载数据时出错: {e}")
            self.save_data()

    def save_data(self):
        """保存数据到JSON文件"""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            print(f"数据已保存到: {self.data_file}")
            return True
        except Exception as e:
            print(f"保存数据时出错: {e}")
            return False

    def add_student(self, name, gender, student_id=None, photo_path="images/assets/default-rect.png",
                    dingding=None, wechat=None, phone=None, address=None, personality=None, introduction=None, hobbies=None):
        """添加学生"""
        # 生成学生ID (如果未提供)
        if not student_id:
            existing_ids = [s['id'] for s in self.data['students']]
            next_num = 1
            while f"S{next_num:03d}" in existing_ids:
                next_num += 1
            student_id = f"S{next_num:03d}"

        # 处理照片
        photo_data = None
        if photo_path and os.path.exists(photo_path):
            try:
                # 如果使用Base64编码存储照片
                with open(photo_path, 'rb') as img_file:
                    photo_data = f"data:image/{photo_path.split('.')[-1]};base64," + base64.b64encode(img_file.read()).decode('utf-8')
            except Exception as e:
                print(f"处理照片时出错: {e}")
                photo_data = None

        # 创建学生数据
        student = {
            "id": student_id,
            "name": name,
            "gender": gender,
            "photo": photo_data if photo_data else photo_path,  # 使用编码后的数据或路径
            "contact": {
                "dingding": dingding or "",
                "wechat": wechat or "",
                "phone": phone or ""
            },
            "address": address or "",
            "personality": personality or "",
            "introduction": introduction or "",
            "hobbies": hobbies or ""
        }

        # 检查是否已存在相同ID的学生
        for i, s in enumerate(self.data['students']):
            if s['id'] == student_id:
                self.data['students'][i] = student
                print(f"已更新学生: {name} (ID: {student_id})")
                self.save_data()
                return student_id

        # 添加新学生
        self.data['students'].append(student)
        print(f"已添加学生: {name} (ID: {student_id})")
        self.save_data()
        return student_id

    def add_teacher(self, name, gender, subject, photo_path=None,
                    dingding=None, wechat=None, phone=None, motto=None):
        """添加老师"""
        # 生成老师ID
        existing_ids = [t['id'] for t in self.data['teachers']]
        next_num = 1
        while f"T{next_num:03d}" in existing_ids:
            next_num += 1
        teacher_id = f"T{next_num:03d}"

        # 处理照片
        photo_data = None
        if photo_path and os.path.exists(photo_path):
            try:
                # 如果使用Base64编码存储照片
                with open(photo_path, 'rb') as img_file:
                    photo_data = f"data:image/{photo_path.split('.')[-1]};base64," + base64.b64encode(img_file.read()).decode('utf-8')
            except Exception as e:
                print(f"处理照片时出错: {e}")
                photo_data = None

        # 创建老师数据
        teacher = {
            "id": teacher_id,
            "name": name,
            "gender": gender,
            "subject": subject,
            "photo": photo_data if photo_data else photo_path,
            "contact": {
                "dingding": dingding or "",
                "wechat": wechat or "",
                "phone": phone or ""
            },
            "motto": motto or ""
        }

        # 检查是否已存在相同ID的老师
        for i, t in enumerate(self.data['teachers']):
            if t['id'] == teacher_id:
                self.data['teachers'][i] = teacher
                print(f"已更新老师: {name} (ID: {teacher_id})")
                self.save_data()
                return teacher_id

        # 添加新老师
        self.data['teachers'].append(teacher)
        print(f"已添加老师: {name} (ID: {teacher_id})")
        self.save_data()
        return teacher_id

    def update_school_info(self, name=None, found_year=None, description=None,
                           student_count=None, teacher_count=None, images=None):
        """更新学校信息"""
        if name:
            self.data['schoolInfo']['name'] = name
        if found_year:
            self.data['schoolInfo']['foundYear'] = found_year
        if description:
            self.data['schoolInfo']['description'] = description
        if student_count:
            self.data['schoolInfo']['studentCount'] = student_count
        if teacher_count:
            self.data['schoolInfo']['teacherCount'] = teacher_count

        # 处理学校照片
        if images:
            school_images = []
            for img_path in images:
                if os.path.exists(img_path):
                    try:
                        # 如果使用Base64编码存储照片
                        with open(img_path, 'rb') as img_file:
                            img_data = f"data:image/{img_path.split('.')[-1]};base64," + base64.b64encode(img_file.read()).decode('utf-8')
                            school_images.append(img_data)
                    except Exception as e:
                        print(f"处理学校照片时出错: {e}")
                        school_images.append(img_path)
                else:
                    school_images.append(img_path)

            self.data['schoolInfo']['images'] = school_images

        print("学校信息已更新")
        self.save_data()

    def add_message(self, person_id, sender_name, message_text):
        """添加留言"""
        if person_id not in self.data['messages']:
            self.data['messages'][person_id] = []

        message = {
            "sender": sender_name,
            "text": message_text,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.data['messages'][person_id].append(message)
        print(f"已为 {person_id} 添加来自 {sender_name} 的留言")
        self.save_data()

    def list_students(self):
        """列出所有学生"""
        print("\n=== 学生列表 ===")
        for student in self.data['students']:
            print(f"ID: {student['id']}, 姓名: {student['name']}, 性别: {student['gender']}")

    def list_teachers(self):
        """列出所有老师"""
        print("\n=== 老师列表 ===")
        for teacher in self.data['teachers']:
            print(f"ID: {teacher['id']}, 姓名: {teacher['name']}, 学科: {teacher['subject']}")

    def export_data(self, export_file):
        """导出数据到指定文件"""
        try:
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            print(f"数据已导出到: {export_file}")
            return True
        except Exception as e:
            print(f"导出数据时出错: {e}")
            return False

    def import_data(self, import_file):
        """从指定文件导入数据"""
        try:
            with open(import_file, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)

            # 验证导入数据的结构
            required_keys = ["students", "teachers", "schoolInfo", "messages"]
            if not all(key in imported_data for key in required_keys):
                print("导入文件格式无效，缺少必要的数据结构")
                return False

            self.data = imported_data
            print(f"从 {import_file} 成功导入数据")
            self.save_data()
            return True
        except Exception as e:
            print(f"导入数据时出错: {e}")
            return False

    def delete_student(self, student_id):
        """删除学生"""
        for i, student in enumerate(self.data['students']):
            if student['id'] == student_id:
                deleted = self.data['students'].pop(i)
                print(f"已删除学生: {deleted['name']} (ID: {student_id})")
                # 同时删除相关留言
                if student_id in self.data['messages']:
                    del self.data['messages'][student_id]
                    print(f"已删除学生 {student_id} 的所有留言")
                self.save_data()
                return True

        print(f"未找到ID为 {student_id} 的学生")
        return False

    def delete_teacher(self, teacher_id):
        """删除老师"""
        for i, teacher in enumerate(self.data['teachers']):
            if teacher['id'] == teacher_id:
                deleted = self.data['teachers'].pop(i)
                print(f"已删除老师: {deleted['name']} (ID: {teacher_id})")
                # 同时删除相关留言
                if teacher_id in self.data['messages']:
                    del self.data['messages'][teacher_id]
                    print(f"已删除老师 {teacher_id} 的所有留言")
                self.save_data()
                return True

        print(f"未找到ID为 {teacher_id} 的老师")
        return False

    def get_student(self, student_id):
        """获取学生信息"""
        for student in self.data['students']:
            if student['id'] == student_id:
                return student
        return None

    def get_teacher(self, teacher_id):
        """获取老师信息"""
        for teacher in self.data['teachers']:
            if teacher['id'] == teacher_id:
                return teacher
        return None

    def update_student(self, student_id):
        """更新学生信息"""
        student = self.get_student(student_id)
        if not student:
            print(f"未找到ID为 {student_id} 的学生")
            return False

        print(f"\n--- 当前学生信息 ---")
        print(f"ID: {student['id']}, 姓名: {student['name']}, 性别: {student['gender']}")
        print(f"照片: {student['photo']}")
        print(f"钉钉ID: {student['contact']['dingding']}, 微信ID: {student['contact']['wechat']}, 电话: {student['contact']['phone']}")
        print(f"家庭住址: {student['address']}, 性格特点: {student['personality']}")
        print(f"简介: {student['introduction']}")
        print(f"爱干的事: {student['hobbies']}")

        print("\n请选择要更新的信息:")
        print("1. 姓名")
        print("2. 性别")
        print("3. 照片")
        print("4. 钉钉ID")
        print("5. 微信ID")
        print("6. 电话")
        print("7. 家庭住址")
        print("8. 性格特点")
        print("9. 简介")
        print("10. 爱干的事")
        choice = input("请输入选项 (1-10): ")

        if choice == '1':
            new_name = input("请输入新的姓名: ")
            student['name'] = new_name
        elif choice == '2':
            new_gender = input("请输入新的性别 (男/女): ")
            student['gender'] = new_gender
        elif choice == '3':
            new_photo_path = input("请输入新的照片路径: ")
            if new_photo_path and os.path.exists(new_photo_path):
                try:
                    with open(new_photo_path, 'rb') as img_file:
                        photo_data = f"data:image/{new_photo_path.split('.')[-1]};base64," + base64.b64encode(img_file.read()).decode('utf-8')
                    student['photo'] = photo_data
                except Exception as e:
                    print(f"处理照片时出错: {e}")
            else:
                student['photo'] = new_photo_path
        elif choice in ['4', '5', '6']:
            contact_type = { '4': 'dingding', '5': 'wechat', '6': 'phone' }
            new_value = input(f"请输入新的{contact_type[choice]}: ")
            student['contact'][contact_type[choice]] = new_value
        elif choice == '7':
            new_address = input("请输入新的家庭住址: ")
            student['address'] = new_address
        elif choice == '8':
            new_personality = input("请输入新的性格特点: ")
            student['personality'] = new_personality
        elif choice == '9':
            new_introduction = input("请输入新的简介: ")
            student['introduction'] = new_introduction
        elif choice == '10':
            new_hobbies = input("请输入新的爱干的事: ")
            student['hobbies'] = new_hobbies
        else:
            print("无效选择，更新失败")
            return False

        print(f"学生 {student['name']} 的信息已更新")
        self.save_data()
        return True

    def update_teacher(self, teacher_id):
        """更新老师信息"""
        teacher = self.get_teacher(teacher_id)
        if not teacher:
            print(f"未找到ID为 {teacher_id} 的老师")
            return False

        print(f"\n--- 当前老师信息 ---")
        print(f"ID: {teacher['id']}, 姓名: {teacher['name']}, 学科: {teacher['subject']}")
        print(f"照片: {teacher['photo']}")
        print(f"钉钉ID: {teacher['contact']['dingding']}, 微信ID: {teacher['contact']['wechat']}, 电话: {teacher['contact']['phone']}")
        print(f"教育格言: {teacher['motto']}")

        print("\n请选择要更新的信息:")
        print("1. 姓名")
        print("2. 性别")
        print("3. 学科")
        print("4. 照片")
        print("5. 钉钉ID")
        print("6. 微信ID")
        print("7. 电话")
        print("8. 教育格言")
        choice = input("请输入选项 (1-8): ")

        if choice == '1':
            new_name = input("请输入新的姓名: ")
            teacher['name'] = new_name
        elif choice == '2':
            new_gender = input("请输入新的性别 (男/女): ")
            teacher['gender'] = new_gender
        elif choice == '3':
            new_subject = input("请输入新的学科: ")
            teacher['subject'] = new_subject
        elif choice == '4':
            new_photo_path = input("请输入新的照片路径: ")
            if new_photo_path and os.path.exists(new_photo_path):
                try:
                    with open(new_photo_path, 'rb') as img_file:
                        photo_data = f"data:image/{new_photo_path.split('.')[-1]};base64," + base64.b64encode(img_file.read()).decode('utf-8')
                    teacher['photo'] = photo_data
                except Exception as e:
                    print(f"处理照片时出错: {e}")
            else:
                teacher['photo'] = new_photo_path
        elif choice in ['5', '6', '7']:
            contact_type = { '5': 'dingding', '6': 'wechat', '7': 'phone' }
            new_value = input(f"请输入新的{contact_type[choice]}: ")
            teacher['contact'][contact_type[choice]] = new_value
        elif choice == '8':
            new_motto = input("请输入新的教育格言: ")
            teacher['motto'] = new_motto
        else:
            print("无效选择，更新失败")
            return False

        print(f"老师 {teacher['name']} 的信息已更新")
        self.save_data()
        return True


def show_menu():
    """显示菜单"""
    print("\n===== 毕业纪念册管理系统 =====")
    print("1.  添加学生")
    print("2.  添加老师")
    print("3.  更新学校信息")
    print("4.  添加留言")
    print("5.  查看学生列表")
    print("6.  查看老师列表")
    print("7.  导出数据")
    print("8.  导入数据")
    print("9.  删除学生")
    print("10. 删除老师")
    print("11. 更新学生信息")
    print("12. 更新老师信息")
    print("0.  退出系统")
    print("===========================")
    choice = input("请选择操作 (0-10): ")
    return choice

def main():
    # 创建管理器实例
    manager = YearbookManager()

    while True:
        choice = show_menu()

        if choice == '1':
            print("\n--- 添加学生 ---")
            name = input("姓名: ")
            gender = input("性别 (男/女): ")
            student_id = input("学号 (留空自动生成): ")
            photo_path = input("照片路径 (可选): ")
            dingding = input("钉钉ID (可选): ")
            wechat = input("微信ID (可选): ")
            phone = input("电话 (可选): ")
            address = input("家庭住址 (可选): ")
            personality = input("性格特点 (可选): ")

            manager.add_student(
                name, gender, student_id if student_id else None,
                photo_path if photo_path else None,
                dingding, wechat, phone, address, personality
            )

        elif choice == '2':
            print("\n--- 添加老师 ---")
            name = input("姓名: ")
            gender = input("性别 (男/女): ")
            subject = input("任教科目: ")
            photo_path = input("照片路径 (可选): ")
            dingding = input("钉钉ID (可选): ")
            wechat = input("微信ID (可选): ")
            phone = input("电话 (可选): ")
            motto = input("教育格言 (可选): ")

            manager.add_teacher(
                name, gender, subject,
                photo_path if photo_path else None,
                dingding, wechat, phone, motto
            )

        elif choice == '3':
            print("\n--- 更新学校信息 ---")
            name = input("学校名称: ")

            found_year = None
            year_input = input("建校年份: ")
            if year_input:
                try:
                    found_year = int(year_input)
                except:
                    print("年份必须是数字")

            description = input("学校简介: ")

            student_count = None
            count_input = input("学生总数: ")
            if count_input:
                try:
                    student_count = int(count_input)
                except:
                    print("学生数必须是数字")

            teacher_count = None
            count_input = input("教师总数: ")
            if count_input:
                try:
                    teacher_count = int(count_input)
                except:
                    print("教师数必须是数字")

            images_input = input("学校照片路径 (多个路径用逗号分隔): ")
            images = [img.strip() for img in images_input.split(',')] if images_input else None

            manager.update_school_info(
                name, found_year, description,
                student_count, teacher_count, images
            )

        elif choice == '4':
            print("\n--- 添加留言 ---")
            manager.list_students()
            manager.list_teachers()

            person_id = input("\n请输入要添加留言的学生或老师ID: ")
            # 验证ID是否存在
            student = manager.get_student(person_id)
            teacher = manager.get_teacher(person_id)

            if not student and not teacher:
                print(f"未找到ID为 {person_id} 的人员")
                continue

            sender_name = input("您的姓名: ")
            message_text = input("留言内容: ")

            manager.add_message(person_id, sender_name, message_text)

        elif choice == '5':
            manager.list_students()

        elif choice == '6':
            manager.list_teachers()

        elif choice == '7':
            print("\n--- 导出数据 ---")
            export_file = input("导出文件路径: ")
            manager.export_data(export_file)

        elif choice == '8':
            print("\n--- 导入数据 ---")
            import_file = input("导入文件路径: ")
            manager.import_data(import_file)

        elif choice == '9':
            print("\n--- 删除学生 ---")
            manager.list_students()
            student_id = input("\n请输入要删除的学生ID: ")
            manager.delete_student(student_id)

        elif choice == '10':
            print("\n--- 删除老师 ---")
            manager.list_teachers()
            teacher_id = input("\n请输入要删除的老师ID: ")
            manager.delete_teacher(teacher_id)

        elif choice == '11':
            print("\n--- 更新学生信息 ---")
            manager.list_students()
            student_id = input("\n请输入要更新的学生ID: ")
            manager.update_student(student_id)

        elif choice == '12':
            print("\n--- 更新老师信息 ---")
            manager.list_teachers()
            teacher_id = input("\n请输入要更新的老师ID: ")
            manager.update_teacher(teacher_id)


        elif choice == '0':
            print("感谢使用毕业纪念册管理系统，再见！")
            break

        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main()
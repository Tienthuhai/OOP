import tkinter as tk
from tkinter import messagebox, simpledialog
import csv
import os

# Class cha User
class User:
    def __init__(self, username, password, personal_info=""):
        self.username = username
        self.password = password
        self.personal_info = personal_info

# Class con Admin kế thừa từ User
class Admin(User):
    def __init__(self, username, password, personal_info=""):
        super().__init__(username, password, personal_info)
        #super().__init__(username, password)

# Class con Customer kế thừa từ User
class Customer(User):
    def __init__(self, username, password, personal_info=""):
        super().__init__(username, password, personal_info)
        #super().__init__(username, password)

class DataManager:
    def __init__(self, users_file, menu_file):
        self.users_file = users_file
        self.menu_file = menu_file
        self.users = self.load_users()
        self.menu_items = self.load_menu()

    def load_users(self):
        users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["role"] == "admin":
                        users[row["username"]] = Admin(row["username"], row["password"], row["personal_info"])
                    else:
                        users[row["username"]] = Customer(row["username"], row["password"], row["personal_info"])
        return users

    def load_menu(self):
        menu_items = []
        if os.path.exists(self.menu_file):
            with open(self.menu_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    menu_items.append(row)
        return menu_items

    def save_user(self, username, password, role):
        with open(self.users_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password, role])
        if role == "admin":
            self.users[username] = Admin(username, password)
        else:
            self.users[username] = Customer(username, password)

    def save_food(self, food_name, price):
        with open(self.menu_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([food_name, price])
        self.menu_items.append([food_name, price])

    def delete_food(self, food_name):
        self.menu_items = [item for item in self.menu_items if item[0] != food_name]
        with open(self.menu_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.menu_items)
    def update_user_info(self, username, new_personal_info):
        # Cập nhật thông tin cá nhân trong file users.csv
        updated_users = []
        with open(self.users_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    row["personal_info"] = new_personal_info  
                updated_users.append(row)

        
        with open(self.users_file, mode='w', newline='') as file:
            fieldnames = ['username', 'password', 'role', 'personal_info']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_users)

class LoginScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.username_entry = None
        self.password_entry = None
        self.setup()

    def setup(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Tên người dùng:").pack(pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)
        
        tk.Label(self.root, text="Mật khẩu:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(self.root, text="Đăng nhập", command=self.login).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        user = self.app.data_manager.users.get(username)
        if user and user.password == password:
            self.app.current_user = user
            messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
            self.show_user_info() 
            if isinstance(user, Admin):
                self.app.show_admin_screen()
            else:
                self.app.show_customer_screen()
        else:
            messagebox.showerror("Lỗi", "Tên người dùng hoặc mật khẩu không chính xác!")
    def show_user_info(self):
        if isinstance(self.app.current_user, Customer):
            personal_info = self.app.current_user.personal_info
            messagebox.showinfo("Thông tin cá nhân", f"Thông tin của bạn: {personal_info}")
    def update_user_info(self, username, new_personal_info):
        # Cập nhật thông tin cá nhân trong file users.csv
        updated_users = []
        with open(self.users_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    row["personal_info"] = new_personal_info 
                updated_users.append(row)

        
        with open(self.users_file, mode='w', newline='') as file:
            fieldnames = ['username', 'password', 'role', 'personal_info']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_users)
            
  
        
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class CustomerScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup()

    def setup(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Chức năng Khách hàng", font=("Arial", 14, "bold")).pack(pady=10)
        if self.app.current_user:
            personal_info_label = tk.Label(self.root, text=f"Thông tin cá nhân: {self.app.current_user.personal_info}")
            personal_info_label.pack(pady=5)
        functions_khach_hang = [
            "Đặt bàn và gọi món", 
            "Xem lịch sử hóa đơn"
        ]
        for func in functions_khach_hang:
            if func == "Đặt bàn và gọi món":
                tk.Button(self.root, text=func, width=30, command=self.app.show_order_screen).pack(pady=5)
            elif func == "Xem lịch sử hóa đơn":
                tk.Button(self.root, text=func, width=30, command=self.app.show_order_history_screen).pack(pady=5)
            else:
                 tk.Button(self.root, text=func, width=30, command=lambda f=func: self.show_message(f)).pack(pady=5) 
            
           
        tk.Button(self.root, text="Cập nhật thông tin cá nhân", command=self.update_personal_info).pack(pady=5)
        tk.Button(self.root, text="Đăng xuất", command=self.app.show_login_screen, fg="red").pack(pady=20)
    def update_personal_info(self):
        # Hiển thị hộp thoại để người dùng nhập thông tin cá nhân mới
        new_info = simpledialog.askstring("Cập nhật thông tin", "Nhập thông tin cá nhân mới:")
        if new_info:
            self.app.current_user.personal_info = new_info
            
            self.app.data_manager.update_user_info(self.app.current_user.username, new_info)
            messagebox.showinfo("Thông báo", "Cập nhật thông tin cá nhân thành công!")
    def show_message(self, function_name):
        messagebox.showinfo("Thông báo", f"Chức năng '{function_name}' đang được phát triển")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class AdminScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup()

    def setup(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Chức năng Admin", font=("Arial", 14, "bold")).pack(pady=10)
        functions_nhan_vien = [
            "Quản lý Bàn",
            "Quản lý Thực Đơn", "Quản lý Nhân Sự", 
            "Thống kê Hóa Đơn", "Quản lý khách hàng",
            "Thêm tài khoản"
        ]
        for func in functions_nhan_vien:
            if func == "Quản lý Thực Đơn":
                tk.Button(self.root, text=func, width=30, command=self.app.show_menu_screen).pack(pady=5)
            elif func == "Quản lý Bàn":
                tk.Button(self.root, text=func, width=30, command=self.app.show_table_screen).pack(pady=5)
            elif func == "Thống kê Hóa Đơn":
                tk.Button(self.root, text=func, width=30, command=self.app.show_invoice_screen).pack(pady=5)
            
            elif func == "Quản lý khách hàng":
                tk.Button(self.root, text=func, width=30, command=self.app.show_customer_management_screen).pack(pady=5)
                
            elif func == "Thêm tài khoản":
                tk.Button(self.root, text=func, width=30, command=self.app.show_add_user_screen).pack(pady=5)
            elif func == "Quản lý Nhân Sự":
                tk.Button(self.root, text=func, width=30, command=self.app.show_employee_screen).pack(pady=5)
            else:
                tk.Button(self.root, text=func, width=30, command=lambda f=func: self.show_message(f)).pack(pady=5)

        tk.Button(self.root, text="Đăng xuất", command=self.app.show_login_screen, fg="red").pack(pady=20)

    def show_message(self, function_name):
        messagebox.showinfo("Thông báo", f"Chức năng '{function_name}' đang được phát triển")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class AddUserScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup()

    def setup(self):
        self.clear_screen()

        tk.Label(self.root, text="Thêm Tài Khoản Mới", font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(self.root, text="Tên người dùng:").pack(pady=10)
        self.new_username_entry = tk.Entry(self.root)
        self.new_username_entry.pack(pady=5)
        
        tk.Label(self.root, text="Mật khẩu:").pack(pady=10)
        self.new_password_entry = tk.Entry(self.root, show="*")
        self.new_password_entry.pack(pady=5)
        
        tk.Label(self.root, text="Vai trò (admin/customer):").pack(pady=10)
        self.new_role_entry = tk.Entry(self.root)
        self.new_role_entry.pack(pady=5)
        
        tk.Button(self.root, text="Thêm Tài Khoản", command=self.add_user).pack(pady=20)
        tk.Button(self.root, text="Quay lại", command=self.app.show_admin_screen, fg="red").pack(pady=5)

    def add_user(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        role = self.new_role_entry.get()
        
        if username and password and role in ["admin", "customer"]:
            if username not in self.app.data_manager.users:
                self.app.data_manager.save_user(username, password, role)
                messagebox.showinfo("Thông báo", "Thêm tài khoản thành công!")
                self.app.show_admin_screen()
            else:
                messagebox.showerror("Lỗi", "Tài khoản đã tồn tại!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin và chọn vai trò hợp lệ!")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class TableScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup()

    def setup(self):
        self.clear_screen()

        tk.Label(self.root, text="Quản lý Bàn", font=("Arial", 14, "bold")).pack(pady=10)

        # Tạo Listbox để hiển thị danh sách bàn
        self.table_listbox = tk.Listbox(self.root, width=60, height=10)
        self.table_listbox.pack(pady=10)

        
        tk.Button(self.root, text="Xem Danh Sách Bàn", command=self.show_table).pack(pady=5)
        tk.Button(self.root, text="Thêm Bàn", command=self.add_table).pack(pady=5)
        tk.Button(self.root, text="Sửa Bàn", command=self.edit_table).pack(pady=5)
        tk.Button(self.root, text="Xóa Bàn", command=self.delete_table).pack(pady=5)
        tk.Button(self.root, text="Quay lại", command=self.app.show_admin_screen).pack(pady=5)

        self.update_table_listbox()

    def update_table_listbox(self):
        """Cập nhật nội dung của Listbox từ file tables.csv."""
        self.table_listbox.delete(0, tk.END) 
        try:
            with open("table.csv", mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                
                for row in reader:
                    if len(row) >= 3: 
                        self.table_listbox.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]}") 
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file danh sách bàn!")

    def show_table(self):
        """Hiển thị danh sách bàn trong Listbox."""
        self.update_table_listbox()

    def add_table(self):
        table_name = simpledialog.askstring("Thêm Bàn", "Nhập tên bàn:")
        waiter_name = simpledialog.askstring("Thêm Bàn", "Nhập tên nhân viên phục vụ:")
        status = "Trống"  

        if table_name and waiter_name:
            with open("table.csv", mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([table_name, waiter_name, status])
            messagebox.showinfo("Thông báo", f"Bàn {table_name} đã được thêm!")
            self.update_table_listbox()
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

    def edit_table(self):
        selected_item = self.table_listbox.curselection()
        if selected_item:
            table_info = self.table_listbox.get(selected_item[0]).split(" | ")
            table_name = table_info[0]  
            current_waiter = table_info[1]
            current_status = table_info[2]

            new_waiter = simpledialog.askstring("Sửa Bàn", "Nhập tên nhân viên mới:", initialvalue=current_waiter)
            new_status = simpledialog.askstring("Sửa Trạng Thái", "Nhập trạng thái mới (Trống/Đã đặt):", initialvalue=current_status)

            if new_waiter and new_status in ["Trống", "Đã đặt"]:
                table_data = []
                found = False

                with open("table.csv", mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 3:
                            if row[0] == table_name:
                                found = True
                                table_data.append([table_name, new_waiter, new_status])  
                            else:
                                table_data.append(row)

                if found:
                    with open("table.csv", mode='w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerows(table_data)
                    messagebox.showinfo("Thông báo", f"Bàn {table_name} đã được sửa!")
                    self.update_table_listbox()
                else:
                    messagebox.showerror("Lỗi", f"Bàn '{table_name}' không tồn tại!")
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin và trạng thái hợp lệ!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn bàn để sửa!")

    def delete_table(self):
        selected_item = self.table_listbox.curselection()
        if selected_item:
            table_name = self.table_listbox.get(selected_item[0]).split(" | ")[0]  
            table_data = []
            found = False

            with open("table.csv", mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 3:  
                        if row[0] != table_name:
                            table_data.append(row)
                        else:
                            found = True

            if found:
                with open("table.csv", mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(table_data)
                messagebox.showinfo("Thông báo", f"Bàn {table_name} đã được xóa!")
                self.update_table_listbox()
            else:
                messagebox.showerror("Lỗi", f"Bàn '{table_name}' không tồn tại!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn bàn để xóa!")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class EmployeeScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup()

    def setup(self):
        self.clear_screen()

        tk.Label(self.root, text="Quản lý Nhân sự", font=("Arial", 14, "bold")).pack(pady=10)

        # Tạo Listbox để hiển thị danh sách nhân viên
        self.employee_listbox = tk.Listbox(self.root, width=50, height=10)
        self.employee_listbox.pack(pady=10)

      
        tk.Button(self.root, text="Xem Danh Sách Nhân Viên", command=self.show_employees).pack(pady=5)
        tk.Button(self.root, text="Thêm Nhân Viên", command=self.add_employee).pack(pady=5)
        tk.Button(self.root, text="Sửa Nhân Viên", command=self.edit_employee).pack(pady=5)
        tk.Button(self.root, text="Xóa Nhân Viên", command=self.delete_employee).pack(pady=5)
        tk.Button(self.root, text="Quay lại", command=self.app.show_admin_screen).pack(pady=5)

        self.update_employee_listbox()

    def update_employee_listbox(self):
        """Cập nhật nội dung của Listbox từ file danh sách nhân viên."""
        self.employee_listbox.delete(0, tk.END)
        try:
            with open("employees.csv", mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 3:
                        self.employee_listbox.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]}")
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file danh sách nhân viên!")

    def show_employees(self):
        """Hiển thị danh sách nhân viên trong Listbox."""
        self.update_employee_listbox()

    def add_employee(self):
        name = simpledialog.askstring("Thêm Nhân Viên", "Nhập tên nhân viên:")
        position = simpledialog.askstring("Thêm Nhân Viên", "Nhập chức vụ:")
        salary = simpledialog.askstring("Thêm Nhân Viên", "Nhập mức lương:")
        
        if name and position and salary:
            with open("employees.csv", mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([name, position, salary])
            messagebox.showinfo("Thông báo", f"Nhân viên {name} đã được thêm!")
            self.update_employee_listbox()
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

    def edit_employee(self):
        selected_item = self.employee_listbox.curselection()
        if selected_item:
            name = self.employee_listbox.get(selected_item[0]).split(" | ")[0]
            new_position = simpledialog.askstring("Sửa Nhân Viên", "Nhập chức vụ mới:")
            new_salary = simpledialog.askstring("Sửa Nhân Viên", "Nhập mức lương mới:")
            if new_position and new_salary:
                employee_data = []
                found = False

                with open("employees.csv", mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 3:
                            if row[0] == name:
                                found = True
                                employee_data.append([name, new_position, new_salary])
                            else:
                                employee_data.append(row)

                if found:
                    with open("employees.csv", mode='w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerows(employee_data)
                    messagebox.showinfo("Thông báo", f"Nhân viên {name} đã được sửa!")
                    self.update_employee_listbox()
                else:
                    messagebox.showerror("Lỗi", f"Nhân viên '{name}' không tồn tại!")
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhân viên để sửa!")

    def delete_employee(self):
        selected_item = self.employee_listbox.curselection()
        if selected_item:
            name = self.employee_listbox.get(selected_item[0]).split(" | ")[0]
            employee_data = []
            found = False

            with open("employees.csv", mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 3:
                        if row[0] != name:
                            employee_data.append(row)
                        else:
                            found = True

            if found:
                with open("employees.csv", mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(employee_data)
                messagebox.showinfo("Thông báo", f"Nhân viên {name} đã được xóa!")
                self.update_employee_listbox()
            else:
                messagebox.showerror("Lỗi", f"Nhân viên '{name}' không tồn tại!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhân viên để xóa!")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class OrderScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.selected_table = None
        self.selected_dishes = []
        self.total_price = 0
        self.setup()

    def setup(self):
        self.clear_screen()

        
        tk.Label(self.root, text="Chọn Bàn", font=("Arial", 14, "bold")).pack(pady=10)
        self.table_listbox = tk.Listbox(self.root, width=50)
        self.table_listbox.pack(pady=5)
        self.update_table_listbox()
        
        tk.Button(self.root, text="Chọn Bàn", command=self.select_table).pack(pady=5)

        
        tk.Label(self.root, text="Gọi Món", font=("Arial", 14, "bold")).pack(pady=10)
        self.menu_listbox = tk.Listbox(self.root, width=50)
        self.menu_listbox.pack(pady=5)
        self.update_menu_listbox()
        
        tk.Button(self.root, text="Gọi Món", command=self.order_dishes).pack(pady=5)

        
        tk.Button(self.root, text="Xác Nhận Đơn Hàng", command=self.confirm_order).pack(pady=20)

        
        tk.Button(self.root, text="Xem Đơn Hàng", command=self.view_order).pack(pady=5)

        
        tk.Button(self.root, text="Sửa Bàn", command=self.edit_table).pack(pady=5)

       
        tk.Button(self.root, text="Xóa Món", command=self.edit_dish).pack(pady=5)
        tk.Button(self.root, text="Quay lại", command=self.app.show_customer_screen).pack(pady=5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def update_table_listbox(self):
        self.table_listbox.delete(0, tk.END)
        try:
            with open('table.csv', mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row and row[2].strip().lower() == "trống":
                        self.table_listbox.insert(tk.END, f"{row[0]} - {row[1]}")
                    
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file 'table.csv'.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

    def update_menu_listbox(self):
        self.menu_listbox.delete(0, tk.END)
        try:
            with open('menu.csv', mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  
                for row in reader:
                    if row: 
                        self.menu_listbox.insert(tk.END, f"{row[0]} - {row[1]} - {row[2]} VND") 
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file 'menu.csv'.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

    def select_table(self):
        try:
            self.selected_table = self.table_listbox.get(self.table_listbox.curselection())
            messagebox.showinfo("Thông báo", f"Bạn đã chọn bàn: {self.selected_table}")
        except tk.TclError:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một bàn.")

    def order_dishes(self):
        try:
            selected_dish = self.menu_listbox.get(self.menu_listbox.curselection())
            dish_name = selected_dish.split(' - ')[0]
            dish_price = int(selected_dish.split(' - ')[2].replace(" VND", ""))

            self.selected_dishes.append((dish_name, dish_price))
            self.total_price += dish_price
            messagebox.showinfo("Thông báo", f"Bạn đã gọi món: {dish_name} - {dish_price} VND")
        except tk.TclError:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một món ăn.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

    def confirm_order(self):
        if not self.selected_table or not self.selected_dishes:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn bàn và gọi món.")
            return
        
        order_details = f"Bàn: {self.selected_table}\n"
        order_details += "Món đã gọi:\n"
        for dish, price in self.selected_dishes:
            order_details += f"- {dish}: {price} VND\n"
        order_details += f"Tổng tiền: {self.total_price} VND\n"

        messagebox.showinfo("Xác Nhận Đơn Hàng", order_details)

       
        self.save_order()

    def save_order(self):
        try:
            with open('orders.csv', mode='a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.app.current_user.username, self.selected_table,
                                 ', '.join(dish[0] for dish in self.selected_dishes),
                                 self.total_price]) 
                # Thêm thông tin đơn hàng vào orders.csv
            messagebox.showinfo("Thông báo", "Đơn hàng đã được lưu.")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi lưu đơn hàng: {e}")

    def view_order(self):
        if not self.selected_table or not self.selected_dishes:
            messagebox.showwarning("Cảnh báo", "Chưa có đơn hàng nào để hiển thị.")
            return
        
        order_details = f"Bàn: {self.selected_table}\n"
        order_details += "Món đã gọi:\n"
        for dish, price in self.selected_dishes:
            order_details += f"- {dish}: {price} VND\n"
        order_details += f"Tổng tiền: {self.total_price} VND\n"

        messagebox.showinfo("Đơn Hàng", order_details)

    def edit_table(self):
        
        pass

    def edit_dish(self):
        try:
           
            if not self.selected_dishes:
                messagebox.showwarning("Cảnh báo", "Chưa có món nào để sửa.")
                return

            dishes_list = "\n".join(f"{i+1}. {dish[0]} - {dish[1]} VND" for i, dish in enumerate(self.selected_dishes))
            dish_to_delete_index = simpledialog.askinteger("Chọn Món", f"Chọn số món để xóa:\n{dishes_list}")

            if dish_to_delete_index is None or dish_to_delete_index < 1 or dish_to_delete_index > len(self.selected_dishes):
                messagebox.showwarning("Cảnh báo", "Số món không hợp lệ.")
                return

            
            old_dish = self.selected_dishes[dish_to_delete_index - 1]
            self.selected_dishes.pop(dish_to_delete_index - 1) 
            self.total_price -= old_dish[1] 

            messagebox.showinfo("Thông báo", f"Đã xóa món '{old_dish[0]}' khỏi đơn hàng.")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

class InvoiceScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup()

    def setup(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Hóa Đơn", font=("Arial", 14, "bold")).pack(pady=10)
        
        
        self.order_listbox = tk.Listbox(self.root, width=80, height=10)
        self.order_listbox.pack(pady=10)

        self.update_order_listbox()  
        tk.Button(self.root, text="Quay lại", command=self.app.show_admin_screen).pack(pady=5)

        
        self.show_invoice_statistics()

    def show_invoice_statistics(self):
        total_orders = 0
        total_revenue = 0
        
        try:
            with open('orders.csv', mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    total_orders += 1
                    total_revenue += float(row[3])  
        
           
            tk.Label(self.root, text=f"Tổng số đơn hàng: {total_orders}", font=("Arial", 12)).pack(pady=5)
            tk.Label(self.root, text=f"Tổng doanh thu: {total_revenue} VND", font=("Arial", 12)).pack(pady=5)
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file 'orders.csv'.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

    def update_order_listbox(self):
        """Cập nhật nội dung của Listbox từ file orders.csv."""
        self.order_listbox.delete(0, tk.END) 
        try:
            with open("orders.csv", mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  
                for row in reader:
                    if len(row) >= 4:  
                        self.order_listbox.insert(tk.END, f"Username: {row[0]} | Bàn: {row[1]} | Món: {row[2]} | Tổng tiền: {row[3]} VND")
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file danh sách hóa đơn!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class OrderHistoryScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup()

    def setup(self):
        self.clear_screen()
        self.order_listbox = tk.Listbox(self.root, width=70)
        self.order_listbox.pack(pady=20)

        # Nút xem lịch sử hóa đơn
        tk.Button(self.root, text="Xem Lịch Sử Đơn Hàng", command=self.load_order_history).pack(pady=10)
        tk.Button(self.root, text="Quay lại", command=self.app.show_customer_screen).pack(pady=5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_order_history(self):
        if not self.app.current_user: 
            messagebox.showwarning("Cảnh báo", "Chưa đăng nhập. Vui lòng đăng nhập trước.")
            return

        try:
            with open('orders.csv', mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader) 
                self.order_listbox.delete(0, tk.END) 
                for row in reader:
                    if row and row[0] == self.app.current_user.username: 
                        self.order_listbox.insert(tk.END, f" {row[1]},  {row[2]},  {row[3]} VND")
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file 'orders.csv'.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

class MenuScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup()

    def setup(self):
        self.clear_screen()

        tk.Label(self.root, text="Quản lý Thực đơn", font=("Arial", 14, "bold")).pack(pady=10)

       
        self.menu_listbox = tk.Listbox(self.root, width=50, height=10)
        self.menu_listbox.pack(pady=10)

       
        tk.Button(self.root, text="Xem Thực Đơn", command=self.show_menu).pack(pady=5)
        tk.Button(self.root, text="Thêm món ăn", command=self.add_food).pack(pady=5)
        tk.Button(self.root, text="Sửa món ăn", command=self.edit_food).pack(pady=5)
        tk.Button(self.root, text="Xóa món ăn", command=self.delete_food).pack(pady=5)
        tk.Button(self.root, text="Quay lại", command=self.app.show_admin_screen).pack(pady=5)

        
        self.update_menu_listbox()

    def update_menu_listbox(self):
        """Cập nhật nội dung của Listbox từ file thực đơn."""
        self.menu_listbox.delete(0, tk.END)  
        try:
            with open("menu.csv", mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 3: 
                 
                        self.menu_listbox.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]}")
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file thực đơn!")

    def show_menu(self):
        """Hiển thị thực đơn trong Listbox."""
        self.update_menu_listbox() 

    def add_food(self):
        food_name = simpledialog.askstring("Thêm Món Ăn", "Nhập tên món ăn:")
        ingredients = simpledialog.askstring("Thêm Món Ăn", "Nhập nguyên liệu:")
        price = simpledialog.askstring("Thêm Món Ăn", "Nhập giá:")
        
        if food_name and ingredients and price:
            with open("menu.csv", mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([food_name, ingredients, price])
            messagebox.showinfo("Thông báo", f"Món {food_name} đã được thêm!")
            self.update_menu_listbox()
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

    def edit_food(self):
        selected_item = self.menu_listbox.curselection()
        if selected_item:
            food_name = self.menu_listbox.get(selected_item[0]).split(" | ")[0] 
            
            new_ingredients = simpledialog.askstring("Sửa Món Ăn", "Nhập nguyên liệu mới:")
            new_price = simpledialog.askstring("Sửa Món Ăn", "Nhập giá mới:")
            if new_ingredients and new_price:
                menu_items = []
                found = False

               
                with open("menu.csv", mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 3:
                            if row[0] == food_name:
                                found = True
                                menu_items.append([food_name, new_ingredients, new_price])
                            else:
                                menu_items.append(row)

                
                if found:
                    with open("menu.csv", mode='w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerows(menu_items)
                    messagebox.showinfo("Thông báo", f"Món {food_name} đã được sửa!")
                    self.update_menu_listbox()  
                else:
                    messagebox.showerror("Lỗi", f"Món ăn '{food_name}' không tồn tại!")
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn món ăn để sửa!")

    def delete_food(self):
        selected_item = self.menu_listbox.curselection()
        if selected_item:
            food_name = self.menu_listbox.get(selected_item[0]).split(" | ")[0] 
            
            menu_items = []
            found = False

           
            with open("menu.csv", mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 3:
                        if row[0] != food_name:
                            menu_items.append(row)
                        else:
                            found = True

            
            if found:
                with open("menu.csv", mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(menu_items)
                messagebox.showinfo("Thông báo", f"Món {food_name} đã được xóa!")
                self.update_menu_listbox() 
            else:
                messagebox.showerror("Lỗi", f"Món ăn '{food_name}' không tồn tại!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn món ăn để xóa!")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class CustomerManagementScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup()

    def setup(self):
        self.clear_screen()

        tk.Label(self.root, text="Quản lý Khách Hàng", font=("Arial", 14, "bold")).pack(pady=10)

        
        self.customer_listbox = tk.Listbox(self.root, width=60, height=10)
        self.customer_listbox.pack(pady=10)

        
        tk.Button(self.root, text="Xem Danh Sách Khách Hàng", command=self.show_customers).pack(pady=5)
        tk.Button(self.root, text="Quay lại", command=self.app.show_admin_screen).pack(pady=5)

        self.update_customer_listbox()

    def update_customer_listbox(self):
        """Cập nhật nội dung của Listbox từ file users.csv chỉ hiển thị role 'customer'."""
        self.customer_listbox.delete(0, tk.END)
        try:
            with open("users.csv", mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader) 
                for row in reader:
                    if len(row) >= 4 and row[2].strip() == "customer": 
                        self.customer_listbox.insert(tk.END, f"Username: {row[0]}, Thông tin cá nhân: {row[3]}")
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file danh sách người dùng!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

    def show_customers(self):
        """Hiển thị danh sách khách hàng trong Listbox."""
        self.update_customer_listbox()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class RestaurantApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quản lý nhà hàng")
        self.data_manager = DataManager('users.csv', 'menu.csv')
        self.current_user = None
        
        self.root.geometry("600x400")
        
        self.login_screen = LoginScreen(self.root, self)
        self.admin_screen = AdminScreen(self.root, self)
        self.customer_screen = CustomerScreen(self.root, self)
        self.menu_screen = MenuScreen(self.root, self)
        self.employee_screen = EmployeeScreen(self.root, self)
        self.add_user_screen = AddUserScreen(self.root, self)
        self.table_screen = TableScreen(self.root, self)
        self.order_screen = OrderScreen(self.root, self)
        self.order_history_screen = OrderHistoryScreen(self.root, self)
        self.invoice_screen = InvoiceScreen(self.root, self)
        self.customer_management_screen = CustomerManagementScreen(self.root, self)
        
        
       
        

        self.show_login_screen()
        
        self.root.mainloop()

    def show_login_screen(self):
        self.login_screen.setup()

    def show_admin_screen(self):
        self.admin_screen.setup()

    def show_customer_screen(self):
        self.customer_screen.setup()

    def show_menu_screen(self):
        self.menu_screen.setup()

    def show_employee_screen(self):
        self.employee_screen.setup()

    def show_add_user_screen(self):
        self.add_user_screen.setup()
    def show_table_screen(self):
        self.table_screen.setup()
    def show_order_screen(self):
        self.order_screen.setup()
    def show_order_history_screen(self):
        self.order_history_screen.setup()
    def show_invoice_screen(self):
        self.invoice_screen.setup()
    def show_customer_management_screen(self):
        self.customer_management_screen.setup()
    

# Khởi động ứng dụng
if __name__ == "__main__":
    RestaurantApp()

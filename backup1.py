# Import
import sys
import os
from datetime import datetime

# Statement
my_courses= []
users= {}
current_user=""
input_path =sys.argv[1]
output_path =sys.argv[2]

# Utility function
def add_course(courselist,course):
    courselist.append(course)

def remove_course(courselist,code):
    fd = search_code(courselist,code)
    if fd is None:
        input("Course not exist\nPress return to continue")
        return False
    courselist.remove(fd)
    return True

def search_code(courselist,code):
    target_code=code.upper()
    for tmp in courselist:
        if tmp["course_code"].upper()==target_code:
            return tmp       #return the staff or None
    return None

def search_keyword(courselist,keyword):
    kw = keyword.lower()
    out=[]
    for tmp in courselist:
        if kw in tmp["course_title"].lower():
            out.append(tmp)
    return out

# File/System Function Area
def read_input(path):
    f = open(path)

    line_no = 0
    for line in f:
        line_no=line_no+1
        text = line.strip()
        if text=="":
            continue
        attri = text.split("|")
        # C|username|code|title|term|professor|status|remark
        if len(attri) != 8 or attri[0] != "C":
            continue
        username, code, title, term, professor, status, remark = attri[1:]
        level = 0
        for i in code:
            if i.isdigit():
                level = int(i) * 1000
                break

        add_course(my_courses, {
            "username": username.strip(),
            "course_code": code.strip(),
            "course_title": title.strip(),
            "credit": 3,
            "course_level": level,
            "term": term.strip(),
            "professor": professor.strip(),
            "status": status.strip(),
            "remark": remark.strip()
        })
    f.close()

def save_input():
    kept = []
    f = open(input_path, "r")
    for line in f:
        text = line.strip()
        if text == "":
            continue
        attri = text.split("|")
        if attri[0] == "U":
            continue
        if attri[0] == "C" and len(attri) >= 2 and attri[1] == current_user:
            continue
        kept.append(text)
    f.close()

    f = open(output_path, "w")
    for username in users:
        f.write("U|" + username + "|" + users[username] + "\n")
    for text in kept:
        f.write(text + "\n")
    for course in my_courses:
        line = "|".join([
            "C",
            course["username"],
            course["course_code"],
            course["course_title"],
            course["term"],
            course["professor"],
            course["status"],
            course["remark"],
        ])
        f.write(line + "\n")
    f.close()

# Read accounts from the input file. Each account line is U|username|password.
def load_users():
    users.clear()
    try:
        f = open(input_path, "r")
    except OSError:
        print("Cannot open input file: " + input_path)
        sys.exit()

    for line in f:
        line = line.strip()
        if line != "":
            parts = line.split("|")
            if len(parts) >= 3 and parts[0] == "U":
                # Second field is the username, third is the password.
                username = parts[1]
                password = parts[2]
                users[username] = password
    f.close()

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.environ["TERM"] = "xterm-256color"    #pretend error alarm
        os.system("clear")




# core function pls put here in order
# 1
def courseinfo_function():

    print("                  ==MY COURSES==                     ")
    
    print("add courses(a)   remove courses(r)   specific info(s)\n")
    
    #show all of my courses
    for course in my_courses:
        print(f"{course['course_code']:<14}{course['course_title']}")
    print()
    print("Quit(q)")
    ch = input("What's next? ")

    if ch == "a":
        code = input("Input course code: ")
        level = 0
        for i in code:
            if i.isdigit():
                level = int(i) * 1000
                break
        add_course(my_courses, {
            "username": current_user,
            "course_code": code,
            "course_title": input("Input course name: "),
            "credit": 3,
            "course_level": level,
            "term": input("Input term: "),
            "professor": input("Input professor: "),
            "status": input("Input status: "),
            "remark": None
        })
        clear_screen()
        courseinfo_function()
    elif ch == "r":
        code = input("Input course code: ")
        if remove_course(my_courses, code):
            print("Removed")
        else:
            print("Course not found")
        clear_screen()
        courseinfo_function()
    elif ch == "s":
        string = input("Input course code or title: ")
        if string[-4].isdigit():
            tmp="cod"
        else:
            tmp="key"
        if tmp == "cod":
            fc = search_code(my_courses, string)
            if fc is None:
                print("Not found?")
            else:
                print("=========================================================")
                print(fc["course_code"])
                print(fc["course_title"])
                print("---------------------------------------------------------")
                print("Credit : ",fc["credit"],"\t","Level : ",fc["course_level"])
                print("Term : ",fc["term"])
                print("Prof : ",fc["professor"])
                print("Status : ",fc["status"])
                print("Remark : ",fc["remark"])
            input("Press to return")
        elif tmp == "key":
            fc = search_keyword(my_courses,string)
            if fc == []:
                print("Course not found")
            else:
                for course in fc:
                    print("=========================================================")
                    print(course["course_code"])
                    print(course["course_title"])
                    print("---------------------------------------------------------")
                    print("Credit : ",course["credit"],"\t","Level : ",course["course_level"])
                    print("Term : ",course["term"])
                    print("Prof : ",course["professor"])
                    print("Status : ",course["status"])
                    print("Remark : ",course["remark"])
                    print()
            input("Press Enter to go back")
        clear_screen()
        courseinfo_function()
    else:
        return

# 2
def time_function():
    RED = "\033[91m"  # turn to red
    END = "\033[0m"  # stop the red
    form_list = []

    def show_list():
        """打印全部待办：按日期、优先级排序；日期等于今天的整行标红"""
        print("\n===== Todo List =====")
        if len(form_list) == 0:
            print("(empty)")
            print("-" * 50)
            return

        # 排序：先按日期，日期相同再按优先级
        form_list.sort(key=lambda x: (x["date"], x["priority"]))

        today = datetime.now().date()  # 当天日期

        for item in form_list:
            line = (f"{item['date'].date()}\t\t{item['thing']}\t\t"
                    f"{item['class_name']}\t\t{item['priority']}")

            # 关键判断：输入日期与当天日期相同 → 标红
            if item["date"].date() == today:
                print(f"{RED}{line}{END}")
            else:
                print(line)

        print("-" * 50)

    print("To Do List")
    print("add new items (a) \t remove items (r) \t quit (q)")
    print("***********************************************************")

    while True:
        se = input("any decision or quit (q): ").strip().lower()

        # ---------- 退出 ----------
        if se == "q":
            print("Bye")
            break

        # ---------- 添加 ----------
        elif se == "a":
            a = input("please put your date (YYYY-MM-DD): ").strip()
            b = input("put the things: ").strip()
            c = input("put the class name: ").strip()
            d = input("put the priority (1 is highest): ").strip()

            # 日期字符串转换成 datetime 对象，方便排序和比较
            try:
                date_obj = datetime.strptime(a, "%Y-%m-%d")
            except ValueError:
                print("Wrong date format, please use YYYY-MM-DD")
                continue

            # 优先级转换成整数，方便比较
            try:
                priority = int(d)
            except ValueError:
                print("Priority must be an integer")
                continue

            form = {
                "date": date_obj,
                "thing": b,
                "class_name": c,
                "priority": priority
            }
            form_list.append(form)
            print("Added successfully")

        # ---------- 删除 ----------
        elif se == "r":
            # 第一步：先按日期找出所有同一天的记录
            de = input("which day's item do you want to remove (YYYY-MM-DD): ").strip()
            same_date_list = []
            for item in form_list:
                if str(item["date"].date()) == de:
                    same_date_list.append(item)

            # 这一天没有记录
            if len(same_date_list) == 0:
                print("No item on this day")
                continue

            # 第二步：列出这一天所有事项并编号
            print(f"Items on {de}:")
            for i, item in enumerate(same_date_list, start=1):
                print(f"{i}. {item['thing']} | {item['class_name']} | priority {item['priority']}")

            # 第三步：如果这一天有多个事项，让用户选编号
            if len(same_date_list) > 1:
                choice = input("Enter the number you want to delete (0 = cancel): ").strip()
                if not choice.isdigit():
                    print("Invalid input")
                    continue
                idx = int(choice)
                if idx == 0:
                    print("Cancelled")
                    continue
                if idx < 1 or idx > len(same_date_list):
                    print("No such number")
                    continue
                target = same_date_list[idx - 1]
            else:
                # 只有一个，直接删
                target = same_date_list[0]

            form_list.remove(target)
            print("Removed successfully")

        # ---------- 其他输入 ----------
        else:
            print("Unknown command, please type a / r / q")

        # 每次操作完都刷新一次列表（排序 + 标红）
        show_list()

# 3

# 4

# 5
def overview_function():
    while True:
        clear_screen()

        total_courses = len(my_courses)
        total_credits = 0
        term_credits = {}
        term_counts = {}
        status_counts = {}

        for course in my_courses:
            cred = course["credit"]
            total_credits = total_credits + cred

            term = course["term"]
            if term == "":
                term = "Unknown"
            if term not in term_credits:
                term_credits[term] = 0
                term_counts[term] = 0
            term_credits[term] = term_credits[term] + cred
            term_counts[term] = term_counts[term] + 1

            status = course["status"]
            if status == "":
                status = "Unknown"
            if status not in status_counts:
                status_counts[status] = 0
            status_counts[status] += 1
            status_counts[status] = status_counts[status] + 1

        print("=========================================================")
        print("              ==PERSONAL DATA OVERVIEW==                 ")
        print("=========================================================")
        print("User Name      : " + current_user)
        print("Total Courses  : " + str(total_courses))
        print("Total Credits  : " + str(total_credits))
        print("---------------------------------------------------------")

        print("[Credits by Term]")
        if total_courses == 0:
            print("No course records yet.")
        else:
            for term in term_credits:
                c_num = term_counts[term]
                c_cred = term_credits[term]
                warning = ""
                if c_cred < 12:
                    warning = " (Below 12 credits)"
                elif c_cred > 18:
                    warning = " (Over 18 credits)"
                print(
                    "  " + term + " : "
                    + str(c_num) + " course(s), "
                    + str(c_cred) + " credits"
                    + warning
                )

        print("---------------------------------------------------------")
        print("[Courses by Status]")
        if total_courses == 0:
            print("No status records yet.")
        else:
            for st in status_counts:
                print("  " + st + " : " + str(status_counts[st]) + " course(s)")

        print("---------------------------------------------------------")
        print("[Selected Courses Summary]")
        if total_courses == 0:
            print("(Empty)")
        else:
            print("Code | Title | Term | Credit | Status")
            print("---------------------------------------------------------")
            for course in my_courses:
                print(
                    course["course_code"] + " | "
                    + course["course_title"] + " | "
                    + course["term"] + " | "
                    + str(course["credit"]) + " | "
                    + course["status"]
                )
        print("=========================================================")
        print()
        print("Export to txt(e)   Quit(q)")
        ch = input("What's next? ")

        if ch == "e":
            export_name = "overview_" + current_user + ".txt"
            f = open(export_name, "w")
            f.write("=========================================================\n")
            f.write("              ==PERSONAL DATA OVERVIEW==                 \n")
            f.write("=========================================================\n")
            f.write("User Name      : " + current_user + "\n")
            f.write("Total Courses  : " + str(total_courses) + "\n")
            f.write("Total Credits  : " + str(total_credits) + "\n")
            f.write("---------------------------------------------------------\n")
            f.write("[Credits by Term]\n")
            for term in term_credits:
                f.write(
                    "  " + term + " : "
                    + str(term_counts[term]) + " course(s), "
                    + str(term_credits[term]) + " credits\n"
                )
            f.write("---------------------------------------------------------\n")
            f.write("[Courses by Status]\n")
            for st in status_counts:
                f.write("  " + st + " : " + str(status_counts[st]) + " course(s)\n")
            f.write("---------------------------------------------------------\n")
            f.write("[Selected Courses Summary]\n")
            for course in my_courses:
                line = (
                    course["course_code"] + " | "
                    + course["course_title"] + " | "
                    + course["term"] + " | "
                    + str(course["credit"]) + " credits | "
                    + course["status"] + "\n"
                )
                f.write(line)
            f.close()
            print("Saved to " + export_name)
            input("Press Enter to continue")
        elif ch == "q":
            return




#Sign up/ Login from Jerry
def login_function():
    global current_user
    load_users()

    while True:
        print("\n--- Login System ---")
        print("1. Create account")
        print("2. Log in")
        print("3. Log out")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            # Ask for a new username and password.
            username = input("Enter a new username: ").strip()
            password = input("Enter a new password: ").strip()

            # Check the details before creating the account.
            if username == "" or password == "":
                print("Username and password cannot be empty.")
            elif "|" in username or "|" in password:
                print("Please do not use |.")
            elif username in users:
                print("This username already exists.")
            else:
                # Keep the new account in memory. It is written to the output file on save.
                users[username] = password
                print("Account created!")

        elif choice == "2":
            if current_user != "":
                print("Please log out first.")
            else:
                username = input("Username: ").strip()
                password = input("Password: ").strip()

                # Check that the username exists and the password matches.
                if username in users and users[username] == password:
                    current_user = username
                    print("Welcome, " + current_user + "!")
                    return current_user
                else:
                    print("Incorrect username or password.")

        elif choice == "3":
            if current_user == "":
                print("You are not logged in.")
            else:
                # Clear the login status without deleting the account.
                current_user = ""
                print("You have logged out.")

        elif choice == "4":
            print("Goodbye!")
            return ""

        else:
            print("Please enter 1, 2, 3, or 4.")
login_function()
clear_screen()
if current_user == "":
    save_input()
    sys.exit()



#Some Set up
read_input(input_path)
mine = []
for course in my_courses:
    if course["username"] == current_user:
        mine.append(course)
my_courses = mine



# Main interface
while True:
    print("\n")
    print("       ========Study Information Assistance========       \n")
    print("               Course Information Inquiry(1)\n")
    print("               To-do list(2)\n")
    print("               Timetable(3)\n")
    print("               GEN Subject Suggestion(4)\n")
    print("               Personal Data Overview(5)\n")

    ans = input()
    clear_screen()

    if ans == "1":
        courseinfo_function()
        save_input()
        clear_screen()
    elif ans == "2":
        time_function()
    elif ans == 3:
        credit_function()
    elif ans == 4:
        gen_function()
    elif ans == "5":
        overview_function()
        clear_screen()
    else:
        save_input()
        sys.exit()




'''        
被遗弃的计划/代码
def write_output(path):
    f = open(path, "w")
    for course in my_courses:
        line = "|".join([
            course["course_code"],
            course["course_title"],
            course["term"],
            course["professor"],
            course["status"],
            course["remark"],
        ])
        f.write(line + "\n")
    f.close()
'''

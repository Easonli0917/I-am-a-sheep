#######################概念說明#######################
# 這個程式展示Python中函式作為參數傳遞以及裝飾器的概念
# 裝飾器是Python中的高級特性，用於在不修改原函式的情況下添加功能

#######################基礎概念：函式作為參數#######################
# 定義一個普通函式
def say_hello():
    # 印出問候訊息
    print("Hello !")


# 定義一個函式，參數 func 代表「要被執行的函式」
def run_with_announce(func):
    # 在執行函式前先印出提示
    print("Running...")
    # 執行傳進來的函式
    func()
    # 執行完後印出提示
    print("Done.")


# 顯示直接呼叫的方式
print("直接呼叫:")
# 直接呼叫 say_hello 函式
say_hello()

print()
print("透過 run_with_announce 呼叫:")

# 把 say_hello 函式當成參數傳進 run_with_announce
# 注意：這裡是 say_hello，不是 say_hello()（不要加括號）
run_with_announce(say_hello)

print("---------------------")


# =========================================================
######################### 裝飾器範例一 ##########################
# 不帶參數的簡單裝飾器
# =========================================================
# 定義一個裝飾器函式
# func 代表被包裝的原始函式
def gift_wrap(func):
    # wrapper 是包裝後的新函式
    def wrapper():
        # 在執行原函式前做的事：打包禮物
        print("Wrapping the gift...")
        # 執行原本的函式
        func()
        # 執行原函式後做的事：禮物打包完成
        print("Gift wrapped!")

    # 回傳包裝後的函式
    return wrapper


# 重新定義 say_hello 函式
def say_hello():
    # 印出問候訊息
    print("Hello !")


# 手動使用裝飾器
# 把 say_hello 傳進 gift_wrap，獲得被包裝的新函式
# 再把回傳的 wrapper 存回 say_hello 變數
say_hello = gift_wrap(say_hello)

# 這時呼叫 say_hello()
# 其實是在呼叫 wrapper()，會執行完整的包裝流程
say_hello()


# =========================================================
######################### 裝飾器範例二 ##########################
# 帶參數的裝飾器（可重複使用）
# =========================================================
# 定義一個「帶參數的裝飾器」
# name：指令名稱，例如 hello
# description：指令說明，例如 打招呼
def register_command(name, description):  # 外層：接收裝飾器參數
    # 當裝飾器被建立時，先印出登記指令的訊息
    print(f"[登記] 指令 /{name}: {description}")

    # 定義真正的裝飾器
    # func 代表被裝飾的原始函式
    def decorator(func):  # 中層：接收函式
        # 定義包裝函式
        # 之後呼叫原本函式時，其實會執行 wrapper
        def wrapper():  # 內層：包裝函式
            # 在執行原本函式前，先印出執行指令的訊息
            print(f"[執行] 指令 /{name}")
            # 執行原本被裝飾的函式
            func()

        # 回傳包裝後的新函式
        return wrapper

    # 回傳真正的裝飾器 decorator
    return decorator

# 使用 @ 符號應用裝飾器（語法糖）
# 相當於：hello_command = register_command(name="hello", description="打招呼")(hello_command)
@register_command(name="hello", description="打招呼")
def hello_command():
    # 顯示hello指令的功能
    print("你好！我是 hello 指令！")
# 定義一個簡單函式
def say_hello():
    print("Hello!")
# 定義一個可以接收函式當作參數的函式
def run_with_announce(func):
    print("準備完畢...")
    func()
    print("完畢!")

print("直接呼叫函式:")
say_hello()# 呼叫函式

print()
print("透過 run_with_announce 呼叫")
run_with_announce (say_hello)

print("=================")
#===============================================
# 第二段包裝函示
#===============================================
# 核心概念 用一個函式把另一個函式包起來
# 就像在禮物外面包一層包裝紙
def gift_wrap(func):
    def wrapped():
        print("前置動作")
        func()
        print("後置動作")
    return wrapped
def say_hello():
    print("Hello!")
# 手動包裝:把say_hello傳進去,得到包裝後的新版本
say_hello = gift_wrap(say_hello)
# 現在的 say_hello 已經式包裝後的版本
say_hello()
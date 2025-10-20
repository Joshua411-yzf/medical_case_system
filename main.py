import tkinter as tk
from gui import MedicalSystemGUI
import sys

def main():
    """主函数"""
    try:
        root = tk.Tk()
        app = MedicalSystemGUI(root)
        
        # 设置关闭窗口时的操作
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        print("🎉 古今医案查询系统启动成功！")
        print("📚 功能包括：医案查询、学习计划、浏览历史、添加医案、修改医案、删除医案")
        root.mainloop()
        
    except Exception as e:
        print(f"❌ 系统启动失败: {e}")
        print("\n💡 解决方案:")
        print("1. 请确保MySQL服务器正在运行")
        print("2. 请运行初始化脚本: python init_database.py")
        print("3. 检查数据库连接配置")
        input("\n按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()
import mysql.connector
from init_database import init_database
def reset_database():
    """重置数据库：删除并重新创建"""
    try:
        # 连接MySQL服务器（不指定数据库）
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Yzf123456!"
        )
        cursor = conn.cursor()
        
        print("🔄 开始重置数据库...")
        
        # 删除数据库（如果存在）
        cursor.execute("DROP DATABASE IF EXISTS medical_case_system")
        print("✅ 旧数据库删除成功")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ 数据库重置完成，现在运行初始化...")
        
        # 调用初始化函数
        init_database()
        
    except mysql.connector.Error as err:
        print(f"❌ 数据库重置失败: {err}")

if __name__ == "__main__":
    reset_database()
import mysql.connector

def init_database():
    """初始化数据库和表结构"""
    try:
        # 连接MySQL服务器（不指定数据库）
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Yzf123456!"
        )
        cursor = conn.cursor()
        
        print("🚀 开始初始化数据库...")
        
        # 创建数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS medical_case_system")
        cursor.execute("USE medical_case_system")
        print("✅ 数据库创建/连接成功: medical_case_system")
        
        # 创建医案表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medical_records (
                record_id VARCHAR(20) PRIMARY KEY,
                patient VARCHAR(100),
                symptoms TEXT,
                diagnosis TEXT,
                prescription TEXT
            )
        """)
        print("✅ 数据表创建成功: medical_records")
        
        # 检查是否已有数据
        cursor.execute("SELECT COUNT(*) FROM medical_records")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("📝 正在插入示例数据...")
            # 插入示例数据
            sample_data = [
                ("001", "张仲景", "发热恶寒，头项强痛，脉浮", "太阳伤寒", "麻黄汤：麻黄、桂枝、杏仁、甘草"),
                ("002", "李东垣", "发热汗出，恶风，脉缓", "太阳中风", "桂枝汤：桂枝、芍药、甘草、生姜、大枣"),
                ("003", "叶天士", "寒热往来，口苦咽干，胸胁苦满", "少阳病", "小柴胡汤：柴胡、黄芩、半夏、人参、甘草、生姜、大枣"),
                ("004", "吴鞠通", "发热不恶寒，口渴，汗出", "阳明经证", "白虎汤：石膏、知母、甘草、粳米"),
                ("005", "王孟英", "腹满而痛，大便不通，潮热谵语", "阳明腑证", "大承气汤：大黄、厚朴、枳实、芒硝"),
                ("006", "张锡纯", "四肢厥逆，下利清谷，脉微细", "少阴病", "四逆汤：附子、干姜、甘草"),
                ("007", "朱丹溪", "心烦不得眠，口燥咽干", "少阴热化证", "黄连阿胶汤：黄连、黄芩、芍药、鸡子黄、阿胶"),
                ("008", "孙思邈", "腹痛，自利，口不渴", "太阴病", "理中汤：人参、白术、干姜、甘草"),
                ("009", "钱乙", "消渴，气上冲心，心中疼热", "厥阴病", "乌梅丸：乌梅、细辛、干姜、黄连、附子、当归、黄柏、桂枝、人参、花椒"),
                ("010", "扁鹊", "头痛发热，汗出恶风", "太阳中风", "桂枝加葛根汤：桂枝、芍药、甘草、生姜、大枣、葛根")
            ]
            
            for data in sample_data:
                cursor.execute("""
                    INSERT INTO medical_records (record_id, patient, symptoms, diagnosis, prescription)
                    VALUES (%s, %s, %s, %s, %s)
                """, data)
                print(f"  ✅ 插入: {data[0]} - {data[1]}")
            
            print(f"✅ 成功插入 {len(sample_data)} 条示例医案")
        else:
            print(f"ℹ️  数据库中已有 {count} 条医案记录，跳过示例数据插入")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n🎉 数据库初始化完成！")
        print("📊 数据库名称: medical_case_system")
        print("📋 表名称: medical_records")
        print("💡 现在可以运行主程序: python main.py")
        
    except mysql.connector.Error as err:
        print(f"❌ 数据库初始化失败: {err}")
        print("\n请检查:")
        print("1. MySQL服务器是否正在运行")
        print("2. 用户名和密码是否正确")
        print("3. 是否有创建数据库的权限")

if __name__ == "__main__":
    init_database()
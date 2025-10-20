import mysql.connector
from data_structures import MedicalRecord

class DatabaseManager:
    """数据库管理类"""
    def __init__(self, host="localhost", user="root", password="Yzf123456!", database="medical_case_system"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.connect()
    
    def connect(self):
        """连接数据库"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print(f"✅ 数据库连接成功: {self.database}")
        except mysql.connector.Error as err:
            if err.errno == 1049:  # Unknown database
                print(f"❌ 数据库 '{self.database}' 不存在")
                print("请先运行初始化脚本: python init_database.py")
                raise
            else:
                print(f"❌ 数据库连接失败: {err}")
                raise
    
    def check_table_exists(self):
        """检查表是否存在"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES LIKE 'medical_records'")
            result = cursor.fetchone()
            cursor.close()
            return result is not None
        except mysql.connector.Error as err:
            print(f"检查表失败: {err}")
            return False
    
    def load_all_records(self):
        """从数据库加载所有医案"""
        records = []
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM medical_records ORDER BY record_id")
            results = cursor.fetchall()
            
            for row in results:
                record = MedicalRecord(row[0], row[1], row[2], row[3], row[4])
                records.append(record)
            
            cursor.close()
            print(f"✅ 成功加载 {len(records)} 条医案记录")
        except mysql.connector.Error as err:
            print(f"❌ 加载医案失败: {err}")
        
        return records
    
    def add_record(self, record):
        """添加新医案到数据库"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO medical_records (record_id, patient, symptoms, diagnosis, prescription)
                VALUES (%s, %s, %s, %s, %s)
            """, (record.record_id, record.patient, record.symptoms, record.diagnosis, record.prescription))
            self.connection.commit()
            cursor.close()
            print(f"✅ 成功添加医案: {record.record_id}")
            return True
        except mysql.connector.IntegrityError:
            print(f"❌ 医案编号 {record.record_id} 已存在")
            return False
        except mysql.connector.Error as err:
            print(f"❌ 添加医案失败: {err}")
            return False

    def update_record(self, record_id, patient, symptoms, diagnosis, prescription):
        """更新医案信息"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE medical_records 
                SET patient = %s, symptoms = %s, diagnosis = %s, prescription = %s
                WHERE record_id = %s
            """, (patient, symptoms, diagnosis, prescription, record_id))
            
            affected_rows = cursor.rowcount
            self.connection.commit()
            cursor.close()
            
            if affected_rows > 0:
                print(f"✅ 成功更新医案: {record_id}")
                return True
            else:
                print(f"❌ 未找到医案: {record_id}")
                return False
                
        except mysql.connector.Error as err:
            print(f"❌ 更新医案失败: {err}")
            return False

    def delete_record(self, record_id):
        """删除医案"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM medical_records WHERE record_id = %s", (record_id,))
            
            affected_rows = cursor.rowcount
            self.connection.commit()
            cursor.close()
            
            if affected_rows > 0:
                print(f"✅ 成功删除医案: {record_id}")
                return True
            else:
                print(f"❌ 未找到医案: {record_id}")
                return False
                
        except mysql.connector.Error as err:
            print(f"❌ 删除医案失败: {err}")
            return False
    
    def get_record_count(self):
        """获取医案数量"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM medical_records")
            count = cursor.fetchone()[0]
            cursor.close()
            return count
        except mysql.connector.Error as err:
            print(f"获取记录数量失败: {err}")
            return 0
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            print("✅ 数据库连接已关闭")
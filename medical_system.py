from data_structures import LinkList, LinkStack, LinkQueue, MedicalRecord
from database import DatabaseManager

class MedicalSystem:
    """主系统类"""
    def __init__(self):
        self.record_list = LinkList()  # 医案库
        self.browse_history = LinkStack()  # 浏览历史
        self.study_plan = LinkQueue()  # 学习计划
        self.db_manager = None
        self.initialize_database()
    
    def initialize_database(self):
        """初始化数据库连接"""
        try:
            self.db_manager = DatabaseManager()
            # 从数据库加载医案
            self.load_records_from_db()
        except Exception as e:
            print(f"❌ 数据库初始化失败: {e}")
            print("💡 请先运行: python init_database.py")
            raise
    
    def load_records_from_db(self):
        """从数据库加载医案到链表"""
        records = self.db_manager.load_all_records()
        for record in records:
            self.record_list.append(record)
        
        if len(records) == 0:
            print("⚠️  数据库中没有医案数据")
            print("💡 您可以通过'添加医案'功能添加新数据")
        else:
            print(f"✅ 成功加载 {len(records)} 条医案记录到内存")
    
    def search_by_id(self, record_id):
        """根据编号查询医案"""
        record = self.record_list.find_by_id(record_id)
        if record:
            # 添加到浏览历史
            self.browse_history.push(record)
        return record
    
    def search_by_symptoms(self, symptoms_keyword):
        """根据症状关键词查询医案"""
        records = self.record_list.find_by_symptoms(symptoms_keyword)
        if records:
            # 将第一个结果添加到浏览历史
            self.browse_history.push(records[0])
        return records
    
    def add_to_study_plan(self, record_id):
        """添加医案到学习计划"""
        record = self.record_list.find_by_id(record_id)
        if record:
            self.study_plan.enqueue(record)
            return True
        return False
    
    def get_next_study_case(self):
        """获取下一个学习医案"""
        return self.study_plan.dequeue()
    
    def get_browse_history(self):
        """获取浏览历史"""
        return self.browse_history.get_all_items()
    
    def get_study_plan(self):
        """获取学习计划"""
        return self.study_plan.get_all_items()
    
    def get_all_records(self):
        """获取所有医案"""
        return self.record_list.get_all_records()
    
    def add_new_record(self, record_id, patient, symptoms, diagnosis, prescription):
        """添加新医案"""
        # 检查编号是否已存在
        if self.record_list.find_by_id(record_id):
            return False, "医案编号已存在"
        
        new_record = MedicalRecord(record_id, patient, symptoms, diagnosis, prescription)
        
        # 添加到数据库
        if self.db_manager.add_record(new_record):
            # 添加到内存链表
            self.record_list.append(new_record)
            return True, "医案添加成功"
        else:
            return False, "医案添加失败"

    def update_record(self, record_id, patient, symptoms, diagnosis, prescription):
        """更新医案信息"""
        # 先更新数据库
        if self.db_manager.update_record(record_id, patient, symptoms, diagnosis, prescription):
            # 再更新内存中的链表
            if self.record_list.update_by_id(record_id, patient, symptoms, diagnosis, prescription):
                return True, "医案更新成功"
            else:
                return False, "更新内存数据失败"
        else:
            return False, "更新数据库失败"

    def delete_record(self, record_id):
        """删除医案"""
        # 先从学习计划和浏览历史中移除相关记录
        self.remove_from_study_plan(record_id)
        self.remove_from_browse_history(record_id)
        
        # 删除数据库记录
        if self.db_manager.delete_record(record_id):
            # 删除内存链表中的记录
            if self.record_list.delete_by_id(record_id):
                return True, "医案删除成功"
            else:
                return False, "删除内存数据失败"
        else:
            return False, "删除数据库记录失败"

    def remove_from_study_plan(self, record_id):
        """从学习计划中移除医案"""
        new_queue = LinkQueue()
        removed = False
        
        while not self.study_plan.is_empty():
            record = self.study_plan.dequeue()
            if record.record_id != record_id:
                new_queue.enqueue(record)
            else:
                removed = True
        
        self.study_plan = new_queue
        return removed

    def remove_from_browse_history(self, record_id):
        """从浏览历史中移除医案"""
        new_stack = LinkStack()
        removed = False
        
        # 临时存储非目标记录
        temp_list = []
        while not self.browse_history.is_empty():
            record = self.browse_history.pop()
            if record.record_id != record_id:
                temp_list.append(record)
            else:
                removed = True
        
        # 重新入栈（保持原有顺序）
        for record in reversed(temp_list):
            new_stack.push(record)
        
        self.browse_history = new_stack
        return removed
    
    def close(self):
        """关闭系统"""
        if self.db_manager:
            self.db_manager.close()
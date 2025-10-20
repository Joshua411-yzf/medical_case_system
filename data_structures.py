class MedicalRecord:
    """医案数据类"""
    def __init__(self, record_id="", patient="", symptoms="", diagnosis="", prescription=""):
        self.record_id = record_id
        self.patient = patient
        self.symptoms = symptoms
        self.diagnosis = diagnosis
        self.prescription = prescription
    
    def __str__(self):
        return f"编号: {self.record_id}\n患者: {self.patient}\n症状: {self.symptoms}\n诊断: {self.diagnosis}\n处方: {self.prescription}"


class Node:
    """链表节点类"""
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkList:
    """模板类单链表 - 用于存储医案库"""
    def __init__(self):
        self.head = None
        self.size = 0
    
    def is_empty(self):
        return self.head is None
    
    def append(self, data):
        """在链表末尾添加元素"""
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
    
    def find_by_id(self, record_id):
        """根据编号查找医案"""
        current = self.head
        while current:
            if current.data.record_id == record_id:
                return current.data
            current = current.next
        return None
    
    def update_by_id(self, record_id, patient, symptoms, diagnosis, prescription):
        """根据编号更新医案"""
        current = self.head
        while current:
            if current.data.record_id == record_id:
                # 更新医案信息
                current.data.patient = patient
                current.data.symptoms = symptoms
                current.data.diagnosis = diagnosis
                current.data.prescription = prescription
                return True
            current = current.next
        return False
    
    def delete_by_id(self, record_id):
        """根据编号删除医案"""
        if self.is_empty():
            return False
        
        # 如果删除的是头节点
        if self.head.data.record_id == record_id:
            self.head = self.head.next
            self.size -= 1
            return True
        
        # 查找要删除的节点
        current = self.head
        while current.next:
            if current.next.data.record_id == record_id:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        
        return False
    
    def find_by_symptoms(self, symptoms_keyword):
        """根据症状关键词查找医案"""
        results = []
        current = self.head
        while current:
            if symptoms_keyword.lower() in current.data.symptoms.lower():
                results.append(current.data)
            current = current.next
        return results
    
    def get_all_records(self):
        """获取所有医案"""
        records = []
        current = self.head
        while current:
            records.append(current.data)
            current = current.next
        return records
    
    def __len__(self):
        return self.size


class LinkStack:
    """模板类链栈 - 用于存储用户浏览历史"""
    def __init__(self):
        self.top = None
        self.size = 0
    
    def is_empty(self):
        return self.top is None
    
    def push(self, data):
        """入栈"""
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
    
    def pop(self):
        """出栈"""
        if self.is_empty():
            return None
        data = self.top.data
        self.top = self.top.next
        self.size -= 1
        return data
    
    def peek(self):
        """查看栈顶元素"""
        if self.is_empty():
            return None
        return self.top.data
    
    def get_all_items(self):
        """获取栈中所有元素"""
        items = []
        current = self.top
        while current:
            items.append(current.data)
            current = current.next
        return items[::-1]  # 反转列表使其按入栈顺序显示


class LinkQueue:
    """模板类链队列 - 用于存储学习计划"""
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0
    
    def is_empty(self):
        return self.front is None
    
    def enqueue(self, data):
        """入队"""
        new_node = Node(data)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1
    
    def dequeue(self):
        """出队"""
        if self.is_empty():
            return None
        data = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return data
    
    def peek(self):
        """查看队首元素"""
        if self.is_empty():
            return None
        return self.front.data
    
    def get_all_items(self):
        """获取队列中所有元素"""
        items = []
        current = self.front
        while current:
            items.append(current.data)
            current = current.next
        return items
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from medical_system import MedicalSystem

class MedicalSystemGUI:
    """医案系统GUI界面"""
    def __init__(self, root):
        self.root = root
        self.root.title("古今医案查询系统")
        self.root.geometry("900x700")
        
        self.medical_system = MedicalSystem()
        self.current_edit_record_id = None  # 当前正在编辑的医案编号
        
        self.create_widgets()
        self.update_display()
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建选项卡
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 查询选项卡
        self.search_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.search_frame, text="医案查询")
        
        # 学习计划选项卡
        self.study_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.study_frame, text="学习计划")
        
        # 浏览历史选项卡
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="浏览历史")
        
        # 添加医案选项卡
        self.add_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_frame, text="添加医案")
        
        # 修改医案选项卡
        self.edit_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.edit_frame, text="修改医案")
        
        # 删除医案选项卡
        self.delete_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.delete_frame, text="删除医案")
        
        self.setup_search_tab()
        self.setup_study_tab()
        self.setup_history_tab()
        self.setup_add_tab()
        self.setup_edit_tab()
        self.setup_delete_tab()
    
    def setup_search_tab(self):
        """设置查询选项卡"""
        # 查询方式选择
        search_method_frame = ttk.LabelFrame(self.search_frame, text="查询方式", padding=10)
        search_method_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.search_var = tk.StringVar(value="id")
        ttk.Radiobutton(search_method_frame, text="按编号查询", variable=self.search_var, value="id").pack(side=tk.LEFT)
        ttk.Radiobutton(search_method_frame, text="按症状查询", variable=self.search_var, value="symptoms").pack(side=tk.LEFT)
        
        # 查询输入
        search_input_frame = ttk.Frame(self.search_frame)
        search_input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_input_frame, text="查询内容:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_input_frame, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<Return>", lambda e: self.perform_search())
        
        ttk.Button(search_input_frame, text="查询", command=self.perform_search).pack(side=tk.LEFT, padx=5)
        
        # 查询结果
        result_frame = ttk.LabelFrame(self.search_frame, text="查询结果", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, width=80, height=20)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # 操作按钮
        button_frame = ttk.Frame(self.search_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="添加到学习计划", command=self.add_to_study_from_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="修改此医案", command=self.edit_current_search_result).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="删除此医案", command=self.delete_current_search_result).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空结果", command=self.clear_results).pack(side=tk.LEFT, padx=5)
    
    def setup_study_tab(self):
        """设置学习计划选项卡"""
        # 学习计划列表
        list_frame = ttk.LabelFrame(self.study_frame, text="学习计划列表", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.study_listbox = tk.Listbox(list_frame, width=80, height=15)
        self.study_listbox.pack(fill=tk.BOTH, expand=True)
        
        # 操作按钮
        button_frame = ttk.Frame(self.study_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="学习下一个医案", command=self.study_next_case).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="从计划中移除", command=self.remove_from_study_plan).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新列表", command=self.update_display).pack(side=tk.LEFT, padx=5)
        
        # 学习结果显示
        study_result_frame = ttk.LabelFrame(self.study_frame, text="学习内容", padding=10)
        study_result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.study_text = scrolledtext.ScrolledText(study_result_frame, width=80, height=10)
        self.study_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_history_tab(self):
        """设置浏览历史选项卡"""
        # 浏览历史列表
        history_frame = ttk.LabelFrame(self.history_frame, text="浏览历史", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.history_listbox = tk.Listbox(history_frame, width=80, height=20)
        self.history_listbox.pack(fill=tk.BOTH, expand=True)
        
        # 操作按钮
        button_frame = ttk.Frame(self.history_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="查看选中医案", command=self.view_selected_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="添加到学习计划", command=self.add_selected_history_to_study).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="修改选中医案", command=self.edit_selected_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="删除选中医案", command=self.delete_selected_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新列表", command=self.update_display).pack(side=tk.LEFT, padx=5)
    
    def setup_add_tab(self):
        """设置添加医案选项卡"""
        # 医案信息输入
        input_frame = ttk.LabelFrame(self.add_frame, text="医案信息", padding=10)
        input_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        # 编号
        ttk.Label(input_frame, text="编号:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.id_entry = ttk.Entry(input_frame, width=50)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # 患者
        ttk.Label(input_frame, text="患者:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.patient_entry = ttk.Entry(input_frame, width=50)
        self.patient_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # 症状
        ttk.Label(input_frame, text="症状:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.symptoms_text = scrolledtext.ScrolledText(input_frame, width=50, height=4)
        self.symptoms_text.grid(row=2, column=1, padx=5, pady=5)
        
        # 诊断
        ttk.Label(input_frame, text="诊断:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.diagnosis_entry = ttk.Entry(input_frame, width=50)
        self.diagnosis_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # 处方
        ttk.Label(input_frame, text="处方:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.prescription_text = scrolledtext.ScrolledText(input_frame, width=50, height=4)
        self.prescription_text.grid(row=4, column=1, padx=5, pady=5)
        
        # 操作按钮
        button_frame = ttk.Frame(self.add_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="添加医案", command=self.add_new_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空表单", command=self.clear_form).pack(side=tk.LEFT, padx=5)
    
    def setup_edit_tab(self):
        """设置修改医案选项卡"""
        # 选择要修改的医案
        select_frame = ttk.LabelFrame(self.edit_frame, text="选择医案", padding=10)
        select_frame.pack(fill=tk.X, padx=10, pady=5)
        
        select_input_frame = ttk.Frame(select_frame)
        select_input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(select_input_frame, text="医案编号:").pack(side=tk.LEFT)
        self.edit_id_entry = ttk.Entry(select_input_frame, width=20)
        self.edit_id_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(select_input_frame, text="加载医案", command=self.load_record_for_edit).pack(side=tk.LEFT, padx=5)
        ttk.Button(select_input_frame, text="从列表选择", command=self.show_record_selector).pack(side=tk.LEFT, padx=5)
        
        # 医案信息编辑
        edit_input_frame = ttk.LabelFrame(self.edit_frame, text="编辑医案信息", padding=10)
        edit_input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 编号（不可编辑）
        ttk.Label(edit_input_frame, text="编号:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.edit_id_display = ttk.Label(edit_input_frame, text="", foreground="gray")
        self.edit_id_display.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 患者
        ttk.Label(edit_input_frame, text="患者:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.edit_patient_entry = ttk.Entry(edit_input_frame, width=50)
        self.edit_patient_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # 症状
        ttk.Label(edit_input_frame, text="症状:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.edit_symptoms_text = scrolledtext.ScrolledText(edit_input_frame, width=50, height=4)
        self.edit_symptoms_text.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # 诊断
        ttk.Label(edit_input_frame, text="诊断:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.edit_diagnosis_entry = ttk.Entry(edit_input_frame, width=50)
        self.edit_diagnosis_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # 处方
        ttk.Label(edit_input_frame, text="处方:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.edit_prescription_text = scrolledtext.ScrolledText(edit_input_frame, width=50, height=4)
        self.edit_prescription_text.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # 配置网格权重
        edit_input_frame.columnconfigure(1, weight=1)
        edit_input_frame.rowconfigure(2, weight=1)
        edit_input_frame.rowconfigure(4, weight=1)
        
        # 操作按钮
        button_frame = ttk.Frame(self.edit_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="保存修改", command=self.save_edited_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空表单", command=self.clear_edit_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.update_display).pack(side=tk.LEFT, padx=5)
    
    def setup_delete_tab(self):
        """设置删除医案选项卡"""
        # 选择要删除的医案
        select_frame = ttk.LabelFrame(self.delete_frame, text="选择医案", padding=10)
        select_frame.pack(fill=tk.X, padx=10, pady=5)
        
        select_input_frame = ttk.Frame(select_frame)
        select_input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(select_input_frame, text="医案编号:").pack(side=tk.LEFT)
        self.delete_id_entry = ttk.Entry(select_input_frame, width=20)
        self.delete_id_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(select_input_frame, text="加载医案", command=self.load_record_for_delete).pack(side=tk.LEFT, padx=5)
        ttk.Button(select_input_frame, text="从列表选择", command=self.show_delete_selector).pack(side=tk.LEFT, padx=5)
        
        # 医案信息显示
        info_frame = ttk.LabelFrame(self.delete_frame, text="医案信息", padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.delete_info_text = scrolledtext.ScrolledText(info_frame, width=80, height=15)
        self.delete_info_text.pack(fill=tk.BOTH, expand=True)
        
        # 操作按钮
        button_frame = ttk.Frame(self.delete_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="删除医案", command=self.delete_record, style="Danger.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空", command=self.clear_delete_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.update_display).pack(side=tk.LEFT, padx=5)
        
        # 设置危险按钮样式
        style = ttk.Style()
        style.configure("Danger.TButton", foreground="red")
    
    def perform_search(self):
        """执行查询操作"""
        search_content = self.search_entry.get().strip()
        if not search_content:
            messagebox.showwarning("警告", "请输入查询内容")
            return
        
        search_method = self.search_var.get()
        
        if search_method == "id":
            result = self.medical_system.search_by_id(search_content)
            if result:
                self.display_result(result)
            else:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "未找到对应编号的医案")
        else:  # symptoms
            results = self.medical_system.search_by_symptoms(search_content)
            if results:
                self.display_multiple_results(results)
            else:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "未找到包含该症状的医案")
    
    def display_result(self, record):
        """显示单个查询结果"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, str(record))
    
    def display_multiple_results(self, records):
        """显示多个查询结果"""
        self.result_text.delete(1.0, tk.END)
        for i, record in enumerate(records, 1):
            self.result_text.insert(tk.END, f"结果 {i}:\n")
            self.result_text.insert(tk.END, str(record))
            self.result_text.insert(tk.END, "\n" + "="*50 + "\n")
    
    def add_to_study_from_search(self):
        """从查询结果添加到学习计划"""
        search_content = self.search_entry.get().strip()
        if not search_content:
            messagebox.showwarning("警告", "请先进行查询")
            return
        
        if self.search_var.get() == "id":
            if self.medical_system.add_to_study_plan(search_content):
                messagebox.showinfo("成功", "已添加到学习计划")
                self.update_display()
            else:
                messagebox.showerror("错误", "添加失败，请检查编号是否正确")
        else:
            messagebox.showwarning("警告", "请在编号查询模式下使用此功能")
    
    def edit_current_search_result(self):
        """编辑当前查询结果"""
        search_content = self.search_entry.get().strip()
        if not search_content:
            messagebox.showwarning("警告", "请先进行查询")
            return
        
        if self.search_var.get() == "id":
            # 切换到修改选项卡并加载医案
            self.notebook.select(4)  # 切换到修改医案选项卡
            self.edit_id_entry.delete(0, tk.END)
            self.edit_id_entry.insert(0, search_content)
            self.load_record_for_edit()
        else:
            messagebox.showwarning("警告", "请在编号查询模式下使用此功能")
    
    def delete_current_search_result(self):
        """删除当前查询结果"""
        search_content = self.search_entry.get().strip()
        if not search_content:
            messagebox.showwarning("警告", "请先进行查询")
            return
        
        if self.search_var.get() == "id":
            # 切换到删除选项卡并加载医案
            self.notebook.select(5)  # 切换到删除医案选项卡
            self.delete_id_entry.delete(0, tk.END)
            self.delete_id_entry.insert(0, search_content)
            self.load_record_for_delete()
        else:
            messagebox.showwarning("警告", "请在编号查询模式下使用此功能")
    
    def study_next_case(self):
        """学习下一个医案"""
        record = self.medical_system.get_next_study_case()
        if record:
            self.study_text.delete(1.0, tk.END)
            self.study_text.insert(tk.END, str(record))
            self.update_display()
        else:
            messagebox.showinfo("提示", "学习计划为空")
    
    def remove_from_study_plan(self):
        """从学习计划中移除选中医案"""
        selection = self.study_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请选择要移除的医案")
            return
        
        record_text = self.study_listbox.get(selection[0])
        record_id = record_text.split(" - ")[0]
        
        if messagebox.askyesno("确认", f"确定要从学习计划中移除医案 {record_id} 吗？"):
            if self.medical_system.remove_from_study_plan(record_id):
                messagebox.showinfo("成功", "已从学习计划中移除")
                self.update_display()
            else:
                messagebox.showerror("错误", "移除失败")
    
    def view_selected_history(self):
        """查看选中的浏览历史"""
        selection = self.history_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请选择要查看的医案")
            return
        
        # 浏览历史是倒序存储的，需要调整索引
        index = len(self.medical_system.get_browse_history()) - selection[0] - 1
        history_items = self.medical_system.get_browse_history()
        
        if 0 <= index < len(history_items):
            record = history_items[index]
            messagebox.showinfo("医案详情", str(record))
    
    def add_selected_history_to_study(self):
        """将选中的浏览历史添加到学习计划"""
        selection = self.history_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请选择要添加到学习计划的医案")
            return
        
        # 浏览历史是倒序存储的，需要调整索引
        index = len(self.medical_system.get_browse_history()) - selection[0] - 1
        history_items = self.medical_system.get_browse_history()
        
        if 0 <= index < len(history_items):
            record = history_items[index]
            if self.medical_system.add_to_study_plan(record.record_id):
                messagebox.showinfo("成功", "已添加到学习计划")
                self.update_display()
            else:
                messagebox.showerror("错误", "添加失败")
    
    def edit_selected_history(self):
        """编辑选中的浏览历史"""
        selection = self.history_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请选择要修改的医案")
            return
        
        # 浏览历史是倒序存储的，需要调整索引
        index = len(self.medical_system.get_browse_history()) - selection[0] - 1
        history_items = self.medical_system.get_browse_history()
        
        if 0 <= index < len(history_items):
            record = history_items[index]
            # 切换到修改选项卡并加载医案
            self.notebook.select(4)  # 切换到修改医案选项卡
            self.edit_id_entry.delete(0, tk.END)
            self.edit_id_entry.insert(0, record.record_id)
            self.load_record_for_edit()
    
    def delete_selected_history(self):
        """删除选中的浏览历史"""
        selection = self.history_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请选择要删除的医案")
            return
        
        # 浏览历史是倒序存储的，需要调整索引
        index = len(self.medical_system.get_browse_history()) - selection[0] - 1
        history_items = self.medical_system.get_browse_history()
        
        if 0 <= index < len(history_items):
            record = history_items[index]
            # 切换到删除选项卡并加载医案
            self.notebook.select(5)  # 切换到删除医案选项卡
            self.delete_id_entry.delete(0, tk.END)
            self.delete_id_entry.insert(0, record.record_id)
            self.load_record_for_delete()
    
    def add_new_record(self):
        """添加新医案"""
        record_id = self.id_entry.get().strip()
        patient = self.patient_entry.get().strip()
        symptoms = self.symptoms_text.get(1.0, tk.END).strip()
        diagnosis = self.diagnosis_entry.get().strip()
        prescription = self.prescription_text.get(1.0, tk.END).strip()
        
        if not all([record_id, patient, symptoms, diagnosis, prescription]):
            messagebox.showwarning("警告", "请填写所有字段")
            return
        
        success, message = self.medical_system.add_new_record(record_id, patient, symptoms, diagnosis, prescription)
        if success:
            messagebox.showinfo("成功", message)
            self.clear_form()
            self.update_display()
        else:
            messagebox.showerror("错误", message)
    
    def clear_form(self):
        """清空添加医案表单"""
        self.id_entry.delete(0, tk.END)
        self.patient_entry.delete(0, tk.END)
        self.symptoms_text.delete(1.0, tk.END)
        self.diagnosis_entry.delete(0, tk.END)
        self.prescription_text.delete(1.0, tk.END)
    
    def load_record_for_edit(self):
        """加载医案到编辑表单"""
        record_id = self.edit_id_entry.get().strip()
        if not record_id:
            messagebox.showwarning("警告", "请输入医案编号")
            return
        
        record = self.medical_system.search_by_id(record_id)
        if record:
            self.current_edit_record_id = record_id
            self.edit_id_display.config(text=record_id)
            self.edit_patient_entry.delete(0, tk.END)
            self.edit_patient_entry.insert(0, record.patient)
            self.edit_symptoms_text.delete(1.0, tk.END)
            self.edit_symptoms_text.insert(1.0, record.symptoms)
            self.edit_diagnosis_entry.delete(0, tk.END)
            self.edit_diagnosis_entry.insert(0, record.diagnosis)
            self.edit_prescription_text.delete(1.0, tk.END)
            self.edit_prescription_text.insert(1.0, record.prescription)
            messagebox.showinfo("成功", f"已加载医案 {record_id}")
        else:
            messagebox.showerror("错误", f"未找到编号为 {record_id} 的医案")
    
    def load_record_for_delete(self):
        """加载医案到删除表单"""
        record_id = self.delete_id_entry.get().strip()
        if not record_id:
            messagebox.showwarning("警告", "请输入医案编号")
            return
        
        record = self.medical_system.search_by_id(record_id)
        if record:
            self.delete_info_text.delete(1.0, tk.END)
            self.delete_info_text.insert(tk.END, str(record))
            messagebox.showinfo("成功", f"已加载医案 {record_id}，请确认删除")
        else:
            messagebox.showerror("错误", f"未找到编号为 {record_id} 的医案")
    
    def show_record_selector(self):
        """显示医案选择对话框（用于编辑）"""
        self._show_selector("选择要编辑的医案", self.edit_id_entry, self.load_record_for_edit)
    
    def show_delete_selector(self):
        """显示医案选择对话框（用于删除）"""
        self._show_selector("选择要删除的医案", self.delete_id_entry, self.load_record_for_delete)
    
    def _show_selector(self, title, entry_widget, load_callback):
        """显示医案选择对话框"""
        records = self.medical_system.get_all_records()
        if not records:
            messagebox.showinfo("提示", "当前没有医案记录")
            return
        
        # 创建选择窗口
        selector = tk.Toplevel(self.root)
        selector.title(title)
        selector.geometry("600x400")
        
        # 创建列表
        tree = ttk.Treeview(selector, columns=("ID", "Patient", "Diagnosis"), show="headings")
        tree.heading("ID", text="编号")
        tree.heading("Patient", text="患者")
        tree.heading("Diagnosis", text="诊断")
        
        for record in records:
            tree.insert("", tk.END, values=(record.record_id, record.patient, record.diagnosis))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def on_select():
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                record_id = item['values'][0]
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, record_id)
                selector.destroy()
                load_callback()
        
        ttk.Button(selector, text="选择", command=on_select).pack(pady=10)
    
    def save_edited_record(self):
        """保存修改的医案"""
        if not self.current_edit_record_id:
            messagebox.showwarning("警告", "请先加载要修改的医案")
            return
        
        patient = self.edit_patient_entry.get().strip()
        symptoms = self.edit_symptoms_text.get(1.0, tk.END).strip()
        diagnosis = self.edit_diagnosis_entry.get().strip()
        prescription = self.edit_prescription_text.get(1.0, tk.END).strip()
        
        if not all([patient, symptoms, diagnosis, prescription]):
            messagebox.showwarning("警告", "请填写所有字段")
            return
        
        # 确认对话框
        if not messagebox.askyesno("确认", f"确定要修改医案 {self.current_edit_record_id} 吗？"):
            return
        
        success, message = self.medical_system.update_record(
            self.current_edit_record_id, patient, symptoms, diagnosis, prescription
        )
        
        if success:
            messagebox.showinfo("成功", message)
            self.clear_edit_form()
            self.update_display()
        else:
            messagebox.showerror("错误", message)
    
    def delete_record(self):
        """删除医案"""
        record_id = self.delete_id_entry.get().strip()
        if not record_id:
            messagebox.showwarning("警告", "请输入医案编号")
            return
        
        # 确认对话框
        if not messagebox.askyesno("确认删除", f"确定要删除医案 {record_id} 吗？\n此操作不可恢复！"):
            return
        
        success, message = self.medical_system.delete_record(record_id)
        
        if success:
            messagebox.showinfo("成功", message)
            self.clear_delete_form()
            self.update_display()
        else:
            messagebox.showerror("错误", message)
    
    def clear_edit_form(self):
        """清空编辑表单"""
        self.current_edit_record_id = None
        self.edit_id_entry.delete(0, tk.END)
        self.edit_id_display.config(text="")
        self.edit_patient_entry.delete(0, tk.END)
        self.edit_symptoms_text.delete(1.0, tk.END)
        self.edit_diagnosis_entry.delete(0, tk.END)
        self.edit_prescription_text.delete(1.0, tk.END)
    
    def clear_delete_form(self):
        """清空删除表单"""
        self.delete_id_entry.delete(0, tk.END)
        self.delete_info_text.delete(1.0, tk.END)
    
    def clear_results(self):
        """清空查询结果"""
        self.result_text.delete(1.0, tk.END)
    
    def update_display(self):
        """更新所有显示内容"""
        # 更新学习计划列表
        self.study_listbox.delete(0, tk.END)
        study_plan = self.medical_system.get_study_plan()
        for record in study_plan:
            self.study_listbox.insert(tk.END, f"{record.record_id} - {record.patient} - {record.diagnosis}")
        
        # 更新浏览历史列表
        self.history_listbox.delete(0, tk.END)
        browse_history = self.medical_system.get_browse_history()
        for record in browse_history:
            self.history_listbox.insert(tk.END, f"{record.record_id} - {record.patient} - {record.diagnosis}")
    
    def on_closing(self):
        """程序关闭时的处理"""
        self.medical_system.close()
        self.root.destroy()
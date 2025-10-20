安装依赖：
pip install -r requirements.txt

数据初始化：
python init_database.py

重置数据库：
python reset_database.py

运行：
python main.py


删除数据库：
-- 查看所有数据库
SHOW DATABASES;

-- 删除medical_case_system数据库
DROP DATABASE IF EXISTS medical_case_system;

-- 确认删除成功
SHOW DATABASES;

查看数据库中的表数据：
use medical_case_system;
show tables;
desc medical_records;
SELECT * FROM medical_records;
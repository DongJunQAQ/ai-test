from pydantic import BaseModel, Field


class User(BaseModel):
    name: str
    age: int = Field(..., gt=0, lt=120)  # 年龄必须大于0且小于120
    email: str | None = None  # 可选字段


# 验证合法数据
user = User(name="Alice", age=30, email="alice@example.com")
print(user)
print(user.name)
print(user.model_dump_json())  # 转换为JSON字符串

# 验证非法数据（会抛出ValidationError）
try:
    User(name="Bob", age=150)
except Exception as e:
    print(e)

import os

from langchain_core.documents import Document  # 用于创建文档对象
from langchain_openai import OpenAIEmbeddings  # 用于处理文本嵌入，设置嵌入模型
from langchain_postgres import PGVector  # 用于与PostgreSQL向量数据库交互

os.environ.get("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = "https://api.siliconflow.cn/v1"  # 设置环境遍历
connection = "postgresql+psycopg://postgres:123456@192.168.246.188:5432/rag"  # 这里指定使用psycopg作为连接数据库的驱动，因此需要安装psycopg[binary]依赖
vector_store = PGVector(  # 创建PGVector向量存储实例
    embeddings=OpenAIEmbeddings(model="BAAI/bge-m3"),  # 指定使用的嵌入模型
    collection_name="my_rag_docs",  # 文档集合名称，不是数据表的名称
    connection=connection,  # 数据库连接
    use_jsonb=True,  # 启用JSONB格式存储元数据
)
docs = [  # 测试数据文档
    Document(  # 创建Document对象
        page_content="池塘里有猫",
        metadata={"id": 1, "location": "pond", "topic": "animals"},
    ),
    Document(
        page_content="池塘里也有鸭子",
        metadata={"id": 2, "location": "pond", "topic": "animals"},
    ),
    Document(
        page_content="市场上有新鲜的苹果",
        metadata={"id": 3, "location": "market", "topic": "food"},
    ),
    Document(
        page_content="市场也卖新鲜的橙子",
        metadata={"id": 4, "location": "market", "topic": "food"},
    ),
    Document(
        page_content="新的艺术展览很迷人",
        metadata={"id": 5, "location": "museum", "topic": "art"},
    ),
    Document(
        page_content="博物馆也有一个雕塑展览",
        metadata={"id": 6, "location": "museum", "topic": "art"},
    ),
    Document(
        page_content="主街上开了一家新的咖啡店",
        metadata={"id": 7, "location": "Main Street", "topic": "food"},
    ),
    Document(
        page_content="读书俱乐部在图书馆碰面",
        metadata={"id": 8, "location": "library", "topic": "reading"},
    ),
    Document(
        page_content="图书馆每周为孩子们举办一次故事时间活动",
        metadata={"id": 9, "location": "library", "topic": "reading"},
    ),
    Document(
        page_content="社区中心为初学者提供烹饪课",
        metadata={"id": 10, "location": "community center", "topic": "classes"},
    ),
]
# 将测试数据存入数据库
ids = []  # 用来存储文档ID
for doc in docs:  # 遍历测试文档列表，提取每个文档的id并添加到列表中
    ids.append(doc.metadata["id"])
vector_store.add_documents(docs, ids=ids)  # 将测试文档和对应的id添加到向量存储数据库中
# 相似度匹配搜索
query = "咖啡店在哪里"
# query = "猫在哪里"
results = vector_store.similarity_search_with_score(query=query, k=5)  # 执行相似性搜索并返回前5个最相似的结果及其相似度分数
for doc, score in results:  # 遍历搜索结果，打印每个结果的相似度分数、文档内容和元数据
    print(f"* [SIM={score:3f}] {doc.page_content} [{doc.metadata}]")

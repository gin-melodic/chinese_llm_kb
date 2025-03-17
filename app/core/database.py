import psycopg2
from psycopg2.extras import RealDictCursor
from app.core.config import settings

def get_db_connection():
    """创建PostgreSQL数据库连接"""
    conn = psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        dbname=settings.DB_NAME,
        cursor_factory=RealDictCursor
    )
    return conn

def init_vector_extension():
    """初始化pgvector扩展"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
            if cursor.rowcount == 0:
                cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
                conn.commit()
                print("pgvector扩展创建成功")
            else:
                print("pgvector扩展已存在")
    except Exception as e:
        print(f"初始化向量扩展时出错: {e}")
    finally:
        conn.close()

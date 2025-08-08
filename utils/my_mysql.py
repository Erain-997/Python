import pymysql
from utils.logger_manager import LoggerManager

logger = LoggerManager().get_logger(name=__name__)

# 数据库配置 todo 后续分离结构
DB_CONFIG = {
    "host": "",  # 主机地址
    "port": 6446,  # 默认端口
    "user": "",  # 用户名
    "password": "^",  # 密码
    "database": "",  # 数据库名
    "charset": ""
}


def get_db_connection():
    """建立数据库连接"""
    return pymysql.connect(**DB_CONFIG)


def check_unlock_counts(threshold=20):
    """
    查询所有 user_id 的解锁次数（跨两个表）, 并输出超过阈值的 user_id
    """
    query = """
            SELECT user_id, COUNT(*) AS total_count
            FROM (SELECT user_id
                  FROM bs_drama_unlock_t0
                  UNION ALL
                  SELECT user_id
                  FROM bs_drama_unlock_t1) AS combined
            GROUP BY user_id; \
            """

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            exceeded = [row for row in results if row[1] > threshold]

            if exceeded:
                logger.info(f"以下 user_id 的记录数超过 {threshold}：")
                for user_id, count in exceeded:
                    logger.error(f"测试失败: user_id: {user_id}, count: {count}")
                return True
            else:
                logger.info(f"没有 user_id 的记录数超过 {threshold}")
                return False
    finally:
        connection.close()


def check_user_unlock_counts(user_id: str, threshold: int = 20) -> bool:
    """
    查询指定 user_id 在两个表中的总解锁次数。
    若未超过阈值,  则返回 True, 并打印“测试通过”；
    否则打印失败信息并返回 False。
    """
    query = f"""
        SELECT COUNT(*) AS total_count
        FROM (
            SELECT user_id FROM bs_drama_unlock_t0 WHERE user_id = %s
            UNION ALL
            SELECT user_id FROM bs_drama_unlock_t1 WHERE user_id = %s
        ) AS combined;
    """

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (user_id, user_id))
            total_count = cursor.fetchone()[0]

            if total_count > threshold:
                logger.error(f"❌ user_id: {user_id} 的记录数为 {total_count}, 超过阈值 {threshold}, 测试失败")
                return False
            else:
                logger.info(f"✅ user_id: {user_id} 的记录数为 {total_count}, 未超过阈值 {threshold}, 测试通过")
                return True
    finally:
        connection.close()


def update_user_coins_and_bonus(user_id, coins=999, bonus=999):
    """
    将指定 user_id 的 coins 和 bonus 字段更新为指定值。
    优先更新 bs_user_t0，若无数据则尝试更新 bs_user_t1。

    参数:
        user_id (int): 用户 ID。
        coins (int): 要设置的 coins 值，默认 999。
        bonus (int): 要设置的 bonus 值，默认 999。
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 更新 bs_user_t0
            update_query_t0 = """
                              UPDATE bs_user_t0
                              SET coins = %s,
                                  bonus = %s
                              WHERE user_id = %s \
                              """
            cursor.execute(update_query_t0, (coins, bonus, user_id))

            if cursor.rowcount == 0:
                # 更新 bs_user_t1
                update_query_t1 = """
                                  UPDATE bs_user_t1
                                  SET coins = %s,
                                      bonus = %s
                                  WHERE user_id = %s \
                                  """
                cursor.execute(update_query_t1, (coins, bonus, user_id))
                if cursor.rowcount == 0:
                    print(f"⚠️  user_id={user_id} 不存在于 bs_user_t0 或 bs_user_t1")
                    return False
                else:
                    print(f"✅ 已更新 bs_user_t1 中 user_id={user_id} 的 coins 和 bonus 为 {coins}")
            else:
                print(f"✅ 已更新 bs_user_t0 中 user_id={user_id} 的 coins 和 bonus 为 {coins}")

            connection.commit()
            return True

    except Exception as e:
        print(f"❌ 更新 user_id={user_id} 时出错: {e}")
        connection.rollback()
        return False
    finally:
        connection.close()


def check_db_connection_leak(threshold=3, db_name="ffff_stress"):
    """
    检查 MySQL 当前连接是否存在连接泄露的风险。
    - 超过阈值的连接数量
    - 单连接持续时间超过一定时长
    - 处于 Query 状态但未结束的连接
    """
    query = f"""
        SELECT ID, USER, HOST, DB, COMMAND, TIME, STATE, INFO
        FROM information_schema.PROCESSLIST
        WHERE DB = %s AND COMMAND = 'Query' AND TIME > %s
        ORDER BY TIME DESC;
    """

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (db_name, threshold))
            results = cursor.fetchall()

            if results:
                logger.warning(f"以下连接在数据库 [{db_name}] 中可能存在连接泄露，持续时间超过 {threshold} 秒：")
                for row in results:
                    conn_id, user, host, db, command, time_spent, state, info = row
                    logger.error(
                        f"[ID={conn_id}] USER={user}, HOST={host}, TIME={time_spent}s, "
                        f"STATE={state}, SQL={info[:100] if info else 'None'}"
                    )
                return True
            else:
                logger.info(f"未检测到数据库 [{db_name}] 中超过 {threshold} 秒的长连接。")
                return False
    finally:
        connection.close()


# 示例调用
if __name__ == "__main__":
    # check_user_unlock_counts()
    update_user_coins_and_bonus(109087134)

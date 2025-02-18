import sys


class LogHandler:
    def __init__(self):
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.logs = []

    def emit_log_message(self, message):
        # 这里你可以实现将消息发送到前端的逻辑
        self.logs.append(message)
        self.original_stdout.write(f"Log: {message}\n")

    def redirect_logs(self):
        self.logs.clear()

        class LogRedirector:
            def __init__(self, emit_func, original_stdout, original_stderr):
                self.emit_func = emit_func
                self.original_stdout = original_stdout
                self.original_stderr = original_stderr

            def write(self, message):
                if message.strip():
                    self.emit_func(message)
                self.original_stdout.write(message)
                self.original_stdout.flush()

            def flush(self):
                self.original_stdout.flush()
                self.original_stderr.flush()

        self.log_redirector = LogRedirector(
            self.emit_log_message, self.original_stdout, self.original_stderr
        )
        sys.stdout = self.log_redirector
        sys.stderr = self.log_redirector

    def restore_logs(self):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

    def get_logs(self):
        return self.logs


# 使用示例
if __name__ == "__main__":
    log_handler = LogHandler()
    log_handler.redirect_logs()

    # 现在所有的 print 语句都会通过 emit_log_message 函数发送到前端
    print("This will be sent to the front-end log.")

    # 获取日志内容
    logs = log_handler.get_logs()

    # 恢复原始日志
    log_handler.restore_logs()
    print("Collected logs:", logs)

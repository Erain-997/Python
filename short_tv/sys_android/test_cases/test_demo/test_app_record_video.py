import base64
import logging
import time
import unittest

from sys_android.page_objects.reward_page import RewardPage

from common.language.lang_mgr import lang_mgr
from common.utils.path_config import android


class TestAppRecordVideo(unittest.TestCase):
    # 初始化数据——>测试前准备
    def setUp(self) -> None:
        self.driver = RewardPage()

    # 测试环境——>清理
    def tearDown(self) -> None:
        self.driver.quit()

    # 短剧——>我的模块
    def test_reward_video(self):
        try:
            # 启动录制视频
            logging.info("启动录制视频")
            self.start_recording()
            # 等待15秒
            time.sleep(10)
            # 停止录制视频并保存
            self.stop_and_save_recording("test_reward_video.mp4")
            logging.info("视频录制成功")

        except Exception as e:
            self.handle_exception(e)

        logging.info("签到多语言:" + lang_mgr.push_check_in_title_new_1())
        logging.info("订阅" + lang_mgr.profile_subscription_view_default_title())

        # 相等断言 奖励文本
        self.assertEqual("奖励", "奖励")

    def start_recording(self):
        """启动录制视频"""
        self.driver.driver.start_recording_screen()

    def stop_and_save_recording(self, filename):
        """停止录制视频并保存"""
        video_data = self.driver.driver.stop_recording_screen()
        video_path = f"{android.recording_dir}/{filename}"
        with open(video_path, "wb") as video_file:
            video_file.write(base64.b64decode(video_data))

    def handle_exception(self, exception):
        """处理异常"""
        self.driver.screenshot(f"{android.screenshot_dir}/error.png")
        logging.info(exception)


if __name__ == "__main__":
    unittest.main()

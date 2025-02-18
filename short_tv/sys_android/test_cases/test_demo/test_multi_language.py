import pytest

from common.language.lang_mgr import lang_mgr

1


def test_initial_language():
    """
    测试初始语言
    """
    assert lang_mgr.common_unknown_exception() == "Unknown error"


def test_switch_language_to_zh_hans():
    """
    测试切换语言到简体中文
    """
    lang_mgr.switch_language({"language": "zh-CN"})
    assert lang_mgr.common_unknown_exception() == "未知异常"


if __name__ == "__main__":
    pytest.main()

import xml.etree.ElementTree as ET
from collections import OrderedDict

from common.utils.arg_parse_func import args
from common.utils.path_config import android

app_language_codes = {
    "zh_cn": {"locale": "CN", "path": "values-zh-rCN"},
    "en": {"locale": "US", "path": "values"},
    "zh": {"locale": "TW", "path": "values-zh-rTW"},
    "fil": {"locale": "PH", "path": "values-fil"},
    "ja": {"locale": "JP", "path": "values-ja"},
    "ko": {"locale": "KR", "path": "values-ko"},
    "in": {"locale": "ID", "path": "values-in"},
    "hi": {"locale": "IN", "path": "values-hi"},
    "th": {"locale": "TH", "path": "values-th"},
    "ar": {"locale": "SA", "path": "values-ar"},
    "pt": {"locale": "PT", "path": "values-pt"},
    "es": {"locale": "ES", "path": "values-es"},
    "vi": {"locale": "VN", "path": "values-vi"},
    "de": {"locale": "DE", "path": "values-de"},
    "fr": {"locale": "FR", "path": "values-fr"},
    "ms": {"locale": "MY", "path": "values-ms"},
    "ru": {"locale": "RU", "path": "values-ru"},
    "it": {"locale": "IT", "path": "values-it"},
}


# 单例类 LangMgr
class LangMgr:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LangMgr, cls).__new__(cls)
            cls._instance.app_language_code = args.language  # 默认语言
            cls._instance.app_language_path = app_language_codes[cls._instance.app_language_code]["path"]
        return cls._instance

    def switch_language(self, capabilities):
        """切换应用语言"""
        new_app_language_code = capabilities["language"]
        if new_app_language_code in app_language_codes:
            self.app_language_code = new_app_language_code
        else:
            raise ValueError(f"Unsupported language key: {new_app_language_code}")

        # 使用 OrderedDict 来维护键的顺序
        ordered_capabilities = OrderedDict(capabilities)

        # 移除现有的 locale 键（如果存在）
        if "locale" in ordered_capabilities:
            del ordered_capabilities["locale"]

        # 添加 locale 键到最后
        ordered_capabilities["locale"] = app_language_codes[self.app_language_code]["locale"]
        self.app_language_path = app_language_codes[self.app_language_code]["path"]

    def get_lang_text(self, key: str):
        """获取指定key的语言文本"""
        xml_path = android.language_dir + "/res/" + self.app_language_path + "/strings.xml"

        # 读取XML文件, 返回对应key的value值
        xml_tree = ET.parse(xml_path)
        root = xml_tree.getroot()

        return root.find(f"string[@name='{key}']").text

    def app_name(self):
        return self.get_lang_text("app_name")

    def common_network_error(self):
        return self.get_lang_text("common_network_error")

    def common_unknown_exception(self):
        return self.get_lang_text("common_unknown_exception")

    def common_login_expired(self):
        return self.get_lang_text("common_login_expired")

    def common_re_login(self):
        return self.get_lang_text("common_re_login")

    def common_error_code(self):
        return self.get_lang_text("common_error_code")

    def common_waiting(self):
        return self.get_lang_text("common_waiting")

    def common_retry(self):
        return self.get_lang_text("common_retry")

    def common_no_more_data(self):
        return self.get_lang_text("common_no_more_data")

    def common_data_empty(self):
        return self.get_lang_text("common_data_empty")

    def common_not_find_app_to_send_email(self):
        return self.get_lang_text("common_not_find_app_to_send_email")

    def common_google_pay_not_support(self):
        return self.get_lang_text("common_google_pay_not_support")

    def common_user_canceled(self):
        return self.get_lang_text("common_user_canceled")

    def common_coins(self):
        return self.get_lang_text("common_coins")

    def common_bonus(self):
        return self.get_lang_text("common_bonus")

    def common_current_ep(self):
        return self.get_lang_text("common_current_ep")

    def common_total_ep(self):
        return self.get_lang_text("common_total_ep")

    def common_delete(self):
        return self.get_lang_text("common_delete")

    def common_cancel(self):
        return self.get_lang_text("common_cancel")

    def common_confirm(self):
        return self.get_lang_text("common_confirm")

    def common_submit(self):
        return self.get_lang_text("common_submit")

    def common_play_failed(self):
        return self.get_lang_text("common_play_failed")

    def common_server_error(self):
        return self.get_lang_text("common_server_error")

    def common_copy_success(self):
        return self.get_lang_text("common_copy_success")

    def common_duplicate_op_tip(self):
        return self.get_lang_text("common_duplicate_op_tip")

    def common_later(self):
        return self.get_lang_text("common_later")

    def common_yes(self):
        return self.get_lang_text("common_yes")

    def common_no(self):
        return self.get_lang_text("common_no")

    def common_ok(self):
        return self.get_lang_text("common_ok")

    def main_activity_tab_discover(self):
        return self.get_lang_text("main_activity_tab_discover")

    def main_activity_tab_shorts(self):
        return self.get_lang_text("main_activity_tab_shorts")

    def main_activity_tab_my_list(self):
        return self.get_lang_text("main_activity_tab_my_list")

    def main_activity_tab_profile(self):
        return self.get_lang_text("main_activity_tab_profile")

    def main_activity_tab_reward(self):
        return self.get_lang_text("main_activity_tab_reward")

    def main_activity_tab_guide_tip_1(self):
        return self.get_lang_text("main_activity_tab_guide_tip_1")

    def main_activity_tab_guide_tip_2(self):
        return self.get_lang_text("main_activity_tab_guide_tip_2")

    def discover_fragment_play_now(self):
        return self.get_lang_text("discover_fragment_play_now")

    def discover_fragment_remind_me(self):
        return self.get_lang_text("discover_fragment_remind_me")

    def discover_fragment_reserved(self):
        return self.get_lang_text("discover_fragment_reserved")

    def discover_fragment_coming_soon(self):
        return self.get_lang_text("discover_fragment_coming_soon")

    def discover_fragment_reserve_succeed(self):
        return self.get_lang_text("discover_fragment_reserve_succeed")

    def discover_fragment_coming_soon_more(self):
        return self.get_lang_text("discover_fragment_coming_soon_more")

    def discover_fragment_low_sku_template_notification_go(self):
        return self.get_lang_text("discover_fragment_low_sku_template_notification_go")

    def profile_fragment_uid(self):
        return self.get_lang_text("profile_fragment_uid")

    def profile_fragment_my_wallet(self):
        return self.get_lang_text("profile_fragment_my_wallet")

    def profile_fragment_coins(self):
        return self.get_lang_text("profile_fragment_coins")

    def profile_fragment_bonus(self):
        return self.get_lang_text("profile_fragment_bonus")

    def profile_fragment_top_up(self):
        return self.get_lang_text("profile_fragment_top_up")

    def profile_fragment_rewards(self):
        return self.get_lang_text("profile_fragment_rewards")

    def profile_fragment_feedback(self):
        return self.get_lang_text("profile_fragment_feedback")

    def profile_fragment_language(self):
        return self.get_lang_text("profile_fragment_language")

    def profile_fragment_settings(self):
        return self.get_lang_text("profile_fragment_settings")

    def profile_fragment_guest(self):
        return self.get_lang_text("profile_fragment_guest")

    def profile_fragment_user(self):
        return self.get_lang_text("profile_fragment_user")

    def profile_fragment_feedback_content(self):
        return self.get_lang_text("profile_fragment_feedback_content")

    def profile_fragment_login_tip(self):
        return self.get_lang_text("profile_fragment_login_tip")

    def profile_fragment_reward_tip(self):
        return self.get_lang_text("profile_fragment_reward_tip")

    def profile_fragment_official_social_media(self):
        return self.get_lang_text("profile_fragment_official_social_media")

    def settings_fragment_privacy_policy(self):
        return self.get_lang_text("settings_fragment_privacy_policy")

    def settings_fragment_user_agreement(self):
        return self.get_lang_text("settings_fragment_user_agreement")

    def settings_fragment_delete_account(self):
        return self.get_lang_text("settings_fragment_delete_account")

    def settings_fragment_logout(self):
        return self.get_lang_text("settings_fragment_logout")

    def settings_fragment_version(self):
        return self.get_lang_text("settings_fragment_version")

    def settings_fragment_personal(self):
        return self.get_lang_text("settings_fragment_personal")

    def settings_fragment_account_info(self):
        return self.get_lang_text("settings_fragment_account_info")

    def settings_fragment_else(self):
        return self.get_lang_text("settings_fragment_else")

    def settings_fragment_permissions(self):
        return self.get_lang_text("settings_fragment_permissions")

    def settings_fragment_automatic_episode_unlock(self):
        return self.get_lang_text("settings_fragment_automatic_episode_unlock")

    def app_language_fragment_title(self):
        return self.get_lang_text("app_language_fragment_title")

    def login_activity_login_with(self):
        return self.get_lang_text("login_activity_login_with")

    def login_activity_desc(self):
        return self.get_lang_text("login_activity_desc")

    def login_activity_policy(self):
        return self.get_lang_text("login_activity_policy")

    def delete_account_fragment_title(self):
        return self.get_lang_text("delete_account_fragment_title")

    def delete_account_fragment_desc(self):
        return self.get_lang_text("delete_account_fragment_desc")

    def top_up_fragment_recharge_tip(self):
        return self.get_lang_text("top_up_fragment_recharge_tip")

    def top_up_fragment_recharge_agreement(self):
        return self.get_lang_text("top_up_fragment_recharge_agreement")

    def top_up_fragment_recharge_success(self):
        return self.get_lang_text("top_up_fragment_recharge_success")

    def top_up_fragment_restore(self):
        return self.get_lang_text("top_up_fragment_restore")

    def top_up_fragment_not_find_lost_order_tip(self):
        return self.get_lang_text("top_up_fragment_not_find_lost_order_tip")

    def top_up_fragment_lost_coins_restore_success_tip(self):
        return self.get_lang_text("top_up_fragment_lost_coins_restore_success_tip")

    def top_up_fragment_lost_subs_restore_success_tip(self):
        return self.get_lang_text("top_up_fragment_lost_subs_restore_success_tip")

    def top_up_fragment_lost_coins_subs_restore_success_tip(self):
        return self.get_lang_text("top_up_fragment_lost_coins_subs_restore_success_tip")

    def top_up_fragment_lost_discount_restore_success_tip(self):
        return self.get_lang_text("top_up_fragment_lost_discount_restore_success_tip")

    def top_up_fragment_desc_title(self):
        return self.get_lang_text("top_up_fragment_desc_title")

    def top_up_fragment_desc_content(self):
        return self.get_lang_text("top_up_fragment_desc_content")

    def unlock_episode_dialog_fragment_price(self):
        return self.get_lang_text("unlock_episode_dialog_fragment_price")

    def unlock_episode_dialog_fragment_balance(self):
        return self.get_lang_text("unlock_episode_dialog_fragment_balance")

    def unlock_episode_dialog_fragment_coin_store(self):
        return self.get_lang_text("unlock_episode_dialog_fragment_coin_store")

    def unlock_episode_dialog_fragment_watch_ads(self):
        return self.get_lang_text("unlock_episode_dialog_fragment_watch_ads")

    def unlock_episode_dialog_fragment_watch_ads_desc(self):
        return self.get_lang_text("unlock_episode_dialog_fragment_watch_ads_desc")

    def unlock_episode_dialog_fragment_unlock(self):
        return self.get_lang_text("unlock_episode_dialog_fragment_unlock")

    def unlock_episode_dialog_fragment_low_sku_template_notification(self):
        return self.get_lang_text("unlock_episode_dialog_fragment_low_sku_template_notification")

    def batch_unlock_episode_dialog_fragment_title(self):
        return self.get_lang_text("batch_unlock_episode_dialog_fragment_title")

    def batch_unlock_episode_dialog_fragment_coin_sku_title(self):
        return self.get_lang_text("batch_unlock_episode_dialog_fragment_coin_sku_title")

    def batch_unlock_episode_dialog_fragment_unlock_all_episodes(self):
        return self.get_lang_text("batch_unlock_episode_dialog_fragment_unlock_all_episodes")

    def batch_unlock_episode_dialog_fragment_unlock_success(self):
        return self.get_lang_text("batch_unlock_episode_dialog_fragment_unlock_success")

    def batch_unlock_episode_dialog_fragment_unlock_ad_title(self):
        return self.get_lang_text("batch_unlock_episode_dialog_fragment_unlock_ad_title")

    def batch_unlock_episode_dialog_fragment_unlock_ad_desc(self):
        return self.get_lang_text("batch_unlock_episode_dialog_fragment_unlock_ad_desc")

    def coin_store_dialog_fragment_free_unlock(self):
        return self.get_lang_text("coin_store_dialog_fragment_free_unlock")

    def my_list_fragment_my_collection(self):
        return self.get_lang_text("my_list_fragment_my_collection")

    def my_list_fragment_recently_watched(self):
        return self.get_lang_text("my_list_fragment_recently_watched")

    def my_list_fragment_empty_desc(self):
        return self.get_lang_text("my_list_fragment_empty_desc")

    def my_list_fragment_select_all(self):
        return self.get_lang_text("my_list_fragment_select_all")

    def my_list_fragment_edit_mode_tab_disable_tip(self):
        return self.get_lang_text("my_list_fragment_edit_mode_tab_disable_tip")

    def my_list_fragment_delete_tip(self):
        return self.get_lang_text("my_list_fragment_delete_tip")

    def my_list_fragment_home(self):
        return self.get_lang_text("my_list_fragment_home")

    def shorts_fragment_list(self):
        return self.get_lang_text("shorts_fragment_list")

    def for_you_fragment_share(self):
        return self.get_lang_text("for_you_fragment_share")

    def for_you_fragment_more(self):
        return self.get_lang_text("for_you_fragment_more")

    def for_you_fragment_less(self):
        return self.get_lang_text("for_you_fragment_less")

    def episode_list_dialog_fragment_shorts_episode_status(self):
        return self.get_lang_text("episode_list_dialog_fragment_shorts_episode_status")

    def episode_list_dialog_fragment_disable_skip_locked_episode(self):
        return self.get_lang_text("episode_list_dialog_fragment_disable_skip_locked_episode")

    def notification_watch_now(self):
        return self.get_lang_text("notification_watch_now")

    def notification_free(self):
        return self.get_lang_text("notification_free")

    def notification_check_in_button(self):
        return self.get_lang_text("notification_check_in_button")

    def notification_daemon_title_1(self):
        return self.get_lang_text("notification_daemon_title_1")

    def notification_daemon_content_1(self):
        return self.get_lang_text("notification_daemon_content_1")

    def notification_daemon_title_2(self):
        return self.get_lang_text("notification_daemon_title_2")

    def notification_daemon_content_2(self):
        return self.get_lang_text("notification_daemon_content_2")

    def notification_enter_now(self):
        return self.get_lang_text("notification_enter_now")

    def notification_go_now(self):
        return self.get_lang_text("notification_go_now")

    def rewards_activity_bonus(self):
        return self.get_lang_text("rewards_activity_bonus")

    def rewards_activity_check_in_title(self):
        return self.get_lang_text("rewards_activity_check_in_title")

    def rewards_activity_check_in_desc(self):
        return self.get_lang_text("rewards_activity_check_in_desc")

    def rewards_activity_check_in(self):
        return self.get_lang_text("rewards_activity_check_in")

    def rewards_activity_check_in_day(self):
        return self.get_lang_text("rewards_activity_check_in_day")

    def rewards_activity_sign_in_resigning(self):
        return self.get_lang_text("rewards_activity_sign_in_resigning")

    def rewards_activity_sign_in_reminder(self):
        return self.get_lang_text("rewards_activity_sign_in_reminder")

    def rewards_activity_sign_in_reminder_tip(self):
        return self.get_lang_text("rewards_activity_sign_in_reminder_tip")

    def rewards_activity_watch_ad_title(self):
        return self.get_lang_text("rewards_activity_watch_ad_title")

    def rewards_activity_watch_ad_desc(self):
        return self.get_lang_text("rewards_activity_watch_ad_desc")

    def rewards_activity_watch_all_ads_desc(self):
        return self.get_lang_text("rewards_activity_watch_all_ads_desc")

    def rewards_activity_watch_ad_bonus_value(self):
        return self.get_lang_text("rewards_activity_watch_ad_bonus_value")

    def rewards_activity_watch_ad_get(self):
        return self.get_lang_text("rewards_activity_watch_ad_get")

    def rewards_activity_watch_ad_double_rewards(self):
        return self.get_lang_text("rewards_activity_watch_ad_double_rewards")

    def rewards_activity_description_title(self):
        return self.get_lang_text("rewards_activity_description_title")

    def rewards_activity_description_value(self):
        return self.get_lang_text("rewards_activity_description_value")

    def rewards_activity_go(self):
        return self.get_lang_text("rewards_activity_go")

    def rewards_activity_accept_task_reward_tip(self):
        return self.get_lang_text("rewards_activity_accept_task_reward_tip")

    def play_episode_activity_unlock_success(self):
        return self.get_lang_text("play_episode_activity_unlock_success")

    def play_episode_activity_update_speed_tip(self):
        return self.get_lang_text("play_episode_activity_update_speed_tip")

    def play_episode_activity_speed_playing(self):
        return self.get_lang_text("play_episode_activity_speed_playing")

    def play_episode_activity_speed_playing_unit(self):
        return self.get_lang_text("play_episode_activity_speed_playing_unit")

    def play_episode_activity_resolution_auto(self):
        return self.get_lang_text("play_episode_activity_resolution_auto")

    def play_episode_activity_resolution_auto_select_tip(self):
        return self.get_lang_text("play_episode_activity_resolution_auto_select_tip")

    def play_episode_activity_resolution_loading_tip(self):
        return self.get_lang_text("play_episode_activity_resolution_loading_tip")

    def play_episode_activity_downgrade_resolution_due_to_net_caton_auto(self):
        return self.get_lang_text("play_episode_activity_downgrade_resolution_due_to_net_caton_auto")

    def play_episode_activity_downgrade_resolution_due_to_net_caton(self):
        return self.get_lang_text("play_episode_activity_downgrade_resolution_due_to_net_caton")

    def play_episode_activity_downgrade_resolution_due_to_net_caton_switch(self):
        return self.get_lang_text("play_episode_activity_downgrade_resolution_due_to_net_caton_switch")

    def play_episode_activity_switch_resolution_tip(self):
        return self.get_lang_text("play_episode_activity_switch_resolution_tip")

    def play_episode_activity_switch_resolution_process_tip(self):
        return self.get_lang_text("play_episode_activity_switch_resolution_process_tip")

    def play_episode_activity_switch_resolution_auto_tip(self):
        return self.get_lang_text("play_episode_activity_switch_resolution_auto_tip")

    def play_episode_activity_switch_resolution_auto_process_tip(self):
        return self.get_lang_text("play_episode_activity_switch_resolution_auto_process_tip")

    def play_episode_activity_progress_adjust(self):
        return self.get_lang_text("play_episode_activity_progress_adjust")

    def play_episode_activity_unlock_now(self):
        return self.get_lang_text("play_episode_activity_unlock_now")

    def play_episode_activity_switch_resolution_failed(self):
        return self.get_lang_text("play_episode_activity_switch_resolution_failed")

    def play_episode_activity_swipe_to_watch(self):
        return self.get_lang_text("play_episode_activity_swipe_to_watch")

    def play_episode_collect_tips_1(self):
        return self.get_lang_text("play_episode_collect_tips_1")

    def play_episode_collect_tips_2(self):
        return self.get_lang_text("play_episode_collect_tips_2")

    def play_episode_collect_tips_3(self):
        return self.get_lang_text("play_episode_collect_tips_3")

    def play_episode_activity_discount_unlock_tips(self):
        return self.get_lang_text("play_episode_activity_discount_unlock_tips")

    def immersion_activity_purchase_all_episode(self):
        return self.get_lang_text("immersion_activity_purchase_all_episode")

    def episode_play_speed_fragment_title(self):
        return self.get_lang_text("episode_play_speed_fragment_title")

    def episode_play_resolution_fragment_title(self):
        return self.get_lang_text("episode_play_resolution_fragment_title")

    def check_in_result_dialog_fragment_title(self):
        return self.get_lang_text("check_in_result_dialog_fragment_title")

    def check_in_result_dialog_fragment_watch_ad_desc(self):
        return self.get_lang_text("check_in_result_dialog_fragment_watch_ad_desc")

    def check_in_result_dialog_fragment_watch_now(self):
        return self.get_lang_text("check_in_result_dialog_fragment_watch_now")

    def login_dialog_fragment_fb_first_login_bonus_tip(self):
        return self.get_lang_text("login_dialog_fragment_fb_first_login_bonus_tip")

    def login_dialog_fragment_google_first_login_bonus_tip(self):
        return self.get_lang_text("login_dialog_fragment_google_first_login_bonus_tip")

    def facebook_login_dialog_fragment_huge(self):
        return self.get_lang_text("facebook_login_dialog_fragment_huge")

    def phone_auth_fragment_hint_phone_number(self):
        return self.get_lang_text("phone_auth_fragment_hint_phone_number")

    def phone_auth_fragment_hint_verification_code(self):
        return self.get_lang_text("phone_auth_fragment_hint_verification_code")

    def phone_auth_fragment_get(self):
        return self.get_lang_text("phone_auth_fragment_get")

    def phone_auth_fragment_resend(self):
        return self.get_lang_text("phone_auth_fragment_resend")

    def phone_auth_fragment_welcome(self):
        return self.get_lang_text("phone_auth_fragment_welcome")

    def phone_auth_fragment_confirm(self):
        return self.get_lang_text("phone_auth_fragment_confirm")

    def phone_auth_fragment_check_content(self):
        return self.get_lang_text("phone_auth_fragment_check_content")

    def phone_auth_fragment_succeed(self):
        return self.get_lang_text("phone_auth_fragment_succeed")

    def phone_auth_fragment_invalid_area_code(self):
        return self.get_lang_text("phone_auth_fragment_invalid_area_code")

    def phone_auth_fragment_network_error(self):
        return self.get_lang_text("phone_auth_fragment_network_error")

    def email_auth_fragment_welcome(self):
        return self.get_lang_text("email_auth_fragment_welcome")

    def email_auth_fragment_hint_email_address(self):
        return self.get_lang_text("email_auth_fragment_hint_email_address")

    def email_auth_fragment_check_content(self):
        return self.get_lang_text("email_auth_fragment_check_content")

    def email_auth_fragment_succeed(self):
        return self.get_lang_text("email_auth_fragment_succeed")

    def immersion_back_fragment_title(self):
        return self.get_lang_text("immersion_back_fragment_title")

    def immersion_back_fragment_button_play(self):
        return self.get_lang_text("immersion_back_fragment_button_play")

    def region_select_fragment_title(self):
        return self.get_lang_text("region_select_fragment_title")

    def bind_info_fragment_email(self):
        return self.get_lang_text("bind_info_fragment_email")

    def bind_info_fragment_phone(self):
        return self.get_lang_text("bind_info_fragment_phone")

    def bind_info_fragment_unbound(self):
        return self.get_lang_text("bind_info_fragment_unbound")

    def bind_info_fragment_bind(self):
        return self.get_lang_text("bind_info_fragment_bind")

    def ad_loading(self):
        return self.get_lang_text("ad_loading")

    def ad_interstitial_remove_ad_by_payment(self):
        return self.get_lang_text("ad_interstitial_remove_ad_by_payment")

    def notification_permission_dialog_title(self):
        return self.get_lang_text("notification_permission_dialog_title")

    def notification_permission_dialog_des(self):
        return self.get_lang_text("notification_permission_dialog_des")

    def notification_permission_dialog_receive(self):
        return self.get_lang_text("notification_permission_dialog_receive")

    def notification_permission_dialog_choose_title(self):
        return self.get_lang_text("notification_permission_dialog_choose_title")

    def notification_permission_dialog_choose_turn_on(self):
        return self.get_lang_text("notification_permission_dialog_choose_turn_on")

    def notification_permission_dialog_granted(self):
        return self.get_lang_text("notification_permission_dialog_granted")

    def notification_permission_dialog_choose_item_0(self):
        return self.get_lang_text("notification_permission_dialog_choose_item_0")

    def notification_permission_dialog_choose_item_1(self):
        return self.get_lang_text("notification_permission_dialog_choose_item_1")

    def notification_permission_dialog_choose_item_2(self):
        return self.get_lang_text("notification_permission_dialog_choose_item_2")

    def notification_permission_dialog_choose_item_3(self):
        return self.get_lang_text("notification_permission_dialog_choose_item_3")

    def sku_expansion_dialog_fragment_title(self):
        return self.get_lang_text("sku_expansion_dialog_fragment_title")

    def sku_expansion_dialog_fragment_count_down(self):
        return self.get_lang_text("sku_expansion_dialog_fragment_count_down")

    def normal_login_guide_dialog_fragment_desc(self):
        return self.get_lang_text("normal_login_guide_dialog_fragment_desc")

    def normal_login_guide_dialog_fragment_protect_your_property(self):
        return self.get_lang_text("normal_login_guide_dialog_fragment_protect_your_property")

    def normal_login_guide_dialog_fragment_log_in(self):
        return self.get_lang_text("normal_login_guide_dialog_fragment_log_in")

    def rating_dialog_title(self):
        return self.get_lang_text("rating_dialog_title")

    def rating_dialog_desc(self):
        return self.get_lang_text("rating_dialog_desc")

    def rating_dialog_desc_key_word(self):
        return self.get_lang_text("rating_dialog_desc_key_word")

    def rating_dialog_rating_success_tip(self):
        return self.get_lang_text("rating_dialog_rating_success_tip")

    def update_dialog_title(self):
        return self.get_lang_text("update_dialog_title")

    def update_dialog_now(self):
        return self.get_lang_text("update_dialog_now")

    def report_dialog_uploaded_by_users_report_it(self):
        return self.get_lang_text("report_dialog_uploaded_by_users_report_it")

    def report_dialog_uploaded_by_users_des(self):
        return self.get_lang_text("report_dialog_uploaded_by_users_des")

    def report_dialog_report(self):
        return self.get_lang_text("report_dialog_report")

    def report_dialog_drama_upload(self):
        return self.get_lang_text("report_dialog_drama_upload")

    def report_dialog_upload_drama(self):
        return self.get_lang_text("report_dialog_upload_drama")

    def report_dialog_add_cover(self):
        return self.get_lang_text("report_dialog_add_cover")

    def report_dialog_your_drama_and_win_coins(self):
        return self.get_lang_text("report_dialog_your_drama_and_win_coins")

    def report_dialog_drama_cover(self):
        return self.get_lang_text("report_dialog_drama_cover")

    def report_dialog_drama_name(self):
        return self.get_lang_text("report_dialog_drama_name")

    def report_dialog_drama_name_hint(self):
        return self.get_lang_text("report_dialog_drama_name_hint")

    def report_dialog_drama_name_length_hint(self):
        return self.get_lang_text("report_dialog_drama_name_length_hint")

    def report_dialog_your_email(self):
        return self.get_lang_text("report_dialog_your_email")

    def report_dialog_your_email_hint(self):
        return self.get_lang_text("report_dialog_your_email_hint")

    def report_dialog_upload_video(self):
        return self.get_lang_text("report_dialog_upload_video")

    def report_dialog_apply(self):
        return self.get_lang_text("report_dialog_apply")

    def report_dialog_under_review(self):
        return self.get_lang_text("report_dialog_under_review")

    def report_dialog_report_succeed(self):
        return self.get_lang_text("report_dialog_report_succeed")

    def report_dialog_re_upload(self):
        return self.get_lang_text("report_dialog_re_upload")

    def report_dialog_upload_permission(self):
        return self.get_lang_text("report_dialog_upload_permission")

    def my_wallet_fragment_title(self):
        return self.get_lang_text("my_wallet_fragment_title")

    def my_wallet_fragment_empty_record(self):
        return self.get_lang_text("my_wallet_fragment_empty_record")

    def my_wallet_fragment_discount(self):
        return self.get_lang_text("my_wallet_fragment_discount")

    def my_wallet_fragment_coins_record(self):
        return self.get_lang_text("my_wallet_fragment_coins_record")

    def my_wallet_fragment_bonus_record(self):
        return self.get_lang_text("my_wallet_fragment_bonus_record")

    def my_wallet_fragment_unused(self):
        return self.get_lang_text("my_wallet_fragment_unused")

    def my_wallet_fragment_used(self):
        return self.get_lang_text("my_wallet_fragment_used")

    def act_app_open_skip(self):
        return self.get_lang_text("act_app_open_skip")

    def home_login_guide_dialog_title(self):
        return self.get_lang_text("home_login_guide_dialog_title")

    def home_login_guide_dialog_button(self):
        return self.get_lang_text("home_login_guide_dialog_button")

    def logout_tip_dialog_title(self):
        return self.get_lang_text("logout_tip_dialog_title")

    def logout_tip_dialog_desc_1(self):
        return self.get_lang_text("logout_tip_dialog_desc_1")

    def logout_tip_dialog_desc_2(self):
        return self.get_lang_text("logout_tip_dialog_desc_2")

    def logout_tip_dialog_desc_3(self):
        return self.get_lang_text("logout_tip_dialog_desc_3")

    def logout_tip_dialog_desc_4(self):
        return self.get_lang_text("logout_tip_dialog_desc_4")

    def logout_tip_dialog_reconsider(self):
        return self.get_lang_text("logout_tip_dialog_reconsider")

    def merge_tourist_dialog_title(self):
        return self.get_lang_text("merge_tourist_dialog_title")

    def merge_tourist_dialog_content(self):
        return self.get_lang_text("merge_tourist_dialog_content")

    def merge_tourist_dialog_processing(self):
        return self.get_lang_text("merge_tourist_dialog_processing")

    def merge_tourist_dialog_succeed_title(self):
        return self.get_lang_text("merge_tourist_dialog_succeed_title")

    def merge_tourist_dialog_succeed_content(self):
        return self.get_lang_text("merge_tourist_dialog_succeed_content")

    def merge_tourist_dialog_failed(self):
        return self.get_lang_text("merge_tourist_dialog_failed")

    def merge_tourist_dialog_retry(self):
        return self.get_lang_text("merge_tourist_dialog_retry")

    def gdpr_refusing_toast(self):
        return self.get_lang_text("gdpr_refusing_toast")

    def push_check_in_title_0(self):
        return self.get_lang_text("push_check_in_title_0")

    def push_check_in_title_1(self):
        return self.get_lang_text("push_check_in_title_1")

    def push_check_in_title_2(self):
        return self.get_lang_text("push_check_in_title_2")

    def push_check_in_title_3(self):
        return self.get_lang_text("push_check_in_title_3")

    def push_check_in_title_4(self):
        return self.get_lang_text("push_check_in_title_4")

    def push_check_in_title_new_0(self):
        return self.get_lang_text("push_check_in_title_new_0")

    def push_check_in_title_new_1(self):
        return self.get_lang_text("push_check_in_title_new_1")

    def push_check_in_title_new_2(self):
        return self.get_lang_text("push_check_in_title_new_2")

    def push_check_in_title_new_3(self):
        return self.get_lang_text("push_check_in_title_new_3")

    def push_check_in_title_new_4(self):
        return self.get_lang_text("push_check_in_title_new_4")

    def push_check_in_contents_0(self):
        return self.get_lang_text("push_check_in_contents_0")

    def push_check_in_contents_1(self):
        return self.get_lang_text("push_check_in_contents_1")

    def push_check_in_contents_2(self):
        return self.get_lang_text("push_check_in_contents_2")

    def push_check_in_contents_3(self):
        return self.get_lang_text("push_check_in_contents_3")

    def push_check_in_contents_4(self):
        return self.get_lang_text("push_check_in_contents_4")

    def push_check_in_contents_new_0(self):
        return self.get_lang_text("push_check_in_contents_new_0")

    def push_check_in_contents_new_1(self):
        return self.get_lang_text("push_check_in_contents_new_1")

    def push_check_in_contents_new_2(self):
        return self.get_lang_text("push_check_in_contents_new_2")

    def push_check_in_contents_new_3(self):
        return self.get_lang_text("push_check_in_contents_new_3")

    def push_check_in_contents_new_4(self):
        return self.get_lang_text("push_check_in_contents_new_4")

    def push_expansion_sku_title_0(self):
        return self.get_lang_text("push_expansion_sku_title_0")

    def push_expansion_sku_title_1(self):
        return self.get_lang_text("push_expansion_sku_title_1")

    def push_expansion_sku_title_2(self):
        return self.get_lang_text("push_expansion_sku_title_2")

    def push_expansion_sku_title_3(self):
        return self.get_lang_text("push_expansion_sku_title_3")

    def push_expansion_sku_title_4(self):
        return self.get_lang_text("push_expansion_sku_title_4")

    def push_expansion_sku_content_0(self):
        return self.get_lang_text("push_expansion_sku_content_0")

    def push_expansion_sku_content_1(self):
        return self.get_lang_text("push_expansion_sku_content_1")

    def push_expansion_sku_content_2(self):
        return self.get_lang_text("push_expansion_sku_content_2")

    def push_expansion_sku_content_3(self):
        return self.get_lang_text("push_expansion_sku_content_3")

    def push_expansion_sku_content_4(self):
        return self.get_lang_text("push_expansion_sku_content_4")

    def profile_subscription_view_default_title(self):
        return self.get_lang_text("profile_subscription_view_default_title")

    def profile_subscription_view_default_content(self):
        return self.get_lang_text("profile_subscription_view_default_content")

    def profile_subscription_view_unsubscribed(self):
        return self.get_lang_text("profile_subscription_view_unsubscribed")

    def profile_subscription_view_subscribed(self):
        return self.get_lang_text("profile_subscription_view_subscribed")

    def profile_subscription_view_weekly_card(self):
        return self.get_lang_text("profile_subscription_view_weekly_card")

    def profile_subscription_view_monthly_card(self):
        return self.get_lang_text("profile_subscription_view_monthly_card")

    def profile_subscription_view_annual_card(self):
        return self.get_lang_text("profile_subscription_view_annual_card")

    def profile_subscription_view_weekly_pro_card(self):
        return self.get_lang_text("profile_subscription_view_weekly_pro_card")

    def profile_subscription_view_monthly_pro_card(self):
        return self.get_lang_text("profile_subscription_view_monthly_pro_card")

    def profile_subscription_view_annual_pro_card(self):
        return self.get_lang_text("profile_subscription_view_annual_pro_card")

    def profile_subscription_view_weekly_pro_card_desc(self):
        return self.get_lang_text("profile_subscription_view_weekly_pro_card_desc")

    def profile_subscription_view_monthly_pro_card_desc(self):
        return self.get_lang_text("profile_subscription_view_monthly_pro_card_desc")

    def profile_subscription_view_annual_pro_card_desc(self):
        return self.get_lang_text("profile_subscription_view_annual_pro_card_desc")

    def profile_subscription_view_expire_time(self):
        return self.get_lang_text("profile_subscription_view_expire_time")

    def profile_subscription_view_unsupport_product(self):
        return self.get_lang_text("profile_subscription_view_unsupport_product")

    def subscription_detail_activity_title(self):
        return self.get_lang_text("subscription_detail_activity_title")

    def subscription_detail_activity_privilege_title(self):
        return self.get_lang_text("subscription_detail_activity_privilege_title")

    def subscription_detail_activity_desc_title(self):
        return self.get_lang_text("subscription_detail_activity_desc_title")

    def subscription_detail_activity_pro_desc_content(self):
        return self.get_lang_text("subscription_detail_activity_pro_desc_content")

    def subscription_detail_activity_privilege_3_desc(self):
        return self.get_lang_text("subscription_detail_activity_privilege_3_desc")

    def subscription_detail_activity_privilege_4_desc(self):
        return self.get_lang_text("subscription_detail_activity_privilege_4_desc")

    def subscription_detail_activity_privilege_5_desc(self):
        return self.get_lang_text("subscription_detail_activity_privilege_5_desc")

    def subscription_detail_activity_subs_success(self):
        return self.get_lang_text("subscription_detail_activity_subs_success")

    def subscription_day_bonus_claimed(self):
        return self.get_lang_text("subscription_day_bonus_claimed")

    def campaign_shorts_tip_float_view_title(self):
        return self.get_lang_text("campaign_shorts_tip_float_view_title")

    def subs_type_view_total_earning(self):
        return self.get_lang_text("subs_type_view_total_earning")

    def subs_type_view_total_earning_2(self):
        return self.get_lang_text("subs_type_view_total_earning_2")

    def subs_type_view_get_now(self):
        return self.get_lang_text("subs_type_view_get_now")

    def subs_type_view_first_recharge_tip(self):
        return self.get_lang_text("subs_type_view_first_recharge_tip")

    def subs_type_view_detail(self):
        return self.get_lang_text("subs_type_view_detail")

    def subs_type_view_disable_subs_tip(self):
        return self.get_lang_text("subs_type_view_disable_subs_tip")

    def subs_type_view_claim_bonus(self):
        return self.get_lang_text("subs_type_view_claim_bonus")

    def subs_type_view_old_test_claim_bonus(self):
        return self.get_lang_text("subs_type_view_old_test_claim_bonus")

    def subs_type_view_per_week(self):
        return self.get_lang_text("subs_type_view_per_week")

    def subs_type_view_per_month(self):
        return self.get_lang_text("subs_type_view_per_month")

    def subs_type_view_per_year(self):
        return self.get_lang_text("subs_type_view_per_year")

    def subs_type_view_renew_per_week(self):
        return self.get_lang_text("subs_type_view_renew_per_week")

    def subs_type_view_renew_per_month(self):
        return self.get_lang_text("subs_type_view_renew_per_month")

    def subs_type_view_renew_per_year(self):
        return self.get_lang_text("subs_type_view_renew_per_year")

    def language_app(self):
        return self.get_lang_text("language_app")

    def language_en(self):
        return self.get_lang_text("language_en")

    def language_zh_simplified(self):
        return self.get_lang_text("language_zh_simplified")

    def language_zh_traditional(self):
        return self.get_lang_text("language_zh_traditional")

    def language_fil(self):
        return self.get_lang_text("language_fil")

    def language_hi(self):
        return self.get_lang_text("language_hi")

    def language_in(self):
        return self.get_lang_text("language_in")

    def language_ja(self):
        return self.get_lang_text("language_ja")

    def language_ko(self):
        return self.get_lang_text("language_ko")

    def language_th(self):
        return self.get_lang_text("language_th")

    def language_ar(self):
        return self.get_lang_text("language_ar")

    def language_es(self):
        return self.get_lang_text("language_es")

    def language_pt(self):
        return self.get_lang_text("language_pt")

    def language_vi(self):
        return self.get_lang_text("language_vi")

    def language_de(self):
        return self.get_lang_text("language_de")

    def language_fr(self):
        return self.get_lang_text("language_fr")

    def restore_tip_view_tip(self):
        return self.get_lang_text("restore_tip_view_tip")

    def restore_tip_view_refresh(self):
        return self.get_lang_text("restore_tip_view_refresh")

    def purchase_failed_tip_dialog_desc(self):
        return self.get_lang_text("purchase_failed_tip_dialog_desc")

    def shorts_fragment_trailer_enter_immersion(self):
        return self.get_lang_text("shorts_fragment_trailer_enter_immersion")

    def shorts_fragment_current_episode_finished(self):
        return self.get_lang_text("shorts_fragment_current_episode_finished")

    def shorts_fragment_current_episode_updating(self):
        return self.get_lang_text("shorts_fragment_current_episode_updating")

    def shorts_fragment_next_episode_tip(self):
        return self.get_lang_text("shorts_fragment_next_episode_tip")

    def shorts_fragment_trailer(self):
        return self.get_lang_text("shorts_fragment_trailer")

    def shorts_fragment_trailer_in_production(self):
        return self.get_lang_text("shorts_fragment_trailer_in_production")

    def search_activity_history_title(self):
        return self.get_lang_text("search_activity_history_title")

    def search_activity_popular_title(self):
        return self.get_lang_text("search_activity_popular_title")

    def search_activity_no_result(self):
        return self.get_lang_text("search_activity_no_result")

    def search_activity_more_no_result(self):
        return self.get_lang_text("search_activity_more_no_result")

    def search_activity_input_keyword_hint(self):
        return self.get_lang_text("search_activity_input_keyword_hint")

    def search_activity_clear_history_hint(self):
        return self.get_lang_text("search_activity_clear_history_hint")

    def search_activity_search_frequently_tips(self):
        return self.get_lang_text("search_activity_search_frequently_tips")

    def search_activity_redeem_code_disabled(self):
        return self.get_lang_text("search_activity_redeem_code_disabled")

    def search_activity_redeem_code_delisted(self):
        return self.get_lang_text("search_activity_redeem_code_delisted")

    def search_activity_redeem_code_overdue(self):
        return self.get_lang_text("search_activity_redeem_code_overdue")

    def search_activity_redeem_code_use_up(self):
        return self.get_lang_text("search_activity_redeem_code_use_up")

    def search_activity_redeem_code_unsupported(self):
        return self.get_lang_text("search_activity_redeem_code_unsupported")

    def ad_retention_dialog_fragment_content(self):
        return self.get_lang_text("ad_retention_dialog_fragment_content")

    def ad_retention_dialog_fragment_unlocked_today(self):
        return self.get_lang_text("ad_retention_dialog_fragment_unlocked_today")

    def pure_paying_user_ad_retention_dialog_fragment_unlocked_today(self):
        return self.get_lang_text("pure_paying_user_ad_retention_dialog_fragment_unlocked_today")

    def new_recommend_shorts_fragment_title(self):
        return self.get_lang_text("new_recommend_shorts_fragment_title")

    def new_recommend_shorts_fragment_more_tip(self):
        return self.get_lang_text("new_recommend_shorts_fragment_more_tip")

    def new_recommend_shorts_fragment_more(self):
        return self.get_lang_text("new_recommend_shorts_fragment_more")

    def new_recommend_shorts_fragment_must_read(self):
        return self.get_lang_text("new_recommend_shorts_fragment_must_read")

    def subs_pro_expired_dialog_content(self):
        return self.get_lang_text("subs_pro_expired_dialog_content")

    def redeem_code_dialog_fragment_redemption_successful(self):
        return self.get_lang_text("redeem_code_dialog_fragment_redemption_successful")

    def redeem_code_dialog_fragment_receive_benefits(self):
        return self.get_lang_text("redeem_code_dialog_fragment_receive_benefits")

    def redeem_code_dialog_fragment_received(self):
        return self.get_lang_text("redeem_code_dialog_fragment_received")

    def play_episode_activity_pip_guide_title(self):
        return self.get_lang_text("play_episode_activity_pip_guide_title")

    def play_episode_activity_pip_guide_content(self):
        return self.get_lang_text("play_episode_activity_pip_guide_content")

    def discover_more_fragment_empty_content(self):
        return self.get_lang_text("discover_more_fragment_empty_content")

    def discover_more_fragment_empty_btn_text(self):
        return self.get_lang_text("discover_more_fragment_empty_btn_text")

    def discover_more_category_filter_fragment_all(self):
        return self.get_lang_text("discover_more_category_filter_fragment_all")

    def sign_in_reminder_fragment_btn(self):
        return self.get_lang_text("sign_in_reminder_fragment_btn")

    def sign_in_reminder_fragment_content(self):
        return self.get_lang_text("sign_in_reminder_fragment_content")

    def sign_in_success_dialog_content(self):
        return self.get_lang_text("sign_in_success_dialog_content")

    def sign_in_success_dialog_bonus(self):
        return self.get_lang_text("sign_in_success_dialog_bonus")

    def sign_in_watch_ad_fragment_content(self):
        return self.get_lang_text("sign_in_watch_ad_fragment_content")

    def sign_in_watch_ad_fragment_btn(self):
        return self.get_lang_text("sign_in_watch_ad_fragment_btn")

    def my_collection_fragment_drama_has_purchase(self):
        return self.get_lang_text("my_collection_fragment_drama_has_purchase")

    def immersion_activity_free_clarity_1080p(self):
        return self.get_lang_text("immersion_activity_free_clarity_1080p")

    def subscription_detail_activity_subs_update_success(self):
        return self.get_lang_text("subscription_detail_activity_subs_update_success")

    def subs_update_dialog_title(self):
        return self.get_lang_text("subs_update_dialog_title")

    def subscription_detail_activity_privilege_new_5_title(self):
        return self.get_lang_text("subscription_detail_activity_privilege_new_5_title")

    def ad_continue_dialog_fragment_content(self):
        return self.get_lang_text("ad_continue_dialog_fragment_content")

    def ad_continue_retention_dialog_fragment_title(self):
        return self.get_lang_text("ad_continue_retention_dialog_fragment_title")

    def ad_free_drama_dialog_fragment_content(self):
        return self.get_lang_text("ad_free_drama_dialog_fragment_content")


lang_mgr = LangMgr()

# 示例用法
if __name__ == "__main__":
    print(f"当前语言: {lang_mgr.app_language_code}")
    print(f"当前语言: {lang_mgr.login_activity_login_with()}")

    lang_mgr.switch_language("zh-CN")
    print(f"切换后语言: {lang_mgr.lang_key}")
    print(f"切换后语言: {lang_mgr.login_activity_login_with()}")

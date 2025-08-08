import pytest
import allure
from api_cases.tools.tools import login
from api_clients.Project_Name__ffff_api_app_test import ffff_dramaInfo_encrypt_dramaDetail, \
    ffff_dramaInfo_getDramaIdByShortPlayId, ffff_dramaInfo_dramaDetailV2
from utils.logger_manager import LoggerManager
from api_clients.新人推荐_test import ffff_recommend_checkNewUserRecommend, ffff_recommend_getNewUserRecommendInfo, \
    ffff_recommend_getNewUserTimeInfo
from api_clients.用户绑定相关_test import ffff_user_sendEmail, ffff_user_bindList, ffff_user_addBind, \
    ffff_user_bindByPhone, ffff_user_bindByEmail
from api_clients.支付相关_test import ffff_pay_android_recover, ffff_pay_iOS_recover, \
    ffff_pay_localDollarCurrencyConversion, ffff_pay_android_coinSkuBuy, ffff_pay_iOS_coinSkuBuy
from api_clients.订阅列表控制器_test import ffff_subscription_getProductListV3
from api_clients.feed流观看历史记录_test import ffff_feedWatchHistory_saveWatchHistory
from api_clients.SendMessageController_test import ffff_message_sendMessageVerificationCode
from api_clients.用户信息表_查询余额_test import ffff_user_reportDefaultShortPlay, ffff_user_getFBUserInfo, \
    ffff_user_setUserLanguage, ffff_user_reportUserAdInfo, ffff_user_reportActiveTime, ffff_user_getUserBalance, \
    ffff_user_getAnotherUserInfo, ffff_user_migrateAccount
from api_clients.系统管理相关接口_test import ffff_system_getConfigByKey, ffff_system_getUpgradeVersionManageInfo
from api_clients.广告相关接口_test import ffff_ad_watchAdUnLockComplete, ffff_ad_signWatchAd
from api_clients.首页推荐_轮播相关接口_test import ffff_homeData_encrypt_getBannerMore, \
    ffff_homeData_encrypt_getTabHomeData, ffff_homeData_getHomeConfig
from api_clients.app归因上报_test import ffff_adMatch_deepLinkReport
from api_clients.签到相关接口_test import ffff_sig_signRecord, ffff_sig_sign
from api_clients.累计看剧时长任务相关接口_test import ffff_watchTimeTask_getTaskConfig, ffff_watchTimeTask_receiveReward
from api_clients.任务相关接口_test import ffff_appTask_getAppTaskList, ffff_appTask_receiveRewards
from api_clients.签到提醒相关推送_test import ffff_push_sign_signReminder, ffff_push_sign_missSignReminder
from api_clients.挽留接口_test import ffff_retain_getComingSoonShortPlays, ffff_retain_getExitRetainShortPlays
from api_clients.活动资源位_配置_test import ffff_activityResource_resourceListByTypes
from api_clients.用户订阅信息_test import ffff_subscription_android, ffff_subscription_iosV2, ffff_subscription
from api_clients.观看历史记录_test import ffff_watchHistory_saveWatchHistory, ffff_watchHistory_delWatchHistory, \
    ffff_watchHistory_getWatchHistoryList
from api_clients.收藏相关接口_test import ffff_collect_cancelCollect, ffff_collect_batchCancelCollect, \
    ffff_collect_collectOp, ffff_collect_collectList
from api_clients._p__test import ffff_bonusRecord_getBonusTotal
from api_clients.用户配置信息接口_test import ffff_user_config, ffff_user_config
from api_clients.sku_相关接口_test import ffff_sku_getCoinsStoreListAndAdInfoBySkuModel, \
    ffff_sku_getUnlockedPageSkuList, ffff_sku_getCoinsStoreListBySkuModel
from api_clients.站内搜索_test import ffff_search_hotSearch, ffff_search_searchPage
from api_clients.用户设备信息_相关接口_test import ffff_userRegistrationToken_report
from api_clients.获取服务器时间_时间校正_test import ffff_correction_time
from api_clients.app初始化_上报_ua信息_test import ffff_appReport_lpReport
from api_clients.短剧解锁相关接口_test import ffff_shortPlay_unlockEpisodeByWatchAd, ffff_shortPlay_watchAdUnlockInfo, \
    ffff_shortPlay_unlockByWatchAd, ffff_shortPlay_unlockByCoin, ffff_shortPlay_unlockEpisodeByGold
from api_clients.奖励币过期推送接口_test import ffff_push_bonusExpiring_getPushInfo
from api_clients.落地页上报_test import ffff_clickAd_lpReport
from api_clients.短剧详情相关接口_test import ffff_shortPlay_shortPlayDetail, ffff_shortPlay_getTopRechargeShortPlays, \
    ffff_shortPlay_getSearchCarouselPlays, ffff_shortPlay_getPopularShortPlay
from api_clients.foryou_相关接口_test import ffff_forYou_encrypt_getForYouListOnlyOne, \
    ffff_forYou_encrypt_getForYouListPageNewV2
from api_clients.登录接口_test import ffff_login_tripartiteLogin, ffff_login_initLogin, ffff_login_getUserInfo, \
    ffff_login_deleteAccount, ffff_login_loginOut
from utils.my_mysql import update_user_coins_and_bonus


@allure.feature("高频接口汇总 - 自动生成")
class TestAllApis_success:
    @pytest.fixture(scope='function', autouse=True)
    def environment(self):
        LoggerManager().init(filename="TestAllApis")
        self.logger = LoggerManager().get_logger(name=__name__)
        with allure.step("用户登录"):
            self.client = login()
        yield
        with allure.step("用例环境清理"):
            self.logger.info("用例环境清理")

    @allure.title("ffff_recommend_checkNewUserRecommend 接口测试")
    def test_ffff_recommend_checkNewUserRecommend_success(self):
        ffff_recommend_checkNewUserRecommend(self.client)

    @allure.title("ffff_recommend_getNewUserRecommendInfo 接口测试")
    def test_ffff_recommend_getNewUserRecommendInfo_success(self):
        ffff_recommend_getNewUserRecommendInfo(self.client)

    @allure.title("ffff_recommend_getNewUserTimeInfo 接口测试")
    def test_ffff_recommend_getNewUserTimeInfo_success(self):
        ffff_recommend_getNewUserTimeInfo(self.client)

    # @allure.title("ffff_user_sendEmail 接口测试")
    # def test_ffff_user_sendEmail_success(self):
    #     ffff_user_sendEmail(self.client, email="luziyou@flareflow.ai")

    @allure.title("ffff_user_bindList 接口测试")
    def test_ffff_user_bindList_success(self):
        ffff_user_bindList(self.client)

    @allure.title("ffff_user_addBind 接口测试")
    def test_ffff_user_addBind_success(self):
        ffff_user_addBind(self.client)

    @allure.title("ffff_user_bindByPhone 接口测试")
    def test_ffff_user_bindByPhone_success(self):
        ffff_user_bindByPhone(self.client, phone="18888888888", areaCode="86")

    @allure.title("ffff_user_bindByEmail 接口测试")
    def test_ffff_user_bindByEmail_success(self):
        ffff_user_bindByEmail(self.client, email="luziyou@flareflow.ai", otp="520070")

    @allure.title("ffff_pay_localDollarCurrencyConversion 接口测试")
    def test_ffff_pay_localDollarCurrencyConversion_success(self):
        ffff_pay_localDollarCurrencyConversion(self.client)

    @allure.title("ffff_pay_android_coinSkuBuy 接口测试")
    def test_ffff_pay_android_coinSkuBuy_success(self):
        update_user_coins_and_bonus(self.client, self.client.user_id)
        ffff_pay_android_coinSkuBuy(self.client, shortPlayId=410360, episode=8)

    @allure.title("ffff_pay_iOS_coinSkuBuy 接口测试")
    def test_ffff_pay_iOS_coinSkuBuy_success(self):
        update_user_coins_and_bonus(self.client, self.client.user_id)
        ffff_pay_iOS_coinSkuBuy(self.client)

    @allure.title("ffff_subscription_getProductListV3 接口测试")
    def test_ffff_subscription_getProductListV3_success(self):
        ffff_subscription_getProductListV3(self.client)

    @allure.title("ffff_feedWatchHistory_saveWatchHistory 接口测试")
    def test_ffff_feedWatchHistory_saveWatchHistory_success(self):
        ffff_feedWatchHistory_saveWatchHistory(self.client, dramaId=410360, watchTime=99)

    @allure.title("ffff_message_sendMessageVerificationCode 接口测试")
    def test_ffff_message_sendMessageVerificationCode_success(self):
        ffff_message_sendMessageVerificationCode(self.client, phone="18888888888", areaCode="86")

    @allure.title("ffff_user_reportDefaultShortPlay 接口测试")
    def test_ffff_user_reportDefaultShortPlay_success(self):
        ffff_user_reportDefaultShortPlay(self.client)

    @allure.title("ffff_user_getFBUserInfo 接口测试")
    def test_ffff_user_getFBUserInfo_success(self):
        ffff_user_getFBUserInfo(self.client)

    @allure.title("ffff_user_setUserLanguage 接口测试")
    def test_ffff_user_setUserLanguage_success(self):
        ffff_user_setUserLanguage(self.client)

    @allure.title("ffff_user_reportUserAdInfo 接口测试")
    def test_ffff_user_reportUserAdInfo_success(self):
        ffff_user_reportUserAdInfo(self.client)

    @allure.title("ffff_user_reportActiveTime 接口测试")
    def test_ffff_user_reportActiveTime_success(self):
        ffff_user_reportActiveTime(self.client)

    @allure.title("ffff_user_getUserBalance 接口测试")
    def test_ffff_user_getUserBalance_success(self):
        ffff_user_getUserBalance(self.client)

    @allure.title("ffff_user_getAnotherUserInfo 接口测试")
    def test_ffff_user_getAnotherUserInfo_success(self):
        ffff_user_getAnotherUserInfo(self.client)

    @allure.title("ffff_user_migrateAccount 接口测试")
    def test_ffff_user_migrateAccount_success(self):
        ffff_user_migrateAccount(self.client, userId=self.client.user_id)

    @allure.title("ffff_system_getConfigByKey 接口测试")
    def test_ffff_system_getConfigByKey_success(self):
        ffff_system_getConfigByKey(self.client)

    @allure.title("ffff_ad_watchAdUnLockComplete 接口测试")
    def test_ffff_ad_watchAdUnLockComplete_success(self):
        ffff_ad_watchAdUnLockComplete(self.client, id=1)

    @allure.title("ffff_ad_signWatchAd 接口测试")
    def test_ffff_ad_signWatchAd_success(self):
        ffff_ad_watchAdUnLockComplete(self.client, id=1)
        ffff_ad_signWatchAd(self.client)

    @allure.title("ffff_homeData_encrypt_getTabHomeData 接口测试")
    def test_ffff_homeData_encrypt_getTabHomeData_success(self):
        ffff_homeData_encrypt_getTabHomeData(self.client)

    @allure.title("ffff_homeData_getHomeConfig 接口测试")
    def test_ffff_homeData_getHomeConfig_success(self):
        ffff_homeData_getHomeConfig(self.client)

    @allure.title("ffff_adMatch_deepLinkReport 接口测试")
    def test_ffff_adMatch_deepLinkReport_success(self):
        ffff_adMatch_deepLinkReport(self.client)

    @allure.title("ffff_sig_signRecord 接口测试")
    def test_ffff_sig_signRecord_success(self):
        ffff_sig_signRecord(self.client)

    @allure.title("ffff_sig_sign 接口测试")
    def test_ffff_sig_sign_success(self):
        ffff_sig_sign(self.client)

    @allure.title("ffff_watchTimeTask_getTaskConfig 接口测试")
    def test_ffff_watchTimeTask_getTaskConfig_success(self):
        ffff_watchTimeTask_getTaskConfig(self.client)

    @allure.title("ffff_watchTimeTask_receiveReward 接口测试")
    def test_ffff_watchTimeTask_receiveReward_success(self):
        ffff_watchTimeTask_receiveReward(self.client, [])

    @allure.title("ffff_appTask_getAppTaskList 接口测试")
    def test_ffff_appTask_getAppTaskList_success(self):
        ffff_appTask_getAppTaskList(self.client)

    @allure.title("ffff_appTask_receiveRewards 接口测试")
    def test_ffff_appTask_receiveRewards_success(self):
        ffff_appTask_receiveRewards(self.client)

    @allure.title("ffff_push_sign_signReminder 接口测试")
    def test_ffff_push_sign_signReminder_success(self):
        ffff_push_sign_signReminder(self.client)

    @allure.title("ffff_retain_getExitRetainShortPlays 接口测试")
    def test_ffff_retain_getExitRetainShortPlays_success(self):
        ffff_retain_getExitRetainShortPlays(self.client)

    @allure.title("ffff_activityResource_resourceListByTypes 接口测试")
    def test_ffff_activityResource_resourceListByTypes_success(self):
        ffff_activityResource_resourceListByTypes(self.client)

    @allure.title("ffff_subscription_android 接口测试")
    def test_ffff_subscription_android_success(self):
        ffff_subscription_android(self.client)

    @allure.title("ffff_subscription_iosV2 接口测试")
    def test_ffff_subscription_iosV2_success(self):
        ffff_subscription_iosV2(self.client)

    @allure.title("ffff_watchHistory_saveWatchHistory 接口测试")
    def test_ffff_watchHistory_saveWatchHistory_success(self):
        ffff_watchHistory_saveWatchHistory(self.client, watchTime=1000, dramaId=410360)

    @allure.title("ffff_watchHistory_delWatchHistory 接口测试")
    def test_ffff_watchHistory_delWatchHistory_success(self):
        ffff_watchHistory_delWatchHistory(self.client, businessIdList=[410360])

    @allure.title("ffff_watchHistory_getWatchHistoryList 接口测试")
    def test_ffff_watchHistory_getWatchHistoryList_success(self):
        ffff_watchHistory_getWatchHistoryList(self.client, lastTime=0, pageSize=30)

    @allure.title("ffff_collect_cancelCollect 接口测试")
    def test_ffff_collect_cancelCollect_success(self):
        ffff_collect_cancelCollect(self.client, collectSource=1, colletType=1, businessId=410360)

    @allure.title("ffff_collect_batchCancelCollect 接口测试")
    def test_ffff_collect_batchCancelCollect_success(self):
        ffff_collect_batchCancelCollect(self.client, businessIdList=[410360])

    @allure.title("ffff_collect_collectOp 接口测试")
    def test_ffff_collect_collectOp_success(self):
        ffff_collect_collectOp(self.client, businessId=410360, scene=1, colletType=1, watchTime=1000, dramaId=410360,
                               collectSource=1)

    @allure.title("ffff_collect_collectList 接口测试")
    def test_ffff_collect_collectList_success(self):
        ffff_collect_collectList(self.client, pageSize=30, lastTime=1754567730123, colletType=2, collectSource=[2])

    @allure.title("ffff_dramaInfo_dramaDetailV2 接口测试")
    def test_ffff_dramaInfo_dramaDetailV2_success(self):
        ffff_dramaInfo_dramaDetailV2(self.client, shortPlayId=728600, episodeNum=1)

    @allure.title("ffff_dramaInfo_encrypt_dramaDetail 接口测试")
    def test_ffff_dramaInfo_encrypt_dramaDetail_success(self):
        # mg_drama 中的id
        ffff_dramaInfo_encrypt_dramaDetail(self.client, businessId=407328)

    @allure.title("ffff_dramaInfo_getDramaIdByShortPlayId 接口测试")
    def test_ffff_dramaInfo_getDramaIdByShortPlayId_success(self):
        ffff_dramaInfo_getDramaIdByShortPlayId(self.client, businessId=728612)

    @allure.title("ffff_user_config 接口测试")
    def test_ffff_user_config_success(self):
        ffff_user_config(self.client)

    @allure.title("ffff_sku_getCoinsStoreListBySkuModel 接口测试")
    def test_ffff_sku_getCoinsStoreListBySkuModel_success(self):
        ffff_sku_getCoinsStoreListBySkuModel(self.client)

    @allure.title("ffff_search_searchPage 接口测试")
    def test_ffff_search_searchPage_success(self):
        ffff_search_searchPage(self.client)

    @allure.title("ffff_userRegistrationToken_report 接口测试")
    def test_ffff_userRegistrationToken_report_success(self):
        ffff_userRegistrationToken_report(self.client)

    @allure.title("ffff_correction_time 接口测试")
    def test_ffff_correction_time_success(self):
        ffff_correction_time(self.client)

    @allure.title("ffff_appReport_lpReport 接口测试")
    def test_ffff_appReport_lpReport_success(self):
        ffff_appReport_lpReport(self.client)

    @allure.title("ffff_shortPlay_unlockEpisodeByWatchAd 接口测试")
    def test_ffff_shortPlay_unlockEpisodeByWatchAd_success(self):
        ffff_shortPlay_unlockEpisodeByWatchAd(self.client, shortPlayId=728600, episodeNum=8)

    @allure.title("ffff_shortPlay_watchAdUnlockInfo 接口测试")
    def test_ffff_shortPlay_watchAdUnlockInfo_success(self):
        ffff_shortPlay_watchAdUnlockInfo(self.client, businessId=1)

    @allure.title("ffff_shortPlay_unlockByWatchAd 接口测试")
    def test_ffff_shortPlay_unlockByWatchAd_success(self):
        ffff_shortPlay_unlockByWatchAd(self.client, businessId=407328, autoUnlock=True)

    @allure.title("ffff_shortPlay_unlockByCoin 接口测试")
    def test_ffff_shortPlay_unlockByCoin_success(self):
        # 前置充钱
        update_user_coins_and_bonus(self.client.user_id)
        ffff_shortPlay_unlockByCoin(self.client, businessId=407328)

    @allure.title("ffff_shortPlay_unlockEpisodeByGold 接口测试")
    def test_ffff_shortPlay_unlockEpisodeByGold_success(self):
        # 前置充钱
        update_user_coins_and_bonus(self.client.user_id)
        ffff_shortPlay_unlockEpisodeByGold(self.client, shortPlayId=728601, episodeNum=8)

    @allure.title("ffff_push_bonusExpiring_getPushInfo 接口测试")
    def test_ffff_push_bonusExpiring_getPushInfo_success(self):
        ffff_push_bonusExpiring_getPushInfo(self.client)

    @allure.title("ffff_clickAd_lpReport 接口测试")
    def test_ffff_clickAd_lpReport_success(self):
        ffff_clickAd_lpReport(self.client)

    @allure.title("ffff_shortPlay_shortPlayDetail 接口测试")
    def test_ffff_shortPlay_shortPlayDetail_success(self):
        # short_play_code
        ffff_shortPlay_shortPlayDetail(self.client, businessId=728600)

    @allure.title("ffff_shortPlay_getTopRechargeShortPlays 接口测试")
    def test_ffff_shortPlay_getTopRechargeShortPlays_success(self):
        ffff_shortPlay_getTopRechargeShortPlays(self.client)

    @allure.title("ffff_shortPlay_getSearchCarouselPlays 接口测试")
    def test_ffff_shortPlay_getSearchCarouselPlays_success(self):
        ffff_shortPlay_getSearchCarouselPlays(self.client)

    @allure.title("ffff_shortPlay_getPopularShortPlay 接口测试")
    def test_ffff_shortPlay_getPopularShortPlay_success(self):
        ffff_shortPlay_getPopularShortPlay(self.client)

    @allure.title("ffff_forYou_encrypt_getForYouListOnlyOne 接口测试")
    def test_ffff_forYou_encrypt_getForYouListOnlyOne_success(self):
        ffff_forYou_encrypt_getForYouListOnlyOne(self.client)

    @allure.title("ffff_login_initLogin 接口测试")
    def test_ffff_login_initLogin_success(self):
        ffff_login_initLogin(self.client, deviceId="12345678901")

    @allure.title("ffff_login_getUserInfo 接口测试")
    def test_ffff_login_getUserInfo_success(self):
        ffff_login_getUserInfo(self.client)

    @allure.title("ffff_login_deleteAccount 接口测试")
    def test_ffff_login_deleteAccount_success(self):
        ffff_login_deleteAccount(self.client)

    @allure.title("ffff_login_loginOut 接口测试")
    def test_ffff_login_loginOut_success(self):
        ffff_login_loginOut(self.client)


@allure.feature("高频接口汇总 - 待调试")
class TestAllApis_check:
    @pytest.fixture(scope='function', autouse=True)
    def environment(self):
        LoggerManager().init(filename="TestAllApis")
        self.logger = LoggerManager().get_logger(name=__name__)
        with allure.step("用户登录"):
            self.client = login()
        yield
        with allure.step("用例环境清理"):
            self.logger.info("用例环境清理")

    @allure.title("ffff_login_tripartiteLogin 接口测试")
    def test_ffff_login_tripartiteLogin_success(self):
        ffff_login_tripartiteLogin(self.client)

    @allure.title("ffff_forYou_encrypt_getForYouListPageNewV2 接口测试")
    def test_ffff_forYou_encrypt_getForYouListPageNewV2_success(self):
        ffff_forYou_encrypt_getForYouListPageNewV2(self.client, pageSize=10, pageNum=1)

    @allure.title("ffff_sku_getUnlockedPageSkuList 接口测试")
    def test_ffff_sku_getUnlockedPageSkuList_success(self):
        ffff_sku_getUnlockedPageSkuList(self.client)

    @allure.title("ffff_search_hotSearch 接口测试")
    def test_ffff_search_hotSearch_success(self):
        ffff_search_hotSearch(self.client)

    @allure.title("ffff_homeData_encrypt_getBannerMore 接口测试")
    def test_ffff_homeData_encrypt_getBannerMore_success(self):
        ffff_homeData_encrypt_getBannerMore(self.client)

    @allure.title("ffff_system_getUpgradeVersionManageInfo 接口测试")
    def test_ffff_system_getUpgradeVersionManageInfo_success(self):
        ffff_system_getUpgradeVersionManageInfo(self.client)

    @allure.title("ffff_pay_android_recover 接口测试")
    def test_ffff_pay_android_recover_success(self):
        ffff_pay_android_recover(self.client)

    @allure.title("ffff_pay_iOS_recover 接口测试")
    def test_ffff_pay_iOS_recover_success(self):
        ffff_pay_iOS_recover(self.client)

    @allure.title("ffff_subscription 接口测试")
    def test_ffff_subscription_success(self):
        ffff_subscription(self.client)

    @allure.title("ffff_sku_getCoinsStoreListAndAdInfoBySkuModel 接口测试")
    def test_ffff_sku_getCoinsStoreListAndAdInfoBySkuModel_success(self):
        ffff_sku_getCoinsStoreListAndAdInfoBySkuModel(self.client)

    @allure.title("ffff_bonusRecord_getBonusTotal 接口测试")
    def test_ffff_bonusRecord_getBonusTotal_success(self):
        ffff_bonusRecord_getBonusTotal(self.client)

    @allure.title("ffff_push_sign_missSignReminder 接口测试")
    def test_ffff_push_sign_missSignReminder_success(self):
        ffff_push_sign_missSignReminder(self.client)

    @allure.title("ffff_retain_getComingSoonShortPlays 接口测试")
    def test_ffff_retain_getComingSoonShortPlays_success(self):
        ffff_retain_getComingSoonShortPlays(self.client)

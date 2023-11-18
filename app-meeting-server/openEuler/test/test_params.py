import copy
import json
import logging
from rest_framework import status
from rest_framework.test import APITestCase
from openeuler.models import User, GroupUser, Meeting, Collect, Activity, ActivityCollect
from openeuler.test.common import create_user, create_group, create_meetings_sponsor_user, create_meeting_admin_user, \
    get_user, create_activity_sponsor_user, create_activity_admin_user

from openeuler.test.constant import xss_script, crlf_text, html_text

logger = logging.getLogger("django")


# noinspection PyUnresolvedReferences
class TestCommon(APITestCase):

    def get_client(self, user, token):
        c = self.client
        c.force_authenticate(user, token)
        return c

    def init_user(self, count_data=50):
        for i in range(count_data):
            create_user("username_{}".format(i), "openid_{}".format(i))

    def init_group(self, count_data=50):
        group = create_group("group_user")
        self.init_user(count_data)
        return group

    def init_meetings(self, data, is_admin=False):
        data = copy.deepcopy(data)
        group = create_group(data["group_name"])
        data["group_id"] = group.id
        if not is_admin:
            token, user = create_meetings_sponsor_user("sponsor", "sponsor_openid")
        else:
            token, user = create_meeting_admin_user("sponsor", "sponsor_openid")
        return token, user, data

    def tearDown(self) -> None:
        ret = GroupUser.objects.all().delete()
        logger.info("delete group user and result is:{}".format(str(ret)))
        ret = Meeting.objects.all().delete()
        logger.info("delete meeting and result is:{}".format(str(ret)))
        ret = Collect.objects.all().delete()
        logger.info("delete meeting collect and result is:{}".format(str(ret)))
        ret = Activity.objects.all().delete()
        logger.info("delete activity and result is:{}".format(str(ret)))
        ret = ActivityCollect.objects.all().delete()
        logger.info("delete activity collect and result is:{}".format(str(ret)))
        ret = User.objects.all().delete()
        logger.info("delete user and result is:{}".format(str(ret)))


class LoginViewTest(APITestCase):
    value = "*" * 16
    url = "/login/"

    def test_login_lack_openid(self):
        ret = self.client.post(self.url, data=dict())
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_openid(self):
        ret = self.client.post(self.url, data={"code": "*" * 129})
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_empty_openid(self):
        ret = self.client.post(self.url, data={"code": ""})
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)


class RefreshViewTest(APITestCase):
    url = "/refresh/"

    def test_refresh_lack_refresh(self):
        ret = self.client.post(self.url, data={})
        self.assertEqual(ret.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_not_match(self):
        ret = self.client.post(self.url, data={"refresh": "match"})
        self.assertEqual(ret.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_ok(self):
        _, refresh_token, user = create_user("test_refresh_ok", "test_refresh_ok")
        ret = self.client.post(self.url, data={"refresh": refresh_token})
        self.assertEqual(ret.status_code, status.HTTP_200_OK)

    def test_refresh_expired(self):
        """Need to test manually"""
        pass


class LogoutViewTest(TestCommon):
    url = "/logout/"

    def test_logout_ok(self):
        token, _, user = create_user("test_logout_ok", "test_logout_ok")
        c = self.get_client(user, token)
        ret = c.post(self.url)
        self.assertEqual(ret.status_code, status.HTTP_200_OK)


class LogoffViewTest(TestCommon):
    url = "/logoff/"

    def test_logoff_ok(self):
        header, _, user = create_user("test_logout_ok", "test_logout_ok")
        c = self.get_client(user, header)
        ret = c.post(self.url)
        self.assertEqual(ret.status_code, status.HTTP_200_OK)


class AgreePrivacyPolicyViewTest(TestCommon):
    url = "/agree/"

    def test_agree_privacy_ok(self):
        header, _, user = create_user("test_logout_ok", "test_logout_ok")
        c = self.get_client(user, header)
        ret = c.put(self.url)
        self.assertEqual(ret.status_code, status.HTTP_200_OK)


class RevokeAgreementViewTest(TestCommon):
    url = "/revoke/"

    def test_revoke_agree_privacy_ok(self):
        header, _, user = create_user("test_logout_ok", "test_logout_ok")
        c = self.get_client(user, header)
        ret = c.post(self.url)
        self.assertEqual(ret.status_code, status.HTTP_200_OK)


class GroupUserAddViewTest(TestCommon):
    url = "/groupuser/action/new/"
    data = {
        "group_id": "",
        "ids": "1-2"
    }

    def test_with_ok(self):
        group = create_group("group1")
        for i in range(50):
            create_user("username_{}".format(i), "openid_{}".format(i))
        self.data["group_id"] = group.id
        self.data["ids"] = "-".join([str(i) for i in User.objects.values_list("id", flat=True)])
        token, user = create_meeting_admin_user("user_admin")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_200_OK)

    def test_over_user_count(self):
        group = create_group("group1")
        for i in range(51):
            create_user("username_{}".format(i), "openid_{}".format(i))
        self.data["group_id"] = group.id
        self.data["ids"] = "-".join([str(i) for i in User.objects.values_list("id", flat=True)])
        token, user = create_meeting_admin_user("user_admin")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_count_eq_zero(self):
        group = create_group("group1")
        create_user("username_0", "openid_0")
        self.data["group_id"] = group.id
        self.data["ids"] = ""
        token, user = create_meeting_admin_user("user_admin")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_count_not_eq_int(self):
        group = create_group("group1")
        create_user("username_0", "openid_0")
        user = User.objects.get(nickname="username_0")
        self.data["group_id"] = group.id
        self.data["ids"] = "{}-xxx".format(user.id)
        token, user = create_meeting_admin_user("user_admin")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_group_not_exist(self):
        create_user("username_0", "openid_0")
        user = User.objects.get(nickname="username_0")
        self.data["group_id"] = str(1)
        self.data["ids"] = "{}".format(user.id)
        token, user = create_meeting_admin_user("user_admin")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_permission(self):
        token, user = create_meetings_sponsor_user()
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_permission_2(self):
        token, _, user = create_user()
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)


class GroupUserDelViewTest(TestCommon):
    url = "/groupuser/action/del/"
    data = {
        "group_id": "",
        "ids": "1-2"
    }

    def test_with_ok(self):
        group = self.init_group()
        self.data["group_id"] = group.id
        self.data["ids"] = "-".join([str(i) for i in User.objects.values_list("id", flat=True)])
        token, user = create_meeting_admin_user("user_admin1", "user_admin1")
        c = self.get_client(user, token)
        c.post(GroupUserAddViewTest.url, data=self.data)
        token, user = create_meeting_admin_user("user_admin2", "user_admin2")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_200_OK)

    def test_over_user_count(self):
        group = create_group("group1")
        for i in range(51):
            create_user("username_{}".format(i), "openid_{}".format(i))
        self.data["group_id"] = group.id
        self.data["ids"] = "-".join([str(i) for i in User.objects.values_list("id", flat=True)])
        token, user = create_meeting_admin_user("user_admin", "user_admin")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_count_eq_zero(self):
        group = create_group("group1")
        create_user("username_0", "openid_0")
        self.data["group_id"] = group.id
        self.data["ids"] = ""
        token, user = create_meeting_admin_user("user_admin", "user_admin")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_count_not_eq_int(self):
        group = create_group("group1")
        create_user("username_0", "openid_0")
        user = User.objects.get(nickname="username_0")
        self.data["group_id"] = group.id
        self.data["ids"] = "{}-xxx".format(user.id)
        token, user = create_meeting_admin_user("user_admin", "user_admin")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_group_not_exist(self):
        create_user("username_0", "openid_0")
        user = User.objects.get(nickname="username_0")
        self.data["group_id"] = str(1)
        self.data["ids"] = "{}".format(user.id)
        token, user = create_meeting_admin_user("user_admin", "user_admin")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_not_all_in_group_user(self):
        group = self.init_group()
        self.data["group_id"] = group.id
        user_ids = "-".join([str(i) for i in User.objects.filter(id__lt=10).values_list("id", flat=True)])
        self.data["ids"] = user_ids + "-100000"
        token, user = create_meeting_admin_user("user_admin", "user_admin")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_permission(self):
        token, user = create_meetings_sponsor_user()
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_permission_2(self):
        token, _, user = create_user()
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)


class SponsorAddViewTest(TestCommon):
    url = "/sponsor/action/new/"
    data = {
        "ids": "1-2"
    }

    def test_ok(self):
        self.init_user(50)
        users = User.objects.all().values_list("id", flat=True)
        self.data["ids"] = "-".join([str(i) for i in users])
        token, user = create_activity_admin_user("user_admin")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_200_OK)

    def test_over_count(self):
        self.init_user(60)
        users = User.objects.all().values_list("id", flat=True)
        self.data["ids"] = "-".join([str(i) for i in users])
        token, user = create_activity_admin_user("user_admin")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lt_zero(self):
        self.init_user(1)
        self.data["ids"] = ""
        token, user = create_activity_admin_user("user_admin")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_not_all_in(self):
        self.init_user(50)
        users = User.objects.all().values_list("id", flat=True)
        User.objects.all().update(activity_level=2)
        self.data["ids"] = "-".join([str(i) for i in users])
        token, user = create_activity_admin_user("user_admin")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_permission(self):
        token, user = create_meetings_sponsor_user()
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_permission_2(self):
        token, _, user = create_user()
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)


class SponsorDelViewTest(TestCommon):
    url = "/sponsor/action/del/"
    data = {
        "ids": "1-2"
    }

    def test_ok(self):
        self.init_user(50)
        users = User.objects.all().values_list("id", flat=True)
        self.data["ids"] = "-".join([str(i) for i in users])
        token, user = create_activity_admin_user("user_admin", "user_admin")
        c = self.get_client(user, token)
        c.post(SponsorAddViewTest.url, data=self.data)
        token, user = create_activity_admin_user("user_admin1", "user_admin1")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_200_OK)

    def test_over_count(self):
        self.init_user(60)
        users = User.objects.all().values_list("id", flat=True)
        self.data["ids"] = "-".join([str(i) for i in users])
        token, user = create_activity_admin_user("user_admin")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lt_zero(self):
        self.init_user(1)
        self.data["ids"] = ""
        token, user = create_activity_admin_user("user_admin")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_not_all_in(self):
        self.init_user(50)
        User.objects.all().values_list("id", flat=True)
        User.objects.all().update(activity_level=2)
        self.data["ids"] = "1-10000"
        token, user = create_activity_admin_user("user_admin")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_permission(self):
        token, user = create_meetings_sponsor_user()
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_permission_2(self):
        token, _, user = create_user()
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)


class MeetingsViewTest(TestCommon):
    url = "/meetings/"
    data = {
        "topic": "*" * 128,  # string类型，会议名称，必填，长度限制128，限制内容中含有http，\r\n, xss攻击标签
        "platform": "zoom",  # string类型，平台，只能是以下参数: zoom,welink,tencent， 必填
        "sponsor": "T" * 20,  # string类型，会议发起人，必填，长度限制20，限制内容中含有http，\r\n, xss攻击标签

        "group_name": "*" * 40,  # string类型，sig 组名称，必填， 限制40
        "group_id": 1,  # int类型，sig组id, 必填
        "date": "2023-11-20",  # string类型，时间：2023-10-29，必填
        "start": "08:00",  # string类型，开始时间，必填
        "end": "09:00",  # string类型，结束时间，必填
        "etherpad": "https://etherpad.openeuler.org/p/A-Tune-meetingsdafssdfadsfasdfa",
        # string类型，以 https://etherpad.openeuler.org开头，必填，限制64
        "agenda": "*" * 4096,  # string类型，开会内容，必填，内容可以为空， 限制为4096，限制内容中含有http，\r\n, xss攻击标签
        "emaillist": ";".join(["{}@163.com".format("a" * 42) for _ in range(20)]),
        # string类型, 发送邮件，以;拼接，长度最长为1000，每封邮箱长度最长为50，限制20封，必填，内容可以为空
        "record": "cloud"  # string类型，是否自动录制，必填，可为空字符串，空字符串代表非自动录制，必填，内容可以为空
    }

    def test_ok(self):
        self.data["topic"] = "k" * 128
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_200_OK)

    def test_topic(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["topic"] = "*" * 129
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_topic_1(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["topic"] = ""
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_platform(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["platform"] = "sadfdsfadsfadsfasd"
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_group_name(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["group_name"] = ""
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_group_id(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["group_id"] = "xxxxxx"
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_date(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["date"] = "xxxxxx"
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_date_1(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["date"] = "2025-11-02"
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_start(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["start"] = "08:13"
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_start_1(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["start"] = "xxx:13"
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_end(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["end"] = "08:13"
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_end_1(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["end"] = "xxx:13"
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_etherpad(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["etherpad"] = "*" * 65
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_agenda(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["agenda"] = "*" * 4097
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_agenda_2(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["agenda"] = xss_script
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_agenda_4(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["agenda"] = html_text
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email_list(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["emaillist"] = ";".join(["{}@163.com".format("a" * 42) for _ in range(51)])
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email_list_1(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["emaillist"] = ";".join(["{}163.com".format("a" * 42) for _ in range(10)])
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email_list_2(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["emaillist"] = "sdajkfljlkdsjfk;asd@qq.com"
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_record(self):
        token, user, data = self.init_meetings(self.data)
        c = self.get_client(user, token)
        data["record"] = "cloudafdslfajsdlfjds"
        ret = c.post(self.url, data=data)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_permission(self):
        token, user = create_meeting_admin_user()
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_permission_2(self):
        token, _, user = create_user()
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_permission_3(self):
        token, user = create_activity_sponsor_user()
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_permission_4(self):
        token, user = create_activity_admin_user()
        c = self.get_client(user, token)
        ret = c.post(self.url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)


class MeetingDelViewTest(TestCommon):
    url = "/meeting/{}/"

    def test_ok(self):
        token, user, data = self.init_meetings(MeetingsViewTest.data)
        c = self.get_client(user, token)
        c.post(MeetingsViewTest.url, data=data)
        token, user = get_user("sponsor")
        m = Meeting.objects.first()
        c = self.get_client(user, token)
        url = self.url.format(m.mid)
        print(url)
        ret = c.delete(url)
        print(ret.__dict__)
        self.assertEqual(ret.status_code, status.HTTP_200_OK)

    def test_not_delete_by_others(self):
        token, user, data = self.init_meetings(MeetingsViewTest.data)
        c = self.get_client(user, token)
        c.post(MeetingsViewTest.url, data=data)
        m = Meeting.objects.first()
        url = self.url.format(m.mid)
        token, user = create_meetings_sponsor_user("xxxxxxx", "xxxxxxx")
        c = self.get_client(user, token)
        ret = c.delete(url)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_permission_1(self):
        url = self.url.format(1)
        token, _, user = create_user()
        c = self.get_client(user, token)
        ret = c.delete(url)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_permission_2(self):
        url = self.url.format(1)
        token, user = create_activity_sponsor_user()
        c = self.get_client(user, token)
        ret = c.delete(url)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_permission_3(self):
        url = self.url.format(1)
        token, user = create_activity_admin_user()
        c = self.get_client(user, token)
        ret = c.delete(url)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)


class ActivityViewTest(TestCommon):
    url = "/activity/"
    data = {
        "title": "1" * 50,  # 活动主题，string类型，限制长度1-50
        "date": "2023-11-20",  # 日期，大于今天
        "activity_type": 1,  # 活动类型，1为线下活动，2为线上活动
        "register_url": "https://space.bilibili.com/527064077",  # 报名链接，url链接检查
        "synopsis": "*" * 4096,  # 活动简介，xss攻击检查，crlf攻击检查,限制长度4096
        "address": "*" * 100,  # 线下活动才有此字段
        "detail_address": "东城区灯市口利生大厦写字楼(锡拉胡同)",  # 线下活动才有此字段，详细地址, xss攻击检查，crlf攻击检查，限制长度100
        "longitude": "",  # 线下活动才有此字段，经度, xss攻击检查，crlf攻击检查，限制长度8位
        "latitude": "",  # 线下活动才有此字段，维度, xss攻击检查，crlf攻击检查，限制长度8位
        "start": "08:00",  # 线上活动才有此字段，开始时间
        "end": "09:00",  # 线上活动才有此字段，结束时间
        "poster": 1,  # 海报，目前只有1,2,3,4
        "schedules": [{"start": "08:00", "end": "09:00", "topic": "活动xxxxxxx",
                       "speakerList": [{"name": "活动1", "title": "工程师1"}, {"name": "活动2", "title": "工程师2"}]},
                      {"start": "08:00", "end": "09:00", "topic": "活动yyyyyyyyyy",
                       "speakerList": [{"name": "活动1", "title": "工程师1"}, {"name": "活动2", "title": "工程师2"}]}],
    }

    def init_activity_data(self, is_online=True):
        temp = copy.deepcopy(self.data)
        if is_online:
            temp["activity_type"] = 2
            del temp["address"]
            del temp["detail_address"]
            del temp["longitude"]
            del temp["latitude"]
        else:
            temp["activity_type"] = 1
            del temp["start"]
            del temp["end"]
        return temp

    def test_ok(self):
        data = self.init_activity_data()
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_200_OK)

    def test_invalid_title(self):
        data = self.init_activity_data()
        del data["title"]
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_title_1(self):
        data = self.init_activity_data()
        data["title"] = "a" * 51
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_title_2(self):
        data = self.init_activity_data()
        data["title"] = html_text
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_title_3(self):
        data = self.init_activity_data()
        data["title"] = xss_script
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_date(self):
        data = self.init_activity_data()
        data["date"] = "2306-11-19"
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_date_1(self):
        data = self.init_activity_data()
        data["date"] = "dsfafdsfadsfasd"
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_activity_type(self):
        data = self.init_activity_data()
        data["activity_type"] = 3
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_register_url(self):
        data = self.init_activity_data()
        data["register_url"] = "dsfadsfasdfasdfadsfa"
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_synopsis(self):
        data = self.init_activity_data()
        data["synopsis"] = "*" * 4097
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_address(self):
        data = self.init_activity_data(is_online=False)
        data["address"] = "*" * 101
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_detail_address(self):
        data = self.init_activity_data(is_online=False)
        data["detail_address"] = "*" * 101
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_longitude(self):
        data = self.init_activity_data(is_online=False)
        data["longitude"] = "*" * 101
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_longitude_1(self):
        data = self.init_activity_data(is_online=False)
        data["longitude"] = "312312312.312312312312"
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_latitude(self):
        data = self.init_activity_data(is_online=False)
        data["latitude"] = "*" * 101
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_start(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        data["latitude"] = "*" * 101
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_start_1(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        data["start"] = "08:13"
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_start_2(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        data["start"] = "xxx:13"
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_end_1(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        data["end"] = "08:13"
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_end_2(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        data["end"] = "xxx:13"
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_poster(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        data["poster"] = "5"
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_schedules(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        data["schedules"] = "*" * 8193
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_schedules_1(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        data["schedules"] = [{  # 限制长度8192
            "start": "08:00",  # 开始时间, 时间限制08:00 -> 23:59
            "end": "09:00",  # 结束时间, 时间限制08:00 -> 23:59
            "topic": "活动1",  # 活动子主题, xss攻击检查，crlf攻击检查
            "speakerList": [{
                "name": xss_script,  # 嘉宾名称,xss攻击检查，crlf攻击检查
                "title": "工程师"  # 嘉宾职称,xss攻击检查，crlf攻击检查
            }]
        }],
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_schedules_2(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        data["schedules"] = [{  # 限制长度8192
            "start": "08:00",  # 开始时间, 时间限制08:00 -> 23:59
            "end": "09:00",  # 结束时间, 时间限制08:00 -> 23:59
            "topic": "活动1",  # 活动子主题, xss攻击检查，crlf攻击检查
            "speakerList": [{
                "name": html_text,  # 嘉宾名称,xss攻击检查，crlf攻击检查
                "title": "工程师"  # 嘉宾职称,xss攻击检查，crlf攻击检查
            }]
        }],
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_schedules_3(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        data["schedules"] = [{  # 限制长度8192
            "start": "08:00",  # 开始时间, 时间限制08:00 -> 23:59
            "end": "09:00",  # 结束时间, 时间限制08:00 -> 23:59
            "topic": "活动1",  # 活动子主题, xss攻击检查，crlf攻击检查
            "speakerList": [{
                "name": crlf_text,  # 嘉宾名称,xss攻击检查，crlf攻击检查
                "title": "工程师"  # 嘉宾职称,xss攻击检查，crlf攻击检查
            }]
        }]
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_schedules_4(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        data["schedules"] = [{  # 限制长度8192
            "start": "08:00",  # 开始时间, 时间限制08:00 -> 23:59
            "end": "09:00",  # 结束时间, 时间限制08:00 -> 23:59
            "topic": "活动1",  # 活动子主题, xss攻击检查，crlf攻击检查
            "speakerList": [{
                "name": "name",  # 嘉宾名称,xss攻击检查，crlf攻击检查
                "title": xss_script  # 嘉宾职称,xss攻击检查，crlf攻击检查
            }]
        }]
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_schedules_5(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        data["schedules"] = [{  # 限制长度8192
            "start": "08:00",  # 开始时间, 时间限制08:00 -> 23:59
            "end": "09:00",  # 结束时间, 时间限制08:00 -> 23:59
            "topic": "活动1",  # 活动子主题, xss攻击检查，crlf攻击检查
            "speakerList": [{
                "name": "name",  # 嘉宾名称,xss攻击检查，crlf攻击检查
                "title": html_text  # 嘉宾职称,xss攻击检查，crlf攻击检查
            }]
        }]
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_schedules_6(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        data["schedules"] = [{  # 限制长度8192
            "start": "08:00",  # 开始时间, 时间限制08:00 -> 23:59
            "end": "09:00",  # 结束时间, 时间限制08:00 -> 23:59
            "topic": "活动1",  # 活动子主题, xss攻击检查，crlf攻击检查
            "speakerList": [{
                "name": "name",  # 嘉宾名称,xss攻击检查，crlf攻击检查
                "title": crlf_text  # 嘉宾职称,xss攻击检查，crlf攻击检查
            }]
        }]
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_schedules_7(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        data["schedules"] = [{  # 限制长度8192
            "start": "08:00",  # 开始时间, 时间限制08:00 -> 23:59
            "end": "09:00",  # 结束时间, 时间限制08:00 -> 23:59
            "topic": crlf_text,  # 活动子主题, xss攻击检查，crlf攻击检查
            "speakerList": [{
                "name": "name",  # 嘉宾名称,xss攻击检查，crlf攻击检查
                "title": "title"  # 嘉宾职称,xss攻击检查，crlf攻击检查
            }]
        }]
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_schedules_8(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        data["schedules"] = [{  # 限制长度8192
            "start": "08:00",  # 开始时间, 时间限制08:00 -> 23:59
            "end": "09:00",  # 结束时间, 时间限制08:00 -> 23:59
            "topic": html_text,  # 活动子主题, xss攻击检查，crlf攻击检查
            "speakerList": [{
                "name": "name",  # 嘉宾名称,xss攻击检查，crlf攻击检查
                "title": "title"  # 嘉宾职称,xss攻击检查，crlf攻击检查
            }]
        }]
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_schedules_9(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        data["schedules"] = [{  # 限制长度8192
            "start": "08:00",  # 开始时间, 时间限制08:00 -> 23:59
            "end": "09:00",  # 结束时间, 时间限制08:00 -> 23:59
            "topic": xss_script,  # 活动子主题, xss攻击检查，crlf攻击检查
            "speakerList": [{
                "name": "name",  # 嘉宾名称,xss攻击检查，crlf攻击检查
                "title": "title"  # 嘉宾职称,xss攻击检查，crlf攻击检查
            }]
        }]
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_schedules_10(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        data["schedules"] = [{  # 限制长度8192
            "start": "08:01",  # 开始时间, 时间限制08:00 -> 23:59
            "end": "09:00",  # 结束时间, 时间限制08:00 -> 23:59
            "topic": "topic",  # 活动子主题, xss攻击检查，crlf攻击检查
            "speakerList": [{
                "name": "name",  # 嘉宾名称,xss攻击检查，crlf攻击检查
                "title": "title"  # 嘉宾职称,xss攻击检查，crlf攻击检查
            }]
        }]
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_schedules_11(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        data["schedules"] = [{  # 限制长度8192
            "start": "07:00",  # 开始时间, 时间限制08:00 -> 23:59
            "end": "09:00",  # 结束时间, 时间限制08:00 -> 23:59
            "topic": "topic",  # 活动子主题, xss攻击检查，crlf攻击检查
            "speakerList": [{
                "name": "name",  # 嘉宾名称,xss攻击检查，crlf攻击检查
                "title": "title"  # 嘉宾职称,xss攻击检查，crlf攻击检查
            }]
        }]
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_schedules_12(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        data["schedules"] = [{  # 限制长度8192
            "start": "07:00",  # 开始时间, 时间限制08:00 -> 23:59
            "end": "23:00",  # 结束时间, 时间限制08:00 -> 23:59
            "topic": "topic",  # 活动子主题, xss攻击检查，crlf攻击检查
            "speakerList": [{
                "name": "name",  # 嘉宾名称,xss攻击检查，crlf攻击检查
                "title": "title"  # 嘉宾职称,xss攻击检查，crlf攻击检查
            }]
        }]
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_schedules_13(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        data["schedules"] = [{  # 限制长度8192
            "start": "07:00",  # 开始时间, 时间限制08:00 -> 23:59
            "end": "20:60",  # 结束时间, 时间限制08:00 -> 23:59
            "topic": "topic",  # 活动子主题, xss攻击检查，crlf攻击检查
            "speakerList": [{
                "name": "name",  # 嘉宾名称,xss攻击检查，crlf攻击检查
                "title": "title"  # 嘉宾职称,xss攻击检查，crlf攻击检查
            }]
        }]
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_permission(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_activity_admin_user()
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_permission_1(self):
        data = self.init_activity_data(is_online=False)
        token, _, user = create_user()
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_permission_2(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_meeting_admin_user()
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_permission_3(self):
        data = self.init_activity_data(is_online=False)
        token, user = create_meetings_sponsor_user()
        c = self.get_client(user, token)
        ret = c.post(self.url, data=data, format='json')
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)


class ActivityPublishViewTest(TestCommon):
    url = "/activitypublish/{}/"

    def test_ok(self):
        data = ActivityViewTest().init_activity_data()
        token, user = create_activity_sponsor_user("sponsor", "sponsor")
        c = self.get_client(user, token)
        c.post(ActivityViewTest.url, data=data, format='json')
        token, user = create_activity_admin_user("sponsor1", "sponsor1")
        c = self.get_client(user, token)
        activity = Activity.objects.first()
        url = self.url.format(activity.id)
        ret = c.put(url)
        self.assertEqual(ret.status_code, status.HTTP_200_OK)

    def test_not_exist(self):
        token, user = create_activity_admin_user("sponsor", "sponsor_openid")
        url = self.url.format("20000")
        c = self.get_client(user, token)
        ret = c.put(url)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_permission(self):
        token, _, user = create_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        url = self.url.format("20000")
        ret = c.put(url)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_permission_1(self):
        token, user = create_meetings_sponsor_user("sponsor", "sponsor_openid")
        url = self.url.format("20000")
        c = self.get_client(user, token)
        ret = c.put(url)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_permission_2(self):
        token, user = create_meeting_admin_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        url = self.url.format("20000")
        ret = c.put(url)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_permission_3(self):
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        url = self.url.format("20000")
        ret = c.put(url)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)


class ActivityRejectViewTest(TestCommon):
    url = "/activityreject/{}/"

    def test_ok(self):
        data = ActivityViewTest().init_activity_data()
        token, user = create_activity_sponsor_user("sponsor", "sponsor")
        c = self.get_client(user, token)
        c.post(ActivityViewTest.url, data=data, format='json')
        token, user = create_activity_admin_user("sponsor1", "sponsor1")
        activity = Activity.objects.first()
        url = self.url.format(activity.id)
        c = self.get_client(user, token)
        ret = c.put(url)
        self.assertEqual(ret.status_code, status.HTTP_200_OK)

    def test_not_exist(self):
        token, user = create_activity_admin_user("sponsor", "sponsor_openid")
        url = self.url.format("20000")
        c = self.get_client(user, token)
        ret = c.put(url)
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_permission(self):
        token, _, user = create_user("sponsor", "sponsor_openid")
        url = self.url.format("20000")
        c = self.get_client(user, token)
        ret = c.put(url)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_permission_1(self):
        token, user = create_meetings_sponsor_user("sponsor", "sponsor_openid")
        url = self.url.format("20000")
        c = self.get_client(user, token)
        ret = c.put(url)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_permission_2(self):
        token, user = create_meeting_admin_user("sponsor", "sponsor_openid")
        url = self.url.format("20000")
        c = self.get_client(user, token)
        ret = c.put(url)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_permission_3(self):
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        url = self.url.format("20000")
        c = self.get_client(user, token)
        ret = c.put(url)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)


class ActivityDelViewTest(TestCommon):
    url = "/activitydel/{}/"

    def test_ok(self):
        data = ActivityViewTest().init_activity_data()
        print(data)
        token, user = create_activity_sponsor_user("sponsor", "sponsor")
        c = self.get_client(user, token)
        c.post(ActivityViewTest.url, data=data, format='json')
        token, user = create_activity_admin_user("sponsor_admin", "sponsor_admin")
        activity = Activity.objects.first()
        url = ActivityPublishViewTest.url.format(activity.id)
        c = self.get_client(user, token)
        ret = c.put(url)
        self.assertEqual(ret.status_code, status.HTTP_200_OK)
        token, user = get_user("sponsor_admin")
        url = self.url.format(activity.id)
        c = self.get_client(user, token)
        ret = c.put(url)
        self.assertEqual(ret.status_code, status.HTTP_200_OK)

    def test_not_permission(self):
        token, _, user = create_user("test_not_permission", "test_not_permission")
        url = self.url.format("20000")
        c = self.get_client(user, token)
        ret = c.put(url)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_permission_1(self):
        token, user = create_meetings_sponsor_user("sponsor", "sponsor_openid")
        url = self.url.format("20000")
        c = self.get_client(user, token)
        ret = c.put(url)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_permission_2(self):
        token, user = create_meeting_admin_user("sponsor", "sponsor_openid")
        url = self.url.format("20000")
        c = self.get_client(user, token)
        ret = c.put(url)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_permission_3(self):
        token, user = create_activity_sponsor_user("sponsor", "sponsor_openid")
        url = self.url.format("20000")
        c = self.get_client(user, token)
        ret = c.put(url)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)


class ActivityUpdateViewTest(TestCommon):
    url = "/activityupdate/{}/"
    data = {
        "schedules": json.dumps(
            [{
                "start": "08:00",  # 开始时间, 时间限制08:00 -> 23:59
                "end": "09:00",  # 结束时间, 时间限制08:00 -> 23:59
                "topic": "xxjflasdfads",  # 活动子主题, xss攻击检查，crlf攻击检查
                "speakerList": [{
                    "name": "name",  # 嘉宾名称,xss攻击检查，crlf攻击检查
                    "title": "title"  # 嘉宾职称,xss攻击检查，crlf攻击检查
                }]
            }]
        )
    }

    def test_ok(self):
        data = ActivityViewTest().init_activity_data()
        token, user = create_activity_sponsor_user("sponsor", "sponsor")
        c = self.get_client(user, token)
        c.post(ActivityViewTest.url, data=data, format='json')
        token, user = create_activity_admin_user("sponsor1", "sponsor1")
        c = self.get_client(user, token)
        activity = Activity.objects.first()
        url = ActivityPublishViewTest.url.format(activity.id)
        c.put(url)
        token, user = get_user("sponsor")
        c = self.get_client(user, token)
        url = self.url.format(activity.id)
        ret = c.put(url, data=self.data, format="json")
        self.assertEqual(ret.status_code, status.HTTP_200_OK)

    def test_not_exist(self):
        data = ActivityViewTest().init_activity_data()
        token, user = create_activity_sponsor_user("sponsor", "sponsor")
        c = self.get_client(user, token)
        c.post(ActivityViewTest.url, data=data,format= "json")
        token, user = create_activity_admin_user("sponsor1", "sponsor1")
        c = self.get_client(user, token)
        activity = Activity.objects.first()
        url = ActivityPublishViewTest.url.format(activity.id)
        c.put(url)
        token, user = get_user("sponsor")
        c = self.get_client(user, token)
        url = self.url.format("11111")
        ret = c.put(url, data=self.data, format="json")
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_permission(self):
        token, _, user = create_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        url = self.url.format("20000")
        ret = c.put(url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_permission_1(self):
        token, user = create_meetings_sponsor_user("sponsor", "sponsor_openid")
        c = self.get_client(user, token)
        url = self.url.format("20000")
        ret = c.put(url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_permission_2(self):
        token, user = create_meeting_admin_user("sponsor", "sponsor_openid")
        url = self.url.format("20000")
        c = self.get_client(user, token)
        ret = c.put(url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_permission_3(self):
        token, user = create_activity_admin_user("sponsor", "sponsor_openid")
        url = self.url.format("20000")
        c = self.get_client(user, token)
        ret = c.put(url, data=self.data)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

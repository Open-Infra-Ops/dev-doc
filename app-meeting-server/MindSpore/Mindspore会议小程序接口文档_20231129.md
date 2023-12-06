# 会议小程序接口文档

## 一.用户模块

### 1.用户登录

请求地址：/login/

请求方法：post请求

请求参数：

~~~json
{
    "code": "xxxxxxxxxxxxxxxx"   # string, 微信授权后响应的code
}
~~~

返回参数：

~~~json
{
    "user_id": 1,                 # int, 用户的id
    "access": "",                 # string, 用户登录后的token
    "refresh":  "",               # string，用户的刷新token
    "level": 3,					  # int, 会议活动权限
    "activity_level": 3,          # int, 活动会议权限
    "gitee_name": null,           # string, 码云的gitee_id
    "nickname": "USER_64e02c77",  # string, 微信名称
    "avatar": "https://www.bai",  # string, 头像链接   
    "agree_privacy_policy": true  # bool, 是否赞成隐私声明
}
~~~

### 2.用户刷新token

请求地址：/refresh/

请求方法：post请求

请求参数：

+ json请求体

  ~~~json
  {
      "refresh": "",  # string类型
  }
  ~~~

返回参数：

~~~bash
{
	"access":"",         # string, 用户登录后的token
	"refresh":"",        # string, 用户登录后的refresh
}
~~~

### 3.用户登出

请求地址：/logout/

请求方法：post请求

请求参数：无

返回参数：

```json
{
    "code": 200,
    "msg": "User logged out",
    "data": None
}
```

### 4.用户注销

请求地址：/logoff/

请求方法：post请求

请求参数：无

返回参数：

~~~json
{
    "code": 200,
    "msg": "User logged off",
    "data": None
}
~~~

### 5.同意更新隐私声明

请求地址：/agree/

请求方法：put请求

请求参数：无

返回参数：

~~~json
{
    "code": 200,
    "msg": "Agree to privacy statement",
    "data": None
    "access": ""
}
~~~

### 6.撤销同意更新隐私政策

请求地址： /revoke/

请求方法：post请求

请求参数：无

返回参数：

~~~json
{
    "code": 200,
    "msg": "Revoke agreement of privacy policy",
    "data": None
}
~~~

### 7.修改用户的gitee_name

请求地址：/user/<int:pk>/

请求方法：put请求

请求参数：

- 路径参数：

  ```json
  pk: # int类型 用户的id
  ```

- 请求体: json格式

  ```json
  {
      "gitee_name"： "xxxxx"
  }
  ```

返回参数：

```json
{
    "id": 3,
    "gitee_name": "xxx",
    "access": ""
}
```

### 8.用户的详情信息

请求地址：/userinfo/<int:pk>/

请求方法：get请求

请求参数：

- 路径参数

  ```json
  pk: # int类型，用户id
  ```

返回参数：

```json
{
    "code": 200,
    "msg": "success",
    "data": None
}
```

### 9.查询不在该sig组的用户（分页查询）

请求地址： /users_exclude/<int:pk>/?page=1&size=10&search=nickname

请求方法：get请求

请求参数:

- 路径参数

  ```json
  pk:   int类型, sig组的id
  ```

- 查询参数

  ```json
  page: int类型，第几页，
  size: int类型，每页的大小
  search: 模糊查询，查询nickname
  ```

返回参数:

```json
{
	"total": 50,
	"page": 1,
	"size": 10,
	"data": [{
				"id": 1,   	 				  # int,用户的id 
		  		"nickname": "USER_ac94a464",  # string， 微信获取的头像 
		  		"gitee_name": null,           # string, 码云的gitee_id 
		  		"avatar": "https:xxx.com"     # 头像
			},
			{
				"id": 2,
				"nickname": "USER_b1fc968b",
				"gitee_name": "xxxxx",
				"avatar": "https:xxx.com"
			},
			{
				"id": 3,
				"nickname": "USER_b62429ac",
				"gitee_name": null,
				"avatar": "https:xxx.com"
			}
	]
}
```

### 10.查询在该sig组的用户（分页查询）

请求地址：/users_include/<int:pk>/?page=1&size=10&search=nickname

请求方法：get请求

请求参数:

- 路径参数

  ```json
  pk:   int类型, sig组的id, 路径参数
  ```

- 查询参数：

  ```json
  page: int类型，第几页，
  size: int类型，每页的大小
  search: nickname
  ```

返回参数：

```json
{
	"total": 50,
	"page": 1,
	"size": 10,
	"data": [{
				"id": 1,
				"nickname": "USER_ac94a464",
				"gitee_name": null,
				"avatar": "https://xxxx.com"
			},
			{
				"id": 2,
				"nickname": "USER_b1fc968b",
				"gitee_name": "null",
				"avatar": "https://xxxx.com"
			},
			{
				"id": 3,
				"nickname": "USER_b62429ac",
				"gitee_name": null,
				"avatar": "https://xxxx.com"
			}]
}
```

### 11.查询所有sig组的名称（msg,pro）

请求地址：/groups/

请求方法：get请求

请求参数：无

返回参数：

~~~json
[
    	{
			"id": 1,   		# int类型， group的id 
	  		"name": "xxx"   # string类型， group的name
		},
		{
			"id": 110,
			"name": "xxxxx"
		}
 ]
~~~

### 12.查询所有sig组的名称（SIG）

请求地址：/sigs/

请求方法：get请求

请求参数：无

返回参数：

~~~json
[
    {
        "id": 1,
        "name": "xxxxx",
    },
]
~~~

### 13.查看用户所在组的信息

请求地址：/usergroup/<int:pk>/

请求方法：get请求

请求参数：

- 路径参数

  ```json
  pk: int类型，用户的id
  ```

返回参数：

```json
{
    "group":"xxx", 
    "group_name":"xxxx", 
    "group_type":"xxxx", 
    "etherpad":"xxxxxxx", 
    "description:"https://xxxxxx.com"
}
```

### 14.sig组批量新增用户

请求地址：/groupuser/action/new/

请求方法：post请求

请求参数：

+ 请求体： json格式

  ~~~json
  {
      "ids": "1-2-3-4"       # string类型，
      "group_id"： 1         # int类型，sig组的id, 
  }
  ~~~

返回参数:

~~~json
{
    "code": 200,
    "msg": "Success to add maintainers to the group",
    "access": ""
}
~~~

### 15.sig组批量删除用户

请求地址：/groupuser/action/del/

请求方法：post请求

请求参数：

+ 请求体：json格式

  ~~~json
  {
      "ids": "1-2-3-4"       # string类型
      "group_id"： 1         # int类型，sig组的id, 
  }
  ~~~

返回参数:

~~~json
{
    "code": 200,
    "msg": "successfully deleted",
    "access": ""
}
~~~

### 16.在城市组城市列表

请求地址：/users_include_city/?page=10&size=10&search=nickname

请求方法：get请求

请求参数：

- 查询参数

  ```json
  page: 第几页
  size: 每页大小
  search: nickname
  ```

返回参数:

```json
{
    "code": 200,
    "msg": "success",
    "data": [
        {
            "id": 1,
            "nickname": "USER_dajlfsjdks",
            "gitee_name": "xxx",
            "avatar": "https://xxxxx.com"
        }
    ]
}
```

### 17.不在城市组城市列表

请求地址：/users_exclude_city/?page=10&size=10&search=nickname

请求方法：get请求

请求参数：

- 查询参数

  ```json
  page: 第几页
  size: 每页大小
  search: nickname
  ```

返回参数:

```json
{
    "code": 200,
    "msg": "success",
    "data": [
        {
            "id": 1,
            "nickname": "USER_dajlfsjdks",
            "gitee_name": "xxx",
            "avatar": "https://xxxxx.com"
        }
    ]
}
```

### 18.活动发起人（分页查询）

请求地址：/sponsors/?page=1&size=10&search=nickname

请求方法：get请求

请求参数：无

+ 查询参数

  ~~~jsono
  page: int类型，第几页
  size: int类型，每页的大小
  search: nickname，模糊查询
  ~~~

返回参数：

```json
{
	"total": 50,
	"page": 1,
	"size": 10,
	"data": [{
			"id": 2,
			"nickname": "USER_b1fc968b",
			"avatar": "https://xxxxx.com",
			"gitee_name": "xxxxx"
		},
		{
			"id": 3,
			"nickname": "USER_b62429ac",
			"avatar": "https://xxxxx.com",
			"gitee_name": null
		}
	]
}
```

### 19.非活动发起人(分页查询)

请求地址：/nonsponsors/?page=1&size=10&search=nickname

请求方法：get请求

请求参数：

+ 查询参数

  ~~~json
  page: int类型，第几页
  size: int类型，每页的大小
  search: 模糊查询，nickname
  ~~~

返回参数：

```json
{
	"total": 50,
	"page": 1,
	"size": 10,
	"data": [{
			"id": 2,
			"nickname": "USER_b1fc968b",
			"avatar": "https://xxxxx.com",
			"gitee_name": "xxxx"
		},
		{
			"id": 3,
			"nickname": "USER_b62429ac",
			"avatar": "https://xxxxx.com",
			"gitee_name": null
		}
	]
}
```

### 20.批量添加活动发起人

请求地址：/sponsor/action/new/

请求方法：post请求

请求参数：

+ 请求体： json格式

  ~~~json
  {
      "ids": "1-2-3-4"       # string类型，
  }
  ~~~

返回参数:

```json
{
    "code": 200,
    "msg": "Added successfully",
    "access": ""
}
```

### 21.批量删除活动发起人

请求地址：/sponsor/action/del/

请求方法：post请求

请求参数：

+ 请求体： json格式

  ~~~json
  {
      "ids": "1-2-3-4"       # string类型
  }
  ~~~

返回参数:

```json
{
    "code": 200,
    "msg": "successfully deleted",
    "access": ""
}
```

### 22.查看我的各类计数

请求地址：/mycounts/

请求方法：get请求

请求参数：无

返回参数：

```json
{
    "collected_meetings_count":"xxx", 
    "collected_activities_count":"xxxx", 
    "created_meetings_count":"xxxx", 
    "published_activities_count:"xxxx",
    "drafts_count:"xxxx",
    "publishing_activities_count:"xxxx",
}
```

### 23.城市列表

请求地址：/cities/

请求方法： get请求

请求参数：无

返回参数：

~~~json
[{
    "id":1,
    "name":"xxxx",
    "etherpad":"https://xxxx.com",
}]
~~~

### 24.添加城市

请求地址：/city/

请求方法：post请求

请求参数：

+ 请求体: json格式

  ~~~json
  {
      "name": "xxxx";
  }
  ~~~

返回参数：

~~~json
{
    "code": 200,
    "msg": "success",
    "msg": "success",
}
~~~

### 25.批量新增城市组成员

请求地址：/cityuser/action/new/

请求方法： post请求

请求参数： 

+ 请求体: json格式

  ~~~json
  {
      "ids": "1-2-3-4"       # string类型，
      "city_id"： 1         # int类型，sig组的id, 
  }
  ~~~

返回参数：

~~~json
{
    "code": 200,
    "msg": "success",
    "access": ""
}
~~~



### 26.批量删除城市组成员

请求地址：/cityuser/action/del/

请求方法： post请求

请求参数： 

- 请求体: json格式

  ```json
  {
      "ids": "1-2-3-4"      # string类型，
      "city_id"： 1         # int类型，sig组的id, 
  }
  ```

返回参数：

```json
{
    "code": 200,
    "msg": "success",
    "access": ""
}
```

### 27.查看用户的城市组关系

请求地址：/usercity/<int:pk>/

请求方法： post请求

请求参数： 

- 请求体: json格式

  ```json
  {
      "ids": "1-2-3-4"       # string类型
      "city_id"： 1         # int类型，sig组的id, 
  }
  ```

返回参数：

```json
[
    "city": 1,
    "city_name": "xxx",
    "etherpad": "https://xxxxx.com",
]
```

## 二.会议模块

### 1.创建会议

请求地址：/meetings/

请求方法：post请求

请求参数：

+ 请求体: json格式

  ~~~json
  {
      "topic": "xxx",         # string类型，会议名称
      "platform": "zoom",     # string类型，平台，
      "sponsor": "xxxxx",     # string类型，会议发起人，
      "group_name": "xxxx",   # string类型，sig 组名称，
      "date": "2023-11-02",   # string类型，
      "start": "08:00",       # string类型，开始时间，
      "end": "09:00",         # string类型，结束时间，
      "etherpad": "https://xxxxx.com",# string类型，
      "agenda": "会议内容",    # string类型，开会内容
      "emaillist": "xxxx@163.com;xxxxx@qq.com;", # string类型
      "record": "cloud"，     # string类型
      "meeting_type":         # int类型
      "city":                 # string类型，
  }
  ~~~

返回参数：

~~~json
{
    "code": 200,
    "message": "Created successfully",
    "access": "",
    "id": 4
}
~~~

### 2.删除单个会议

请求地址：/meeting/<int:mid>/

请求方法：delete请求

请求参数：

- 路径参数

  ```json
  mid: # int类型，会议的mid
  ```

返回参数：

```bash
{
	"code": 200,
	"message": "Delete successfully.",
	"access": ""
}
```

### 3.查询单个会议

请求地址：/meetings/<int:pk>/

请求方法：get请求

请求参数：

- 路径参数

  ```json
  pk: # int类型, meeting的id
  ```

返回参数：

```json
{
    "id": 1, 
    "collection_id": 1, 
    "user_id": 1, 
    "group_id": 1, 
    "topic": "topic", 
    "sponsor": "tom", 
    "group_name"： "xxxx", 
    "date": "2023-10-27", 
    "start":"4",         
    "end":"5", 
    "agenda": "xxxx", 
    "etherpad": "xxxx", 
    "mid": "xxxxx", 
    "join_url": "https://xxx.com", 
    "video_url": "https://xxxxx.com", 		 
    "mplatform": "xxxx"
}
```

### 4.会议列表

请求地址：/meetingslist/?page=10&size=10

请求方法：get请求

请求参数：

+ 查询参数

  ~~~json
  page: 第几页
  size: 每页的数量
  ~~~

返回参数：

~~~json
{
	"total": 50,
	"page": 1,
	"size": 10,
	"data": [
        {
            "id": 1, 
            "collection_id": 1, 
            "user_id": 1, 
            "group_id": 1, 
            "topic": "xxx", 
            "sponsor": "xxx", 
            "group_name"： "xxxx", 
            "date": "2023-10-27", 
            "start":"4",         
            "end":"5", 
            "city": "xxxx",
            "agenda": "xxxx", 
            "etherpad": "xxxx", 
            "mid": "xxxxx", 
            "mmid": "xxxxx", 
            "join_url": "https://xxxx.com", 
            "replay_url": "https://xxxx.com", 		 
            "mplatform": "tencent"
        }
	]
}
~~~

### 5.收藏会议

请求路径：/collect/

请求方式：post请求

请求参数：

- 请求体: json格式

  ```json
  {
      "meeting": 5, # int类型，会议的id
  }
  ```

返回参数：

```json
{
    "code":200, 
    "msg": "collect successfully", 
    "collection_id": collection_id, 
    "access": access
}
```

### 6.取消收藏会议

请求路径： /collect/<int:pk>/

请求方式： delete请求

请求参数：

- 路径参数

  ```json
  pk: int类型，collection_id
  ```

返回参数：

```json
{
    "code":200, 
    "msg": "collect successfully", 
    "access": access
}
```



### 7.查询我收藏的会议

请求路径： /collections/?page=1&size=10

请求方式:  get请求

请求参数：

- 查询参数

  ```json
  page: int类型，第几页
  size: int类型，每页的大小
  ```

返回参数：

```json
{
	"total": 50,
	"page": 1,
	"size": 10,
	"data": [
    {
        "id": 2,
        "collection_id": null,
        "user_id": 4,
        "group_id": 1,
        "topic": "xxx",
        "sponsor": "xxxxxxx",
        "group_name": "xxxxxxxx",
        "date": "2023-11-02",
        "start": "08:00",
        "end": "09:00",
        "agenda": "会议内容",
        "etherpad": "xxxxxxxx",
        "mid": "xxxxxx",
        "join_url": "https://xxxxxx.com",
        "video_url": "",
        "mplatform": "xxxxxxx"
    }
	]
}
```



### 8.查询我预定的会议

请求路径： /mymeetings/?page=1&size=10

请求方式:  get请求

请求参数：

- 查询参数

  ```json
  page: int类型，第几页
  size: int类型，每页的大小
  ```

返回参数：

```json
{
	"total": 50,
	"page": 1,
	"size": 10,
	"data": [
    {
        "id": 2,
        "collection_id": null,
        "user_id": 4,
        "group_id": 1,
        "topic": "xxx",
        "sponsor": "xxxxx",
        "group_name": "xxxxx",
        "date": "2023-11-02",
        "start": "08:00",
        "end": "09:00",
        "agenda": "会议内容",
        "etherpad": "https://xxxxxxx.com",
        "mid": "121232",
        "join_url": "https://xxxxx.com",
        "video_url": "",
        "mplatform": "zoom"
    }
	]
}
```

## 三.活动模块

### 1.创建活动并发布

请求路径：/activity/

请求方式： post请求

请求参数：

+ 查询参数

  ~~~json
  publish: true， true则发布，
  ~~~

- 请求体，json

  ```json
  {
  	"title": "线上",                      # 活动主题，string类型，
  	"start_date": "2023-11-03",          # 日期，开始时间
      "end_date": "2023-11-03",            # 日期，结束时间
      "activity_category": 1         		 # int类型
  	"activity_type": 2,            		 # int类型，活动类型
      "address": "北京市北京市xxx",          # 线下活动才有此字段
  	"detail_address": "东城区xxxxx",      # 详细地址
      "longitude": "",	 				 # 经度
  	"latitude": "",	  					 # 维度
  	"register_url": "https://xxx.com",   # 报名链接
      "online_url": "https://xxx.com",     # 线上链接
  	"synopsis": "线上活动",				  # 活动简介
  	"poster": 1,						 # 海报	
  	"schedules": [{	                     
  		"start": "08:00",   # 开始时间,
  		"end": "09:00",     # 结束时间, 
  		"topic": "活动1",    # 活动子主题,
  		"speakerList": [{
  			"name": "活动2",   #嘉宾名称
  			"title": "工程师"  #嘉宾职称
  		}]
  	}],
  }
  ```

返回参数：

```json
{
	"code": 200,
	"msg": "The event application was published successfully",
	"access": ""
}
```

### 2.修改某个活动

请求路径：/activityupdate/<int:pk>/

请求方式：put请求

请求参数：

- 路径参数

  ```json
  pK: int类型，活动的id
  ```

- 请求体，json

  ```json
  {
      "schedules": xxxx,
      "replay_url": "",
      "online_url": "",
  }
  ```

返回参数：

```json
{
    "code":200, 
    "msg": "success",
    "access": "xxxxxx",
}
```

### 3.查询审核列表(分页查询)

请求路径：/waitingactivities/?page=1&size=10

请求方式：get请求

请求参数：

+ 查询参数

  ~~~json
  page: int类型，第几页
  size: int类型，每页的大小
  ~~~

返回参数：

~~~json
{
	"total": 50,
	"page": 1,
	"size": 10,
	"data": [{
		"id": 1,
		"collection_id": null,
		"title": "线下活动测试",
		"start_date": "2023-11-03",
        "end_date": "2023-11-03",
		"activity_type": 1,
        "activity_category": 1,
        "register_method": 1,
        "register_url": "https://xxxxxx.com"
        "online_url": "https://xxxx.com"
		"synopsis": "",
		"address": "北京市北京市东城区xxxxxx",
		"detail_address": "东城区xxxxxxxx",
		"longitude": "xxxxx",
		"latitude": "xxxxxx",
		"schedules": "",
		"poster": 1,
		"status": 2,
		"user": 4,
		"replay_url": null,
	}, ]
}
~~~

### 4.查询待发布详情

请求路径：/waitingactivity/<int:pk>/

请求方式： get请求

请求参数：

+ 路径参数

  ~~~json
  pk： # int类型，发布活动的id
  ~~~

返回参数：

~~~json
{
		"id": 1,
		"collection_id": null,
		"title": "线下活动测试",
		"start_date": "2023-11-03",
        "end_date": "2023-11-03",
		"activity_type": 1,
        "activity_category": 1,
        "register_method": 1,
        "register_url": "https://xxxxxx.com"
        "online_url": "https://xxxx.com"
		"synopsis": "",
		"address": "北京市北京市东城区xxxxxx",
		"detail_address": "东城区xxxxxxxx",
		"longitude": "xxxxx",
		"latitude": "xxxx",
		"schedules": "",
		"poster": 1,
		"status": 2,
		"user": 4,
		"replay_url": null,
	}
~~~

### 5.发布活动申请通过

请求路径：/activity/action/approve/<int:pk>/

请求方式：put请求

请求参数：

+ 路径参数

  ~~~json
  pk: # int类型，活动的id
  ~~~

返回参数:

~~~json
{
	"code": 200,
	"msg": "The event has been reviewed and published",
	"access": ""
}
~~~

### 6.发布活动申请被驳回

请求路径： /activity/action/deny/<int:pk>/

请求方式：put请求

请求参数：

+ 路径参数

  ~~~json
  pk: # int类型，活动的id
  ~~~

返回参数：

~~~json
{
	"code": 200,
	"msg": "Event application has been rejected",
	"access": ""
}
~~~

### 7.下架活动

请求路径：/activity/action/del/<int:pk>/

请求方式: put请求

请求参数：

+ 路径参数

  ~~~json
  pk: int类型，活动的id
  ~~~

返回参数：

~~~jsoN
{
	"code": 204,
	"msg": "Activity deleted successfully",
	"access": ""
}
~~~

### 8.修改活动草案

请求路径：/draftupdate/<int:pk>/

请求方式：put请求

请求参数：

- 路径参数

  ```json
  pk: int类型，活动的id
  ```

- 请求体, json格式

  ```json
  {
  	"title": "线上",                      # 活动主题，string类型，
  	"start_date": "2023-11-03",          # 日期，开始时间
      "end_date": "2023-11-03",            # 日期，结束时间
      "activity_category": 1         		 # int类型
  	"activity_type": 2,            		 # int类型，活动类型
      "address": "北京市北京市xxx",          # 线下活动才有此字段
  	"detail_address": "东城区xxxxx",      # 详细地址
      "longitude": "",	 				 # 经度
  	"latitude": "",	  					 # 维度
  	"register_url": "https://xxx.com",   # 报名链接
      "online_url": "https://xxx.com",     # 线上链接
  	"synopsis": "线上活动",				  # 活动简介
  	"poster": 1,						 # 海报	
  	"schedules": [{	                     
  		"start": "08:00",   # 开始时间,
  		"end": "09:00",     # 结束时间, 
  		"topic": "活动1",    # 活动子主题,
  		"speakerList": [{
  			"name": "活动2",   #嘉宾名称
  			"title": "工程师"  #嘉宾职称
  		}]
  	}],
  }
  ```

返回参数：

```json
{
    "code": 200, 
    "msg": "Edit and save draft event", 
    "access": ""
}
```

### 9.查看单个活动草案

请求路径：/draft/<int:pk>/

请求方式： get请求

请求参数：

- 路径参数

  ```json
  pk: int类型，活动草案的id
  ```

返回参数：

```json
{
		"id": 1,
		"collection_id": null,
		"title": "线下活动测试",
		"start_date": "2023-11-03",
        "end_date": "2023-11-03",
		"activity_type": 1,
        "activity_category": 1,
        "register_method": 1,
        "register_url": "https://xxxxxx.com"
        "online_url": "https://xxxx.com"
		"synopsis": "",
		"address": "北京市北京市东城区xxxxxx",
		"detail_address": "东城区xxxxxxxx",
		"longitude": "xxxxxx",
		"latitude": "xxxxx",
		"schedules": "",
		"poster": 1,
		"status": 2,
		"user": 4,
		"replay_url": null,
}
```

### 10.删除单个活动草案

请求路径：/draft/<int:pk>/	

请求方式：delete请求

请求参数：

- 路径参数

  ```json
  pk: int类型，活动草案的id
  ```

返回参数：

```json
{
    "code":200,
    "msg": "success",
    "access": ""
}
```

### 11.查询活动列表(分页查询)

请求路径：/activities/?page=1&size=10

请求方式：get请求

请求参数：

- 查询参数

  ```json
  page: int类型，第几页
  size: int类型，每页的大小
  activity_status： registering/going/completed
  activity_category： 1,2,3,4
  ```

返回参数：

~~~json
{
	"total": 50,
	"page": 1,
	"size": 10,
	"data": [{
		"id": 1,
		"collection_id": null,
		"title": "线下活动测试",
		"start_date": "2023-11-03",
        "end_date": "2023-11-03",
		"activity_type": 1,
        "activity_category": 1,
        "register_method": 1,
        "register_url": "https://xxxxxx.com"
        "online_url": "https://xxxx.com"
		"synopsis": "",
		"address": "北京市北京市东城区xxxxxx",
		"detail_address": "东城区xxxxxxxx",
		"longitude": "xxxxxx",
		"latitude": "xxxxxx",
		"schedules": "",
		"poster": 1,
		"status": 2,
		"user": 4,
		"replay_url": null,
	}]
}
~~~

### 12.查询单个活动

请求路径：/activity/<int:pk>/

请求方式：get请求

请求参数：无

返回参数：

```json
{
		"id": 1,
		"collection_id": null,
		"title": "线下活动测试",
		"start_date": "2023-11-03",
        "end_date": "2023-11-03",
		"activity_type": 1,
        "activity_category": 1,
        "register_method": 1,
        "register_url": "https://xxxxxx.com"
        "online_url": "https://xxxx.com"
		"synopsis": "",
		"address": "北京市北京市东城区xxxxxx",
		"detail_address": "东城区xxxxxxxx",
		"longitude": "",
		"latitude": "",
		"schedules": "",
		"poster": 1,
		"status": 2,
		"user": 4,
		"replay_url": null,
}
```

### 13.我已经发布的活动列表

请求路径：/mypublishedactivities/?page=1&size=10

请求方式：get请求

请求参数：

+ 查询参数

  ~~~json
  page: 第几页
  size: 每页的大小
  ~~~

返回参数：

~~~json
{
	"total": 50,
	"page": 1,
	"size": 10,
	"data": [{
		"id": 1,
		"collection_id": null,
		"title": "线下活动测试",
		"start_date": "2023-11-03",
        "end_date": "2023-11-03",
		"activity_type": 1,
        "activity_category": 1,
        "register_method": 1,
        "register_url": "https://xxxxxx.com"
        "online_url": "https://xxxx.com"
		"synopsis": "",
		"address": "北京市北京市东城区xxxxxx",
		"detail_address": "东城区xxxxxxxx",
		"longitude": "",
		"latitude": "",
		"schedules": "",
		"poster": 1,
		"status": 2,
		"user": 4,
		"replay_url": null,
	}]
}
~~~



### 14.我的待发布活动列表

请求路径：/mywaitingactivities/?page=1&size=10

请求方式：get请求

请求参数：

- 查询参数

  ```json
  page: 第几页
  size: 每页的大小
  ```

返回参数：

```json
{
	"total": 50,
	"page": 1,
	"size": 10,
	"data": [{
		"id": 1,
		"collection_id": null,
		"title": "线下活动测试",
		"start_date": "2023-11-03",
        "end_date": "2023-11-03",
		"activity_type": 1,
        "activity_category": 1,
        "register_method": 1,
        "register_url": "https://xxxxxx.com"
        "online_url": "https://xxxx.com"
		"synopsis": "",
		"address": "北京市北京市东城区xxxxxx",
		"detail_address": "东城区xxxxxxxx",
		"longitude": "xxxxx",
		"latitude": "xxxxx",
		"schedules": "",
		"poster": 1,
		"status": 2,
		"user": 4,
		"replay_url": null,
}]
}
```



### 15.活动草案列表

请求路径：/drafts/?page=1&size=10

请求方式：get请求

请求参数：

- 查询参数

  ```json
  page: 第几页
  size: 每页的大小
  ```

返回参数：

```json
{
	"total": 50,
	"page": 1,
	"size": 10,
	"data": [{
		"id": 1,
		"collection_id": null,
		"title": "线下活动测试",
		"start_date": "2023-11-03",
        "end_date": "2023-11-03",
		"activity_type": 1,
        "activity_category": 1,
        "register_method": 1,
        "register_url": "https://xxxxxx.com"
        "online_url": "https://xxxx.com"
		"synopsis": "",
		"address": "北京市北京市东城区xxxxxx",
		"detail_address": "东城区xxxxxxxx",
		"longitude": "xxxxx",
		"latitude": "xxxxx",
		"schedules": "",
		"poster": 1,
		"status": 2,
		"user": 4,
		"replay_url": null,
	}]
}
```

### 16.收藏活动

请求路径：/activity/action/collect/

请求方法：post请求

请求参数：

- 请求体，json格式

  ```json
  {
      "activity": # int类型，活动的id
  }
  ```

返回参数：

```json
{
    "code": 200, 
    "msg": "Collection activity", 
    "access": ""
}
```

### 17.取消收藏活动

请求路径：/activity/action/collectdel/<int:pk>/

请求方法：delete请求

请求参数：

- 路径参数：

  ```json
  pk: # int类型，活动id
  ```

返回参数：

```json
{
    "code": 200, 
    "msg": "Collection activity", 
    "access": ""
}
```

### 18.查看我收藏的活动(分页查询)

请求路径：/activitycollections/?page=1&size=10

请求方法：get请求

请求参数：

- 查询参数

  ```json
  page: int类型，第几页
  size: int类型，每页的大小
  ```

返回参数：

```json
{
	"total": 50,
	"page": 1,
	"size": 10,
	"data": [{
		"id": 1,
		"collection_id": null,
		"title": "线下活动测试",
		"start_date": "2023-11-03",
        "end_date": "2023-11-03",
		"activity_type": 1,
        "activity_category": 1,
        "register_method": 1,
        "register_url": "https://xxxxxx.com"
        "online_url": "https://xxxx.com"
		"synopsis": "",
		"address": "北京市北京市东城区xxxxxx",
		"detail_address": "东城区xxxxxxxx",
		"longitude": "xxxxx",
		"latitude": "xxxxx",
		"schedules": "",
		"poster": 1,
		"status": 2,
		"user": 4,
		"replay_url": null,
}]
}
```

### 19.查询最近的活动列表(分页查询)

请求路径：/recentactivities/?page=1&size=10

请求方式：get请求

请求参数：

- 查询参数

  ```json
  page: int类型，第几页
  size: int类型，每页的大小
  ```

返回参数：

~~~json
{
	"total": 50,
	"page": 1,
	"size": 10,
	"data": [{
		"id": 1,
		"collection_id": null,
		"title": "线下活动测试",
		"start_date": "2023-11-03",
        "end_date": "2023-11-03",
		"activity_type": 1,
        "activity_category": 1,
        "register_method": 1,
        "register_url": "https://xxxxxx.com"
        "online_url": "https://xxxx.com"
		"synopsis": "",
		"address": "北京市北京市东城区xxxxxx",
		"detail_address": "东城区xxxxxxxx",
		"longitude": "xxxxx",
		"latitude": "xxxxx",
		"schedules": "",
		"poster": 1,
		"status": 2,
		"user": 4,
		"replay_url": null,
	}]
}
~~~

### 20.查看各类活动计数

请求路径：/countactivities/

请求方法：get请求

请求参数：无

返回参数：

```json
{
	"all_activities_count": 0,         # 全部         
	"registering_activities_count": 0, # 报名中     
	"going_activities_count": 0,	   # 进行中	 
	"completed_activities_count": 0    # 已结束   
}
```



## 四、官网活动

### 1.查询那些日期有数据

请求路径：/meeting_activity_date/?type=all

请求方式： get请求

请求参数：

- 路径参数

  ```json
  type: # all: 查询会议和活动; meetings:查询会议; activity：查询活动。
  ```

返回参数：

```json
{
    "code": 200,
    "msg": "success",
    "data": ["2023-11-16", "2023-11-17", "2023-11-18"]
}
```

### 2.查询某天的具体活动

请求路径：/meeting_activity_data/?date=2023-11-16&type=all

请求方式： get请求

请求参数：

- 路径参数

  ```json
  date: # 查询的某一天,时间类型： 2023-11-16
  type: # string类型
  ```

返回参数：

```json
{
    "code": 200,
    "msg": "success",
    "data": {
    date: "2023-11-16",
    timeData: [
        // 会议
        {
            "id": 1, 
            "group_name": "xxxx", 
            "startTime": "8:00",
            "endTime": "11:00",
            "duration_time": "8:00-11:00",
            "name": "xxxxx",
            "creator": "xxx",
            "detail": "detail",
            "join_url": "https://xxxx.com",
            "meeting_id": "mid",
            "etherpad": "https://xxxx.xxxx.org",
            "platform": "zoom",
            "video_url": "https://xxxx.com",
        },
        // 活动
        {
            "id": 3,
            "title": "xxx",
            "start_date": "2023-11-03",
            "end_date": "2023-11-03",
            "activity_type": 1,
            "address": "北京市北京市xxxxx",
            "detail_address": "东城区灯市口xxxxxxx",
            "longitude": "",
            "latitude": "",
            "synopsis": "",
            "sign_url": "",
            "replay_url": null,
            "register_url": "https://xxxxxx.com",
            "poster": 4,
            "wx_code": "",
            "schedules": ""
		}]
	}
}
```



## 五.功能性

1.心跳检查

请求路径：/ping/

请求方式： get请求

请求参数: 无

返回参数：

~~~json
{
    "code": 200,
    "msg": "the status is ok"
}
~~~




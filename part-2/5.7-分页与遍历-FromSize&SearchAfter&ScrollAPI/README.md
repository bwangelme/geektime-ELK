# 分页与遍历 - From, Size, Search_after & Scroll API

## 查询场景说明

普通：试试获取顶部的文档
scroll: 需要全部的文档
分页：
    1. 使用 from 和 size
    2. 如果需要使用深度分页，使用 search after API。这导致只能往后查询

## 课程Demo

```sh
POST tmdb/_search
{
  "from": 10000,
  "size": 1,
  "query": {
    "match_all": {

    }
  }
}

#Scroll API
DELETE users

POST users/_doc
{"name":"user1","age":10}

POST users/_doc
{"name":"user2","age":11}


POST users/_doc
{"name":"user2","age":12}

POST users/_doc
{"name":"user2","age":13}

POST users/_count

POST users/_search
{
    "size": 1,
    "query": {
        "match_all": {}
    },
    "sort": [
        {"age": "desc"} ,
        {"_id": "asc"}
    ]
}

# search after 使用的是上次结果返回的 sort 字段
POST users/_search
{
    "size": 1,
    "query": {
        "match_all": {}
    },
    "search_after":
        [
          10,
          "uGjpoHIBwlwpmzsxhvAv"],
    "sort": [
        {"age": "desc"} ,
        {"_id": "asc"}
    ]
}


# Scroll API
# 调用的第一次，根据指定的存活时间创建一个快照
DELETE users
POST users/_doc
{"name":"user1","age":10}

POST users/_doc
{"name":"user2","age":20}

POST users/_doc
{"name":"user3","age":30}

POST users/_doc
{"name":"user4","age":40}

# 设定这个快照的存活时间为5分钟
POST /users/_search?scroll=5m
{
    "size": 1,
    "query": {
        "match_all" : {
        }
    }
}

# 由于 scroll 查询的是快照，所以新增的文档不会被查询到
POST users/_doc
{"name":"user5","age":50}

POST /_search/scroll
{
    "scroll" : "1m",
    "scroll_id" : "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAWAWbWdoQXR2d3ZUd2kzSThwVTh4bVE0QQ=="
}
```

# 对象及Nested对象

### 包含嵌套对象的文档

```sh
# 创建博客文档

PUT /blog
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text"
      },
      "time": {
        "type": "date"
      },
      "user": {
        "properties": {
          "city": {
            "type": "text"
          },
          "userid": {
            "type": "long"
          },
          "username": {
            "type": "keyword"
          }
        }
      }
    }
  }
}

# 向博客文档中插入数据
PUT blog/_doc/1
{
  "content": "I Like ElasticSearch",
  "time": "2020-05-10T21:45:12",
  "user": {
    "userid": 1,
    "username": "Jack",
    "city": "Shanghai"
  }
}

# 查询 Blog 信息
POST blog/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"content": "ElasticSearch"}},
        {"match": {"user.username": "Jack"}}
      ]
    }
  }
}
```

### 包含对象数组的文档

```sh
# 创建电影的文档

PUT my_movies
{
  "mappings": {
    "properties": {
      "actors": {
        "properties": {
          "first_name": {
            "type": "keyword"
          },
          "last_name": {
            "type": "keyword"
          }
        }
      },
      "title": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      }
    }
  }
}

# 写入一条电影信息
POST my_movies/_doc/1
{
  "title": "Speed",
  "actors": [
    {"first_name": "Keanu", "last_name": "Reeves"},
    {"first_name": "Dennis", "last_name": "Hopper"}
  ]
}

# 由于 ES 会将数组的每个字段都扁平存储，所以以下查询能查到结果
# "title": "speed"
# "actor.first_name": ["Keanu", "Dennis"],
# "actor.last_name": ["Reeves", "Hoppers"]
GET my_movies/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"actors.first_name": "Keanu"}},
        {"match": {"actors.last_name": "Hopper"}}
      ]
    }
  }
}
```

### Nested 数据类型

Nested 数据类型允许对象数组中的对象被独立索引，在 ES 内部，Nested 文档会被保存在两个 Lucene 文档中，在查询时做 Join 处理。

```sh
# 创建电影的文档

PUT my_movies
{
  "mappings": {
    "properties": {
      "actors": {
        # 注意这里声明了类型为 nested
        "type": "nested",
        "properties": {
          "first_name": {
            "type": "keyword"
          },
          "last_name": {
            "type": "keyword"
          }
        }
      },
      "title": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      }
    }
  }
}

# 写入一条电影信息
POST my_movies/_doc/1
{
  "title": "Speed",
  "actors": [
    {"first_name": "Keanu", "last_name": "Reeves"},
    {"first_name": "Dennis", "last_name": "Hopper"}
  ]
}

# 通过一个嵌套对象字段进行查询
GET my_movies/_search
{
  "query": {
    # 声明查询的字段是嵌套字段
    "nested": {
      # 指出嵌套字段的位置
      "path": "actors",
      # 在嵌套字段内的查询方式
      "query": {
        "bool": {
          "should": [
            {"match": {"actors.first_name": "Keanu"}},
            {"match": {"actors.last_name": "Hopper"}}
          ]
        }
      }
      # 另一种简单的查询
      # "query": {
      #   "match": {"actors.first_name": "Keanu"}
      # }
    }
  }
}

# 使用 Nested 查询
GET my_movies/_search
{
  "query":{
    "nested": {
      "path": "actors",
      "query": {
        "bool": {
          "must": [
            {"match": {"actors.first_name": "Keanu"}},
            {"match": {"actors.last_name": "Reeves"}}
          ]
        }
      }
    }
  }
}

# 对嵌套对象的字段进行聚合
GET my_movies/_search
{
  "size": 0,
  "aggs": {
    "actors": {
      "nested": {
        "path": "actors"
      },
      "aggs": {
        "acotr_name": {
          "terms": {
            "field": "actors.first_name",
            "size": 10
          }
        }
      }
    }
  }
}
```

## 课程demos
```
DELETE blog
# 设置blog的 Mapping
PUT /blog
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text"
      },
      "time": {
        "type": "date"
      },
      "user": {
        "properties": {
          "city": {
            "type": "text"
          },
          "userid": {
            "type": "long"
          },
          "username": {
            "type": "keyword"
          }
        }
      }
    }
  }
}


# 插入一条 Blog 信息
PUT blog/_doc/1
{
  "content":"I like Elasticsearch",
  "time":"2019-01-01T00:00:00",
  "user":{
    "userid":1,
    "username":"Jack",
    "city":"Shanghai"
  }
}


# 查询 Blog 信息
POST blog/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"content": "Elasticsearch"}},
        {"match": {"user.username": "Jack"}}
      ]
    }
  }
}


DELETE my_movies

# 电影的Mapping信息
PUT my_movies
{
      "mappings" : {
      "properties" : {
        "actors" : {
          "properties" : {
            "first_name" : {
              "type" : "keyword"
            },
            "last_name" : {
              "type" : "keyword"
            }
          }
        },
        "title" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        }
      }
    }
}


# 写入一条电影信息
POST my_movies/_doc/1
{
  "title":"Speed",
  "actors":[
    {
      "first_name":"Keanu",
      "last_name":"Reeves"
    },

    {
      "first_name":"Dennis",
      "last_name":"Hopper"
    }

  ]
}

# 查询电影信息
POST my_movies/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"actors.first_name": "Keanu"}},
        {"match": {"actors.last_name": "Hopper"}}
      ]
    }
  }

}

DELETE my_movies
# 创建 Nested 对象 Mapping
PUT my_movies
{
      "mappings" : {
      "properties" : {
        "actors" : {
          "type": "nested",
          "properties" : {
            "first_name" : {"type" : "keyword"},
            "last_name" : {"type" : "keyword"}
          }},
        "title" : {
          "type" : "text",
          "fields" : {"keyword":{"type":"keyword","ignore_above":256}}
        }
      }
    }
}


POST my_movies/_doc/1
{
  "title":"Speed",
  "actors":[
    {
      "first_name":"Keanu",
      "last_name":"Reeves"
    },

    {
      "first_name":"Dennis",
      "last_name":"Hopper"
    }

  ]
}

# Nested 查询
POST my_movies/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"title": "Speed"}},
        {
          "nested": {
            "path": "actors",
            "query": {
              "bool": {
                "must": [
                  {"match": {
                    "actors.first_name": "Keanu"
                  }},

                  {"match": {
                    "actors.last_name": "Hopper"
                  }}
                ]
              }
            }
          }
        }
      ]
    }
  }
}


# Nested Aggregation
POST my_movies/_search
{
  "size": 0,
  "aggs": {
    "actors": {
      "nested": {
        "path": "actors"
      },
      "aggs": {
        "actor_name": {
          "terms": {
            "field": "actors.first_name",
            "size": 10
          }
        }
      }
    }
  }
}


# 普通 aggregation不工作
POST my_movies/_search
{
  "size": 0,
  "aggs": {
    "NAME": {
      "terms": {
        "field": "actors.first_name",
        "size": 10
      }
    }
  }
}

```
## 相关阅读
- https://www.elastic.co/guide/en/elasticsearch/reference/7.1/query-dsl-nested-query.html

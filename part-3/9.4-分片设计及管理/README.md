# 分片设计及管理

+ 日志类应用单个分片不超过50G
+ 搜索类应用单个分片不超过20G


## 课程Demo

```
# 查看分片的大小
GET /_cat/shards/movie
```

## 相关阅读
- https://www.elastic.co/guide/en/elasticsearch/reference/7.1/cluster-reroute.html
- https://www.elastic.co/guide/en/elasticsearch/reference/7.1/indices-forcemerge.html
- https://www.elastic.co/guide/en/elasticsearch/reference/current/allocation-total-shards.html

# 剖析分布式查询及相关性评分

## 搜索的运行机制

搜索分成了两步:

1. Query
2. Fetch

### Query

1. 请求达到的节点成为 `Coordinating` 节点，它在6个主副分片中随机选择3个，发送查询请求。
2. 被选中的分片执行查询，进行排序，每个分片都会返回 From + Size 个排序后的文档ID和排序分数给 Coordinating 节点

### Fetch

1. `Coordinating` 节点从每个分片获取到文档节点和排序值后，重新进行排序，并选取 [from:from+size] 的文档ID
2. 以 Multi Get 的方式从响应的节点上获取对应的文档。

## 潜在的问题

### 性能问题

1. 如果主分片数很多的话，一次性查询的节点将非常多
2. 处理深度分页将会是一个很大的性能挑战

### 相关性算分

1. 每个分片上文档的算法都是基与本分片上的文档进行计算，如果分片上的文档过少，会导致算分偏离的情况。

解决办法:
> 1. 保证文档均匀地分布在各个分片上，如果文档很少，设置1个分片即可。
> 2. 搜索的 URL 中指定参数 `_search?search_type=dfs_query_then_fetch`，它会到每个分片把各分片的词频和文档频率进行搜集，进行一次完整的相关性算分，耗费CPU和内存较高，一般不建议使用。

## 课程demo
```sh
DELETE message
PUT message
{
  "settings": {
    "number_of_shards": 20
  }
}

GET message

# 指定三个文档在不同的分片上
POST message/_doc?routing=1
{
  "content":"good"
}

POST message/_doc?routing=2
{
  "content":"good morning"
}

POST message/_doc?routing=3
{
  "content":"good morning everyone"
}

POST message/_search
{
  "explain": true,
  "query": {
    "match_all": {}
  }
}

# 查询 Good，可以看到三个文档的算法是相同的。
POST message/_search
{
  "explain": true,
  "query": {
    "term": {
      "content": {
        "value": "good"
      }
    }
  }
}


# 加上 search_type 参数后，三个文档的分数不同了，content="good" 排在了第一位
POST message/_search?search_type=dfs_query_then_fetch
{

  "query": {
    "term": {
      "content": {
        "value": "good"
      }
    }
  }
}

```

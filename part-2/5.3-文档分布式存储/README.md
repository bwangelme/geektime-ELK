# 文档分布式存储

## 文档到分片的路由算法

```
shard = hash(_routing) % number_of_primary_shards
```

`_routing` 默认是文档的ID，也可以在创建文档时自己制定。

因为文档的存储位置和主分片数有关，所以主分片的数量不能更改。

## 文档的更新与删除

+ 更新一个文档

![](https://tva1.sinaimg.cn/large/007S8ZIlly1gfet6sd7waj31c10m8tbg.jpg)

+ 删除一个文档

![](https://tva1.sinaimg.cn/large/007S8ZIlly1gfet7cl50sj317m0o67d2.jpg)

# 分片及其生命周期

分片是 ES 中的一个最小工作单元，对应 Lucene 的 Index

倒排索引是不可改变。

Segment 对应一个文档的倒排索引。
Lucene 的所有 Segment 的信息存储在 Commit Point 中。
Lucene 删除文档后不会立刻删除，而是存在 `.del` 文件中。

## Refresh

ES 写文档时先写入 Index Buffer，Refresh 的时候再写入 Segment 中。 Refresh 每秒执行一次(index.refresh_interval)。Index Buffer 占满时也会触发 Refresh。

## Transaction Log

写文档的时候，除了写 Index Buffer，也会写 Transaction Log，用于确保文档断电时不丢失。

## Flush

Refresh 刷新所有的 Index Buffer，将 Segment 落盘，清空 Transaction，默认30分钟执行一次。

## Merge

合并 Segment，删除 `.del` 中的文档。

```
POST myindex/_forcemerge
```

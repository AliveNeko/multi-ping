# 批量检测 IP 的脚本

## 使用方法

#### 环境配置

如果没有安装`uv`，请参考[此处](https://docs.astral.sh/uv/getting-started/installation/)安装`uv`。

#### 拉取项目到本地

```shell
git clone https://github.com/AliveNeko/multi-ping.git
```

#### 设置 IP 

在`ip.txt `文件中填写想要测试的 IP 数据，每行一个 IP地址。

#### 执行

执行运行命令（会自动下载依赖）：

```shell
uv run main.py
```

## 效果

`ip.txt`文件内容：

```
1.1.1.1
```

执行后，`result.csv`的内容：

```csv
IP,平均延迟,丢包率,地区,ASN
1.1.1.1,313.13 ms,0.0%,AU,"Cloudflare, Inc."
```

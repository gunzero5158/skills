# 百度网盘与 OpenList 工作流

## 范围与入口
- 百度成为归档主库后，读取本机 LOCALAPPDATA/GamePortArchive/baidu_connection.json 确认目标；不要继续默认写 Google Drive。挂载名称可被用户修改，按驱动、存储 ID 和真实 root_folder_path 核实，不能硬编码“游戏合集”。
- 游戏归档与用户其他资料分目录挂载。Google 全盘复制必须由用户明确指定范围；源入口优先只读，使用复制而非移动，不自动删除源文件。
- OpenList 的挂载路径是界面入口；root_folder_path 才是百度真实目录。保存成功、work、可列目录、可传输和校验通过是不同状态。

## 授权与诊断
- 用户在官方登录页完成授权，令牌仅放本机或经授权的服务器私有配置，不发到聊天、合集或 GitHub。
- 使用 OpenList 提供参数时，在授权页打开相应开关，生成 Refresh Token；不要把 Access Token 填入刷新令牌。共享模式与使用在线 API 配套，自有客户端按官方驱动文档设置。
- empty token 先只检查刷新令牌是否为空及配置模式，勿输出令牌，也不能仅据错误文字认定用户填错。
- Google deleted_client 指授权请求所用 OAuth 客户端失效，不等于密码错误。已有 rclone 授权可能仍有效，先真实只读测试；可通过本机认证 WebDAV 桥接，避免将不配套客户端的令牌直接复制到 OpenList。

## 迁移与验收
- 先进行小文件和大压缩包上传、下载读回 SHA256 测试。无服务端 SHA256 时不能把本地哈希伪装成云端哈希；如采用 MD5/大小证据，单独标注验证等级。
- 首次迁移枚举全部受管文件，排除经确认的工具配置目录；保留本地和原云盘。维护相对路径、大小、本地 SHA256、读回结果的紧凑清单。
- 同名文件默认不覆盖：比较后跳过相同项，不同项停止处理。续传先确认本地内容未变；中断任务的“已上传”不能直接记为“已验证”。
- HTTP Range 校验须检查 206、Content-Range、分段长度，按顺序计算完整 SHA256。限制并发和在途缓冲，避免一次保留数 GB 分片。
- 完成后刷新并分页读取云端全目录，核对路径集合、数量、大小及重复项；报告读回证据与目录审计边界。任务列表完成不替代完整性验收。
- 更新顺序：新包暂存上传并核验、发布一致的新记录、确认后把被替代旧包移入可恢复区。失败可恢复，不以不完整暂存目录运行删除型 sync。

## 本机与 VPS
- 本机 OpenList+rclone：Google→本机→百度，是否计入 VPN 流量由实际分流决定。远端 OpenList 若仍接本机 rclone，数据仍经过本机。
- VPS 中转必须将两端服务都放在 VPS；管理界面仅监听 loopback，通过 SSH 隧道访问。部署前后核对既有 VPN/Tailscale 服务及监听端口，不修改路由、防火墙或重启既有服务。
- 用户需授权将网盘凭证放到指定 VPS。限制配置权限；不能为方便公开暴露 WebDAV、管理 API 或令牌。
- 百度驱动的 upload_thread 配置是字符串（如 "1"）；改 JSON 时保留字段类型，初始化错误可能回显敏感配置片段，日志需脱敏。
- rclone vfs-cache-mode off 不代表 OpenList 不落盘。检查 OpenList 实际 temp_dir、复制任务和缓存占用；正常完成可清理，崩溃或失败可能残留。仅在无活动任务且确定用途后清理。
- 低内存 VPS 使用单任务或低并发，限制缓冲、上传线程和服务内存。磁盘只需满足最大在途文件及余量，但百度上传可能要求暂存完整文件，不能承诺任意大文件完全流式。
- 长任务使用独立服务与持久状态；浏览器关闭不应终止传输。跨盘复制先小批实测，Google 原生文档导出、同名文件、共享盘等需单独验证。

## 已有本机部署线索
- OpenList：LOCALAPPDATA/GamePortArchive/OpenList，服务端口 15244。
- 维护脚本与证据：D:/projects/game-archive-maintenance；Google 桥接为 google-drive-bridge，端口 15245，只读。
- 本机临时目录已迁至 D:/projects/game-archive-maintenance/openlist-temp；以实际配置为准。
- VPS 使用 ~/game-archive，独立 systemd 服务 game-archive-openlist 与 game-archive-drive。15244/15245 仅 loopback；本机 SSH 管理隧道为 25244。连接参数与凭据仅保存于私有维护目录，不写进技能。
- 验证跨云路径应从真实 Google 文件发起 OpenList copy，并从百度读回比对；小文件通过不代表 1.5TB 或超大单文件已验证。
- 以上是定位线索，不是永久保证；操作前核实配置和进程。旧 C 盘日期工作目录已清理，不再依赖其路径。

参考：https://doc.oplist.org/guide/drivers/baidu 、 https://rclone.org/commands/rclone_serve_webdav/

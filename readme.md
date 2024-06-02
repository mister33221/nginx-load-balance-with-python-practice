# [Nginx]

- [Load Balancer](#load-balancer)
- [Nginx 介紹](#nginx-%E4%BB%8B%E7%B4%B9)

以下我們先來舉幾個問題，讓大家了解為什麼我們需要一個 Nginx 插在 Client 和 Server 之間。

1. 當你開啟了 Airbnb 時，從你的手機發送一個 request，會經過網路、到達 Airbnb 的伺服器，然後 Airbnb 的伺服器會回傳 response 給你的手機。
    而現在 Airbnb 的用戶數量非常的龐大，如果我們只有一台 Server，那麼這台 Server 就會非常的忙碌。
    這時我們就需要增加 Server 的數量，讓每一台 Server 都可以處理一部分的 request，這樣就可以分散 Server 的負擔。
    那我們又該如何讓這些 Server 之間可以協同工作呢？這時就需要一個 Load Balancer 來幫忙了。
2. 現在大多數了網頁，為了安全，都會使用 HTTPS，這就表示 Server 和 Client 之間的資料都是加密的。當我們只有一台 Server，只需要安裝一個 SSL 憑證就可以了。
    但是當我們有多台 Server 時，我們就需要在每一台 Server 上都安裝 SSL 憑證，這樣就會變得非常的麻煩。
    這時我們就可以將 SSL 憑證安裝在 Load Balancer 上，然後再將 request 轉發給 Server，這樣就可以省去在每一台 Server 上安裝 SSL 憑證的麻煩。

## Load Balancer

Load Balancer 是一個位於 Client 和 Server 之間的裝置，它的主要功能是將 Client 發送的 request 分配給 Server，讓 Server 可以平均的處理 request。
Load Balancer 有很多種演算法，例如：Round Robin、Least Connections、IP Hash 等等，這些演算法可以讓我們根據不同的需求來做不同的設定。

## Nginx 介紹

Nginx 是一個非常著名的 Web Server，它的特點是非常的輕量、穩定、高效，所以很多公司都會使用 Nginx 來當作 Load Balancer。
回到 Airbnb 的例子，當你開啟了 Airbnb 時，我們將 request 先送到 Nginx，然後 Nginx 會根據我們的設定，將 request 分配給不同的 Server。
這麼一來，我們就可以平均的分配 request 給不同的 Server，讓每一台 Server 都可以處理一部分的 request，這樣就可以分散 Server 的負擔。

## 安裝 Nginx

我是直接使用 Podman(docker desktop就把podman改成 docker 就可以囉) 來安裝 Nginx，這樣就不用擔心會影響到我的系統。直接安裝在本機上的方法網路上很多，可以依照自己的系統來找尋教學。

- 安裝 Podman
```bash
# 安裝 Nginx
$ podman run -d -p 80:80 --name myNginx nginx
```
- 查看是否安裝成功
```bash
$ podman ps
```

## 查看 Nginx 的設定檔

- 直接查看 nginx.conf
```bash
$ podman exec -it <container ID> cat /etc/nginx/nginx.conf
```
- 進入 Nginx 容器
```bash
$ podman exec -it <container ID> /bin/bash
```
- 進入 Nginx 的設定檔
```bash
$ cd /etc/nginx
```
- 我要要專注的是 Nginx 的設定檔，所以我們先來看看 Nginx 的設定檔長什麼樣子
```bash
$ cat nginx.conf
```
```conf

user  nginx;  # 指定 Nginx 的用戶名稱
worker_processes  auto;  # 指定 Nginx 的 worker process 數量，auto 表示自動設定，通常會設定為 CPU 的核心數量

error_log  /var/log/nginx/error.log notice; # 指定 Nginx 的錯誤日誌存放位置
pid        /var/run/nginx.pid; # 指定 Nginx 的 PID 檔存放位置，PID是 Process ID 的縮寫，也就是進程 ID，進程是用來執行程式的一個實例


events {
    worker_connections  1024; # 指定每個 worker process 可以處理的連線數量，通常會設定為 1024
}


http {
    include       /etc/nginx/mime.types; 
    default_type  application/octet-stream; 

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" ' 
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main; 

    sendfile        on; 
    #tcp_nopush     on;

    keepalive_timeout  65; 

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}
```
> MIME（Multipurpose Internet Mail Extensions）類型是一種標準，用於描述和標籤數據的內容類型。這種標籤可以幫助接收數據的軟體（如瀏覽器）理解如何處理數據。
> MIME 類型由兩部分組成：類型和子類型，兩者之間由一個斜線（/）分隔。
> - text/html：這是 HTML 文件的 MIME 類型。當瀏覽器接收到這種類型的內容時，它會將其作為 HTML 文檔來處理。
> - image/jpeg：這是 JPEG 圖像的 MIME 類型。當瀏覽器接收到這種類型的內容時，它會將其作為圖像來處理。
> - application/pdf：這是 PDF 文件的 MIME 類型。當瀏覽器接收到這種類型的內容時，它會將其作為 PDF 文件來處理。

以下我們來解釋 nginx.conf 中的設定
- user nginx：
    指定 Nginx 的用戶名稱，這裡指定為 nginx。
- worker_processes auto：
    指定 Nginx 的 worker process 數量，這裡設定為 auto，表示自動設定，通常會設定為 CPU 的核心數量。
- error_log /var/log/nginx/error.log notice：
    指定 Nginx 的錯誤日誌存放位置，這裡指定為 /var/log/nginx/error.log，並且只記錄 notice 級別的錯誤。
- pid /var/run/nginx.pid：
    指定 Nginx 的 PID 檔存放位置，PID是 Process ID 的縮寫，也就是進程 ID，進程是用來執行程式的一個實例。
- events：
    指定 Nginx 的事件模塊，這裡設定了 worker_connections，表示每個 worker process 可以處理的連線數量，通常會設定為 1024。
- http：
    指定 Nginx 的 HTTP 模塊，這裡設定了一些 HTTP 相關的配置，例如 MIME types、log format、access log、sendfile、keepalive_timeout 等。
- include /etc/nginx/conf.d/*.conf：
    包含 /etc/nginx/conf.d/ 目錄下的所有以 .conf 結尾的文件，這樣可以將配置文件分開管理，使配置更加清晰。
- log_format：
    定義了一個 log format，這裡的 main 是 log format 的名稱，可以自己定義。log format 用來指定日誌的格式，可以包含一些變量，例如 $remote_addr、$remote_user、$time_local 等。
    - `$remote_addr`：客戶端的 IP 地址。
    - `$remote_user`：用戶名。
    - `$time_local`：伺服器本地時間。
    - `$request`：請求的 URI 和 HTTP 協議。
    - `$status`：HTTP 狀態碼。
    - `$body_bytes_sent`：發送給客戶端的字節數。
    - `$http_referer`：請求的 Referer 頭部，表示請求來源的 URI。
    - `$http_user_agent`：請求的 User-Agent 頭部，表示客戶端的軟體類型。
    - `$http_x_forwarded_for`：請求的 X-Forwarded-For 頭部，當請求經過代理時，這個頭部可以包含原始客戶端的 IP 地址。
- access_log：
    指定 Nginx 的存取日誌存放位置和 log format，這裡的 main 就是上面定義的 log format。
- sendfile：
    指定是否開啟 sendfile 功能，sendfile 是一個高效的文件傳輸機制，可以提高文件的傳輸效率。當 sendfile 設定為 on 時，Nginx 會使用 sendfile 系統調用來傳輸靜態文件，這可以提高靜態文件的傳輸速度，並減少 CPU 的使用率。這對於服務大量靜態文件的網站來說，可以提供顯著的性能提升。然而，請注意，sendfile 只適用於傳輸靜態文件，對於動態內容（如 PHP、Python 等生成的內容），sendfile 不會有任何效果。
- tcp_nopush：
    指定是否開啟 tcp_nopush 功能，tcp_nopush 是一個 TCP 協議的擴展，可以提高網絡傳輸的效率。當 tcp_nopush 設定為 on 時，Nginx 會嘗試合併多個小的數據塊到一個 TCP 包中，然後一次性發送，以減少網絡包的數量並提高網絡效率。這對於靜態文件的傳輸尤其有用，因為它可以減少網絡延遲並提高文件傳輸的速度。請注意，tcp_nopush 指令只有在 sendfile 指令設定為 on 時才會生效，因為它依賴於 sendfile 系統調用來傳輸文件。此外，tcp_nopush 指令只對靜態文件的傳輸有影響，對於動態內容（如 PHP、Python 等生成的內容），它不會有任何效果。
- keepalive_timeout：
    指定 Nginx 的 keepalive_timeout，這裡設定為 65，表示 Nginx 在關閉閒置連接之前會等待 65 秒。keepalive_timeout 指令的值是一個時間長度（以秒為單位），表示 Nginx 在關閉閒置連接之前會等待多長時間。例如，如果 keepalive_timeout 設定為 60，那麼 Nginx 會在一個連接閒置 60 秒後關閉它。
- gzip：
    指定是否開啟 gzip 壓縮功能，gzip 是一種文件壓縮算法，可以將文件的大小壓縮到原來的大小的一部分。在網絡傳輸中，使用 gzip 壓縮可以減少傳輸的數據量，從而提高傳輸速度和效率。當 gzip 指令設定為 on 時，Nginx 會將 HTTP 響應壓縮為 gzip 格式，然後再發送給客戶端。客戶端（如瀏覽器）收到壓縮的響應後，會自動解壓並處理。
- include /etc/nginx/conf.d/*.conf：
    包含 /etc/nginx/conf.d/ 目錄下的所有以 .conf 結尾的文件，這樣可以將配置文件分開管理，使配置更加清晰。

## 查看 Nginx 的預設的 html 歡迎頁

- 進入 Nginx 容器
```bash
$ podman exec -it <container ID> /bin/bash
```
- 查看 Nginx 的 html 檔案
```bash
$ cat /usr/share/nginx/html/index.html
```
```html
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

## 如果我的網站還有包含一些靜態檔案，例如：圖片、CSS、JavaScript 等，我該如何部署到 Nginx 上呢？

- 來說明一下 nginx 中的 mime.types
    - 在空白的 `nginx.conf` 中，我們會需要自己指定那些種類的 mime type，這樣 Nginx 才能正確的處理這些檔案。如下
```conf
http{
    types {
        text/html html htm shtml;
        text/css css;
        text/xml xml;
        image/gif gif;
        image/jpeg jpeg jpg;
        application/javascript js;
        application/json json;
        application/xml xml;
    }

    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;
        location / {
            try_files $uri $uri/ /index.html;
        }
    }
}
```
- 但種類這麼多怎麼辦?，所以 Nginx 提供了一個 `mime.types` 檔案，這個檔案中包含了許多常見的 mime type，檔案位置在 `/etc/nginx/mime.types`。我們可以把內容全部複製到 `nginx.conf` 的 `http` 區塊中，這樣就不用自己指定 mime type 了。
- 但複製一大串的 mime type 會讓 `nginx.conf` 變得很長，也好麻煩(你是鹿丸嗎?)，所以我們可以使用 `include` 來引入 `mime.types` 檔案，這樣就可以讓 `nginx.conf` 變得更加簡潔。
```conf
http{
    include /etc/nginx/mime.types;

    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;
        location / {
            try_files $uri $uri/ /index.html;
        }
    }
}
```
- 當然我們也可在預設的 `nginx.conf` 中找到 `include /etc/nginx/mime.types;`，這樣就不用自己指定 mime type 了。

> `$uri`：請求的 URI，也就是當我們的網址是 `http://localhost/about` 時，$uri 就是 `/about`。
> `ry_files $uri $uri/ /index.html;`：這個指令的作用是嘗試根據請求的 URI 來查找文件，如果找到了就返回該文件，如果找不到就查找 URI/ 目錄，如果還是找不到就返回 index.html 文件。

## Serving 靜態內容

想要在 Nginx 上服務靜態內容，我們的目標就是取代 Nginx 預設的 html 檔案，讓 Nginx 服務我們自己的 html 檔案。

1. 我們先來建立一個靜態的 html 檔案，這裡我們建立一個 `index.html` 檔案，內容如下：
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>
```
2. 接著我們來解自己的 docker-compose.yaml。再前面我們有提到 Nginx 的歡迎葉面是在 `/usr/share/nginx/html/index.html`，所以我們要將我們的 index.html 放到這個位置。
```yaml
version: '3' # 使用 Docker Compose 的版本
services:
  nginx:
    image: nginx # 使用 Nginx 映像檔
    ports:
      - "80:80" # 將本機的 80 port 對應到 Nginx 容器的 80 port。 <host port>:<container port>
    volumes: # 將本機的 index.html 掛載到 Nginx 容器的 /usr/share/nginx/html/index.html，取代 Nginx 預設的 html 檔案
      - ./index.html:/usr/share/nginx/html/index.html 
```
3. 接著我們到我們的專案資料夾，執行以下指令
```bash
$ docker-compose up -d # 啟動容器，`-d` 表示在背景執行，這樣就不會佔用終端機
```
4. 最後我們打開瀏覽器，輸入 `http://localhost`，就可以看到我們自己的 index.html 了。

## 如果我想要使用網址來訪問不同的分頁呢?

- 我們可以在 `nginx.conf` 中的 `server` 區塊中設定 `location`，這樣就可以根據不同的網址來訪問不同的分頁。
- 假設我們已經有了兩個靜態的 html 檔案，分別是 `index.html` 、 `about.html`、`contact.html`。
- 我們先了解遺下幾個用來指令文件路徑的指令
    - location root:
        - 這個指令用來設置請求地跟目錄，當 nginx 處理一個請求時，她會將請求的 url 添加到 root 設置的路徑後面，然後去這個路徑下查找文件。
        - 例如
        ```yaml
        location /dogs/ {
            root /data;
        }
        ```
        - 當請求的 url 是 `http://localhost/dogs/index.html` 時，nginx 會去 `/data/dogs/index.html` 下查找文件。
    - location alias:
        - 這個指令用來設置別名，當 nginx 處理一個請求時，她會將請求的 url 添加到 alias 設置的路徑後面，然後去這個路徑下查找文件。
        - 例如
        ```yaml
        location /cats/ {
            alias /data
        }
        ```
        - 當請求的 url 是 `http://localhost/cats/index.html` 時，nginx 會去 `/data/index.html` 下查找文件。
    - location try_files:
        - 這個指令用來嘗試查找文件，當 nginx 處理一個請求時，又在你指定的 root 或 alias 下找不到文件時，他會根據 try_files 指令的設置來查找文件。
        - 例如
        ```yaml
        location / {
            root /data;
            try_files /test1.html /test2.html =404;
        }
        ```
        - 當請求的 url 是 `http://localhost/` 時，nginx 會先在 `/data/` 下查找文件，如果找不到就會嘗試查找 `/data/test1.html`，如果還是找不到就會嘗試查找 `/data/test2.html`，如果還是找不到就返回 404 錯誤。
        - 另外你也可以使用 `$uri` 來代表請求的 URI，例如 `try_files $uri $uri/ /index.html;`。這時的 `$url` 就是請求的 URI，例如 `http://localhost/about` 的 `$uri` 就是 `/about`。
    - location 307 redirect:
        - 這個指令用來重定向，當 nginx 處理一個請求時，他會將請求重定向到指定的 url。
        - 例如
        ```yaml
        location /redirect {
            return 307 /about;
        }
        ```
        - 當請求的 url 是 `http://localhost/redirect` 時，nginx 會將請求重定向到 `http://localhost/about`。

## 將 Angular 專案部署到 Nginx

只部屬一個靜態的 html 很無聊對吧，我們來部屬一個 Angular 專案到 Nginx 上。

1. 我們先來建立一個 Angular 專案，這裡我們建立一個 `my-app` 專案。
```bash
$ ng new my-app
```
2. 接著我們要建立一個 docker-compose.yaml，這裡我們要將 Angular 專案的 dist 資料夾掛載到 Nginx 容器的 `/usr/share/nginx/html`，這樣 Nginx 就可以服務 Angular 專案了。
```yaml
version: '3' # 使用 Docker Compose 的版本
services:
  nginx:
    image: nginx # 使用 Nginx 映像檔
    ports:
      - "80:80" # 將本機的 80 port 對應到 Nginx 容器的 80 port。 <host port>:<container port>
    volumes: # 將 Angular 專案的 dist 資料夾掛載到 Nginx 容器的 /usr/share/nginx/html，取代 Nginx 預設的 html 檔案
      - ./my-app/dist/my-app:/usr/share/nginx/html
```

> 如果你不想使用 `/usr/share/nginx/html` 這個路徑，你可以自己定義一個路徑，例如：`/usr/share/nginx/my-app`。
> 那麼你可以透過修改 Nginx 的設定檔來指定這個路徑，例如：`/etc/nginx/conf.d/my-app.conf`。
> ```conf
> server {
>     listen 80;
>     server_name localhost;
>     root /usr/share/nginx/my-app;
>     index index.html;
>     location / { #
>         try_files $uri $uri/ /index.html;
>     }
> }
> ```
> 然後在 docker-compose.yaml 中指定這個設定檔
> ```yaml
> version: '3' # 使用 Docker Compose 的版本
> services:
>   nginx:
>     image: nginx # 使用 Nginx 映像檔
>     ports:
>       - "80:80" # 將本機的 80 port 對應到 Nginx 容器的 80 port。 <host port>:<container port>
>     volumes: 
>       - ./my-app/dist/my-app:/usr/share/nginx/my-app # 將 Angular 專案的 dist 資料夾掛載到 Nginx 容器的 /usr/share/nginx/my-app
>       - ./my-app.conf:/etc/nginx/conf.d/my-app.conf # 將 my-app.conf 掛載到 Nginx 容器的 /etc/nginx/conf.d/my-app.conf
> ```

## Load Balancer 流量分配

當我們有多台 Server 時，我們可以使用 Nginx 來做 Load Balancer，讓 Nginx 幫我們分配流量。


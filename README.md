# 代码运行
### 后端
```shell
conda create -n caa python=3.8 -y
conda activate caa
pip install -r requirements.txt

npm install -g ganache-cli
cd decert-backend/web3src
python compileSolidity.py # 编译合约，需要开梯子并且大概1分钟

```
打开一个新的终端开启ganache-cli，开启区块链服务，不要中断
```shell
cd decert-backend
ganache-cli
```
再打开一个新的终端运行后端程序
```shell
cd decert-backend
python app.py
```
### 前端
打开一个新的终端安装并运行前端
```shell
cd ca-frontend
npm install
npm run serve
```

# 代码文件说明

## decert-backend 后端代码说明

### `app.py`

这是主要的 Flask 应用程序文件。它包含了各种端点来处理用户注册、登录、DID 和 VC 的生成与验证等功能。

- **全局变量**：定义了一些全局变量来保存区块链连接、合约地址、用户状态等信息。
- **函数 `deploy`**：部署智能合约到区块链上。
- **函数 `check_file`**：检查文件是否存在并读取其内容。
- **函数 `init_func`**：初始化函数，连接到以太坊节点，读取 ABI 和字节码，获取第一个可用地址，部署合约并初始化 SQLite 数据库。
- **路由 `/checkUserName`**：检查用户名是否在线。
- **路由 `/register`**：处理用户注册逻辑。
- **路由 `/get_holder_info`**：获取持有者的信息。
- **路由 `/login`**：处理用户登录逻辑。
- **路由 `/requestAuthenticateDID`**：持有者请求认证 DID。
- **路由 `/holderRequestVC`**：持有者返回已有的 VC 给前端。
- **路由 `/getBeAskedVPList`**：持有者返回 VP 请求列表给前端。
- **路由 `/holderToVerifier`**：持有者生成 VP 并发送给验证者。
- **路由 `/recVerifyRequest`**：持有者接收验证者的 VP 请求并存入数据库。
- **路由 `/getVP`**：验证者接收 VP。
- **路由 `/checkVP`**：验证者检查 VP。
- **路由 `/verifyVP`**：验证者验证 VP。
- **路由 `/askHolder`**：验证者向持有者发送验证请求。
- **路由 `/recDID`**：颁发者接收 DID。
- **路由 `/getWhoRequestVerifyDID`**：颁发者将 DID 发送给前端。
- **路由 `/requestVerifyDID`**：颁发者验证 DID。
- **路由 `/giveVCToHolder`**：颁发者颁发 VC 给持有者。

### `sqlite.py`

这个文件用于初始化 SQLite 数据库和表。

- **函数 `init_db`**：创建必要的数据库表，包括 `Holder`, `key`, `VC`, `AskedVP`。
- **函数 `init_sqlite`**：调用 `init_db` 函数来初始化数据库。

### `web3src` 目录

这个目录包含了与区块链交互的辅助脚本。

#### `compileSolidity.py`

- **功能**：编译 Solidity 智能合约并生成 ABI 和字节码文件。

#### `generate_key.py`

- **功能**：生成 RSA 或 SM2 密钥对并序列化为 PEM 格式。

#### `generate_vc.py`

- **功能**：生成可验证凭证（VC）并对其进行签名。

#### `generate_vp.py`

- **功能**：生成可验证呈现（VP）并对其进行签名。

#### `get_signature.py`

- **功能**：从私钥生成数字签名。

#### `interact_with_contract.py`

- **功能**：与智能合约交互，包括生成 DID、获取 DID 文档以及添加证明信息。

#### `tuple_to_json.py`

- **功能**：将从智能合约返回的元组数据转换为 JSON 格式。

#### `verify_did.py`

- **功能**：验证 DID 的真实性。

#### `verify_vc.py`

- **功能**：验证可验证凭证（VC）的真实性。

#### `verify_vp.py`

- **功能**：验证可验证呈现（VP）的真实性。

## decert-frontend 前端代码说明

### 1. 项目概述

DeCert 是一个基于区块链的去中心化证书管理系统。它提供了证书的申请、发放、验证等功能,支持持有者、颁发者和验证者三种角色。

项目使用 Vue 3 作为主要框架,结合 Vue Router 进行页面路由,Vuex 进行状态管理。此外还使用了 Element Plus 组件库来快速搭建页面 UI。

项目采用模块化的结构,将不同的功能和页面划分为独立的组件和模块。`src` 目录是主要的代码目录。

### 2. 目录结构说明

- `access`：权限控制相关的代码
  - `accessEnum.ts`：定义了权限相关的枚举
  - `checkAccess.ts`：检查用户权限的函数
- `assets`：存放静态资源,如图片、CSS 等
- `components`：通用组件
  - `GlobalHeader.vue`：全局页头组件
- `config`：配置文件
  - `api.ts`：API 接口的 URL 配置
- `layouts`：布局组件
  - `BasicLayout.vue`：基本布局组件
  - `SimpleLayout.vue`：简单布局组件
- `router`：路由相关的代码
  - `index.ts`：路由器初始化
  - `routes.ts`：路由配置
- `store`：状态管理相关的代码
  - `index.ts`：Vuex store 初始化
  - `user.ts`：用户状态模块
- `views`：页面组件
  - `BlockInfoView.vue`：区块链信息页面
  - `HolderView.vue`：持有者页面
  - `HomeView.vue`：首页
  - `IssuerView.vue`：颁发者页面
  - `LoginView.vue`：登录页面
  - `RegisterView.vue`：注册页面
  - `VerifyView.vue`：验证者页面

### 3. 核心组件和功能模块说明

#### 3.1 持有者页面 `HolderView.vue`

这是持有者的主页面,展示了持有者的个人信息、持有的证书列表以及收到的验证请求。

关键功能:
- 获取并展示持有者信息
- 获取并展示持有者的证书列表
- 处理颁发者的验证请求
- 向颁发者申请新的证书

主要方法:
- `getHolderInfo`: 从后端获取持有者信息
- `getVCList`: 从后端获取证书列表
- `getVPRequestList`: 从后端获取验证请求列表
- `handleVPRequest`: 处理验证请求
- `applyVC`: 申请新的证书

#### 3.2 颁发者页面 `IssuerView.vue`

这是颁发者的主页面,用于处理持有者的证书申请并颁发证书。

关键功能:
- 获取并展示收到的证书申请
- 验证持有者的 DID
- 向持有者颁发证书

主要方法:
- `getRequestList`: 从后端获取证书申请列表
- `verifyDID`: 验证持有者的 DID
- `issueVC`: 向持有者颁发证书

#### 3.3 验证者页面 `VerifyView.vue`

这是验证者的主页面,用于向持有者发起证书验证请求并验证收到的证书。

关键功能:
- 向持有者发起证书验证请求
- 接收并验证持有者提供的证书

主要方法:
- `handleRequest`: 发起证书验证请求
- `handleVerify`: 验证收到的证书

### 4. 路由和页面导航

项目使用 Vue Router 进行页面路由和导航。路由配置在 `src/router/routes.ts` 文件中定义。每个路由映射到一个特定的页面组件。

`src/router/index.ts` 文件初始化路由器并导出供 `main.ts` 使用。

`src/App.vue` 文件中使用 `<router-view>` 组件作为路由出口,根据当前路由动态渲染对应的页面组件。

此外,`src/access/accessEnum.ts` 定义了页面访问权限枚举,`src/access/checkAccess.ts` 提供了检查用户权限的函数。在路由定义中可以设置 `meta.access` 属性来控制页面的访问权限。

### 5. 状态管理

项目使用 Vuex 进行全局状态管理。Vuex store 在 `src/store/index.ts` 文件中初始化。

目前项目中主要有一个用户状态模块,定义在 `src/store/user.ts` 文件中。这个模块管理了登录用户的信息。

在组件中可以使用 `useStore` 函数来获取 store 实例,然后通过 `store.state` 访问状态,通过 `store.dispatch` 调用 actions。

### 6. 网络请求和 API 交互

项目使用原生的 `fetch` 函数进行网络请求。API 的 URL 配置在 `src/config/api.ts` 文件中定义。

主要的 API 包括:
- `/register`: 用户注册
- `/login`: 用户登录
- `/get_holder_info`: 获取持有者信息
- `/holderRequestVC`: 持有者请求证书
- `/getBeAskedVPList`: 获取持有者收到的验证请求
- `/holderToVerifier`: 持有者向验证者提供证书
- `/askHolder`: 验证者向持有者发起验证请求
- `/getWhoRequestVerifyDID`: 颁发者获取收到的 DID 验证请求
- `/reqeustVerifyDID`: 颁发者验证持有者的 DID
- `/giveVCToHolder`: 颁发者向持有者颁发证书

### 7. 其他说明

- 项目使用 TypeScript 进行静态类型检查,主要的组件和函数都有详细的类型定义。
- 项目使用 Element Plus 组件库快速搭建页面 UI。页面中大量使用了 Element Plus 提供的组件,如卡片、表格、表单、对话框等。
- 项目的 CSS 样式主要以内联的方式写在 Vue 单文件组件中。
- 项目中的部分工具函数(如时间格式化)没有详细说明,可以自行阅读源码了解其作用。

以上就是 DeCert 前端代码的详细说明。如果还有任何疑问,欢迎随时交流探讨。

好的,我来帮你思考如何写前端代码说明,然后再详细写出前端代码说明。

前端代码说明的结构可以按照以下方式组织:

1. 项目概述
   - 项目的基本功能和特点
   - 使用的主要技术栈
   - 项目的整体结构

2. 目录结构说明
   - 列出项目的主要目录及其作用
   - 重点说明 `src` 目录下的子目录及其功能

3. 核心组件和功能模块说明
   - 按照功能模块或者页面组件,依次说明其作用、涉及的主要文件、实现的关键逻辑
   - 可以结合代码片段进行解释

4. 路由和页面导航
   - 说明项目的路由配置文件及其作用
   - 介绍项目的页面导航逻辑和权限控制

5. 状态管理
   - 说明项目使用的状态管理库及其配置
   - 介绍项目的全局状态和模块状态

6. 网络请求和 API 交互
   - 说明项目的网络请求库的配置和封装
   - 列出项目涉及的主要 API 接口及其作用

7. 其他重要功能或库的说明
   - 如果项目中使用了其他重要的功能或第三方库,可以在这里进行说明

下面我将根据这个结构,详细写出你的前端代码说明:

## DeCert 前端代码说明

### 1. 项目概述

DeCert 是一个基于区块链的去中心化证书管理系统。它提供了证书的申请、发放、验证等功能,支持持有者、颁发者和验证者三种角色。

项目使用 Vue 3 作为主要框架,结合 Vue Router 进行页面路由,Vuex 进行状态管理。此外还使用了 Element Plus 组件库来快速搭建页面 UI。

项目采用模块化的结构,将不同的功能和页面划分为独立的组件和模块。`src` 目录是主要的代码目录。

### 2. 目录结构说明

- `access`：权限控制相关的代码
  - `accessEnum.ts`：定义了权限相关的枚举
  - `checkAccess.ts`：检查用户权限的函数
- `assets`：存放静态资源,如图片、CSS 等
- `components`：通用组件
  - `GlobalHeader.vue`：全局页头组件
- `config`：配置文件
  - `api.ts`：API 接口的 URL 配置
- `layouts`：布局组件
  - `BasicLayout.vue`：基本布局组件
  - `SimpleLayout.vue`：简单布局组件
- `router`：路由相关的代码
  - `index.ts`：路由器初始化
  - `routes.ts`：路由配置
- `store`：状态管理相关的代码
  - `index.ts`：Vuex store 初始化
  - `user.ts`：用户状态模块
- `views`：页面组件
  - `BlockInfoView.vue`：区块链信息页面
  - `HolderView.vue`：持有者页面
  - `HomeView.vue`：首页
  - `IssuerView.vue`：颁发者页面
  - `LoginView.vue`：登录页面
  - `RegisterView.vue`：注册页面
  - `VerifyView.vue`：验证者页面

### 3. 核心组件和功能模块说明

#### 3.1 持有者页面 `HolderView.vue`

这是持有者的主页面,展示了持有者的个人信息、持有的证书列表以及收到的验证请求。

关键功能:
- 获取并展示持有者信息
- 获取并展示持有者的证书列表
- 处理颁发者的验证请求
- 向颁发者申请新的证书

主要方法:
- `getHolderInfo`: 从后端获取持有者信息
- `getVCList`: 从后端获取证书列表
- `getVPRequestList`: 从后端获取验证请求列表
- `handleVPRequest`: 处理验证请求
- `applyVC`: 申请新的证书

#### 3.2 颁发者页面 `IssuerView.vue`

这是颁发者的主页面,用于处理持有者的证书申请并颁发证书。

关键功能:
- 获取并展示收到的证书申请
- 验证持有者的 DID
- 向持有者颁发证书

主要方法:
- `getRequestList`: 从后端获取证书申请列表
- `verifyDID`: 验证持有者的 DID
- `issueVC`: 向持有者颁发证书

#### 3.3 验证者页面 `VerifyView.vue`

这是验证者的主页面,用于向持有者发起证书验证请求并验证收到的证书。

关键功能:
- 向持有者发起证书验证请求
- 接收并验证持有者提供的证书

主要方法:
- `handleRequest`: 发起证书验证请求
- `handleVerify`: 验证收到的证书

### 4. 路由和页面导航

项目使用 Vue Router 进行页面路由和导航。路由配置在 `src/router/routes.ts` 文件中定义。每个路由映射到一个特定的页面组件。

`src/router/index.ts` 文件初始化路由器并导出供 `main.ts` 使用。

`src/App.vue` 文件中使用 `<router-view>` 组件作为路由出口,根据当前路由动态渲染对应的页面组件。

此外,`src/access/accessEnum.ts` 定义了页面访问权限枚举,`src/access/checkAccess.ts` 提供了检查用户权限的函数。在路由定义中可以设置 `meta.access` 属性来控制页面的访问权限。

### 5. 状态管理

项目使用 Vuex 进行全局状态管理。Vuex store 在 `src/store/index.ts` 文件中初始化。

目前项目中主要有一个用户状态模块,定义在 `src/store/user.ts` 文件中。这个模块管理了登录用户的信息。

在组件中可以使用 `useStore` 函数来获取 store 实例,然后通过 `store.state` 访问状态,通过 `store.dispatch` 调用 actions。

### 6. 网络请求和 API 交互

项目使用原生的 `fetch` 函数进行网络请求。API 的 URL 配置在 `src/config/api.ts` 文件中定义。

主要的 API 包括:
- `/register`: 用户注册
- `/login`: 用户登录
- `/get_holder_info`: 获取持有者信息
- `/holderRequestVC`: 持有者请求证书
- `/getBeAskedVPList`: 获取持有者收到的验证请求
- `/holderToVerifier`: 持有者向验证者提供证书
- `/askHolder`: 验证者向持有者发起验证请求
- `/getWhoRequestVerifyDID`: 颁发者获取收到的 DID 验证请求
- `/reqeustVerifyDID`: 颁发者验证持有者的 DID
- `/giveVCToHolder`: 颁发者向持有者颁发证书

### 7. 其他说明

- 项目使用 TypeScript 进行静态类型检查,主要的组件和函数都有详细的类型定义。
- 项目使用 Element Plus 组件库快速搭建页面 UI。页面中大量使用了 Element Plus 提供的组件,如卡片、表格、表单、对话框等。
- 项目的 CSS 样式主要以内联的方式写在 Vue 单文件组件中。

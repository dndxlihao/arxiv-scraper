# ArxivPaperAssistant - iOS App

## 项目结构

```
ArxivPaperAssistant/
├── ArxivPaperAssistant.xcodeproj/     # Xcode项目文件
├── ArxivPaperAssistant/               # 主应用目录
│   ├── App/                          # 应用入口和配置
│   │   ├── ArxivPaperAssistantApp.swift
│   │   ├── AppDelegate.swift
│   │   └── SceneDelegate.swift
│   ├── Models/                       # 数据模型
│   │   ├── User.swift
│   │   ├── Paper.swift
│   │   ├── Notification.swift
│   │   └── Team.swift
│   ├── Views/                        # 视图组件
│   │   ├── Auth/                     # 认证相关视图
│   │   │   ├── LoginView.swift
│   │   │   ├── RegisterView.swift
│   │   │   └── ForgotPasswordView.swift
│   │   ├── Main/                     # 主界面视图
│   │   │   ├── HomeView.swift
│   │   │   ├── PaperListView.swift
│   │   │   ├── PaperDetailView.swift
│   │   │   └── SettingsView.swift
│   │   ├── Team/                     # 团队相关视图
│   │   │   ├── TeamListView.swift
│   │   │   ├── TeamDetailView.swift
│   │   │   └── CreateTeamView.swift
│   │   └── Components/               # 可复用组件
│   │       ├── PaperCard.swift
│   │       ├── LoadingView.swift
│   │       ├── ErrorView.swift
│   │       └── EmptyStateView.swift
│   ├── ViewModels/                   # 视图模型
│   │   ├── AuthViewModel.swift
│   │   ├── PaperViewModel.swift
│   │   ├── NotificationViewModel.swift
│   │   └── TeamViewModel.swift
│   ├── Services/                     # 网络服务
│   │   ├── APIService.swift
│   │   ├── AuthService.swift
│   │   ├── PaperService.swift
│   │   └── NotificationService.swift
│   ├── Utils/                        # 工具类
│   │   ├── Constants.swift
│   │   ├── Extensions.swift
│   │   ├── KeychainManager.swift
│   │   └── LocalStorage.swift
│   └── Resources/                    # 资源文件
│       ├── Assets.xcassets/          # 图片资源
│       ├── LaunchScreen.storyboard   # 启动屏幕
│       └── Info.plist                # 应用配置
├── ArxivPaperAssistantTests/         # 单元测试
│   ├── ModelsTests.swift
│   ├── ViewModelsTests.swift
│   └── ServicesTests.swift
└── ArxivPaperAssistantUITests/       # UI测试
    ├── AuthUITests.swift
    ├── PaperUITests.swift
    └── TeamUITests.swift
```

## 开发环境要求

- **Xcode**: 15.0+
- **iOS**: 17.0+
- **Swift**: 5.9+
- **macOS**: 14.0+

## 依赖管理

使用 Swift Package Manager (SPM) 管理依赖：

### 必需依赖
1. **Alamofire** - 网络请求
2. **KeychainAccess** - 安全存储
3. **SwiftUI** - 界面框架 (系统自带)

### 可选依赖
1. **Firebase** - 推送和分析 (如果需要)
2. **Realm** - 本地数据库 (如果需要复杂查询)
3. **Kingfisher** - 图片加载 (如果需要显示作者头像)

## 配置步骤

### 1. 创建Xcode项目
1. 打开Xcode，选择 "Create New Project"
2. 选择 "App" 模板
3. 填写项目信息：
   - Product Name: `ArxivPaperAssistant`
   - Organization Identifier: `com.yourcompany`
   - Interface: `SwiftUI`
   - Language: `Swift`
   - Storage: `None` (我们使用Core Data单独管理)

### 2. 配置项目设置
1. 设置最低iOS版本为 17.0
2. 启用后台模式：
   - Background fetch
   - Remote notifications
3. 配置权限：
   - 添加推送通知权限
   - 添加网络访问权限

### 3. 添加依赖
在Xcode中：
1. File → Add Packages
2. 添加以下包：
   - Alamofire: `https://github.com/Alamofire/Alamofire.git`
   - KeychainAccess: `https://github.com/kishikawakatsumi/KeychainAccess.git`

## 开发流程

### 1. 设置开发环境
```bash
# 克隆项目
git clone <repository-url>
cd arxiv_mobile_app/ios

# 打开项目
open ArxivPaperAssistant.xcodeproj
```

### 2. 配置环境变量
创建 `.env` 文件：
```env
API_BASE_URL=http://localhost:8000
DEBUG=true
```

### 3. 运行项目
1. 选择模拟器或真机
2. 点击运行按钮 (⌘R)

## 代码规范

### 命名约定
- 类名：大驼峰 `PaperDetailView`
- 变量名：小驼峰 `paperList`
- 常量名：全大写 `API_BASE_URL`
- 文件扩展名：`.swift`

### 代码结构
```swift
// 1. 导入模块
import SwiftUI
import Alamofire

// 2. 定义模型
struct Paper: Codable, Identifiable {
    let id: String
    let title: String
    let authors: [String]
    let abstract: String
}

// 3. 定义视图
struct PaperListView: View {
    @StateObject private var viewModel = PaperViewModel()
    
    var body: some View {
        List(viewModel.papers) { paper in
            PaperCard(paper: paper)
        }
        .onAppear {
            viewModel.fetchPapers()
        }
    }
}

// 4. 定义视图模型
@MainActor
class PaperViewModel: ObservableObject {
    @Published var papers: [Paper] = []
    @Published var isLoading = false
    @Published var error: Error?
    
    private let service = PaperService()
    
    func fetchPapers() {
        // 实现获取论文逻辑
    }
}
```

## 测试

### 单元测试
```swift
import XCTest
@testable import ArxivPaperAssistant

class PaperViewModelTests: XCTestCase {
    var viewModel: PaperViewModel!
    
    override func setUp() {
        super.setUp()
        viewModel = PaperViewModel()
    }
    
    func testFetchPapers() async {
        // 测试获取论文功能
    }
}
```

### UI测试
```swift
import XCTest

class AuthUITests: XCTestCase {
    var app: XCUIApplication!
    
    override func setUp() {
        super.setUp()
        app = XCUIApplication()
        app.launch()
    }
    
    func testLoginFlow() {
        // 测试登录流程
    }
}
```

## 部署

### 1. 测试版本
1. 配置开发证书
2. 使用TestFlight分发
3. 收集测试反馈

### 2. 生产版本
1. 配置生产证书
2. 提交App Store审核
3. 监控崩溃和性能

## 故障排除

### 常见问题

**Q: 无法连接到后端API**
A: 检查网络配置和CORS设置

**Q: 推送通知不工作**
A: 检查证书配置和权限设置

**Q: 应用崩溃**
A: 检查崩溃日志，使用Xcode调试器

**Q: 内存泄漏**
A: 使用Instruments检查内存使用

## 下一步

1. 创建Xcode项目
2. 实现用户认证
3. 实现论文列表
4. 实现推送通知
5. 测试和优化
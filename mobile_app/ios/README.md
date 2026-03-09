# arXiv论文助手 - iOS项目

## 项目结构

```
ArxivReader/
├── ArxivReader.xcodeproj
├── ArxivReader/
│   ├── App/
│   │   ├── ArxivReaderApp.swift      # 主应用入口
│   │   └── AppDelegate.swift         # 应用委托
│   ├── Models/                       # 数据模型
│   │   ├── User.swift
│   │   ├── Paper.swift
│   │   ├── Team.swift
│   │   └── Notification.swift
│   ├── Views/                        # 视图层
│   │   ├── Auth/
│   │   │   ├── LoginView.swift
│   │   │   └── RegisterView.swift
│   │   ├── Home/
│   │   │   ├── PaperListView.swift
│   │   │   └── PaperDetailView.swift
│   │   ├── Team/
│   │   │   ├── TeamListView.swift
│   │   │   └── TeamDetailView.swift
│   │   └── Settings/
│   │       └── SettingsView.swift
│   ├── ViewModels/                   # 视图模型
│   │   ├── AuthViewModel.swift
│   │   ├── PaperViewModel.swift
│   │   └── TeamViewModel.swift
│   ├── Services/                     # 服务层
│   │   ├── APIService.swift
│   │   ├── AuthService.swift
│   │   ├── PaperService.swift
│   │   └── NotificationService.swift
│   ├── Utils/                        # 工具类
│   │   ├── Constants.swift
│   │   ├── Extensions.swift
│   │   └── NetworkMonitor.swift
│   └── Resources/                    # 资源文件
│       ├── Assets.xcassets
│       └── Info.plist
└── Tests/                           # 测试文件
    ├── ArxivReaderTests/
    └── ArxivReaderUITests/
```

## 开发环境要求

- **Xcode**: 15.0+
- **iOS**: 16.0+
- **Swift**: 5.9+
- **macOS**: 13.0+

## 安装依赖

项目使用Swift Package Manager管理依赖：

```swift
// Package.swift
dependencies: [
    .package(url: "https://github.com/Alamofire/Alamofire.git", from: "5.8.0"),
    .package(url: "https://github.com/SwiftyJSON/SwiftyJSON.git", from: "5.0.0"),
    .package(url: "https://github.com/onevcat/Kingfisher.git", from: "7.0.0")
]
```

## 配置步骤

1. **创建Xcode项目**
   - 打开Xcode → Create New Project
   - 选择 iOS → App
   - 模板: SwiftUI
   - 名称: ArxivReader
   - 界面: SwiftUI
   - 语言: Swift
   - 存储: 选择项目目录

2. **配置推送通知**
   - 在Xcode中打开项目
   - 选择项目 → Signing & Capabilities
   - 点击 + Capability → Push Notifications
   - 配置Apple Developer证书

3. **配置后端API地址**
   ```swift
   // Constants.swift
   enum API {
       static let baseURL = "https://api.yourdomain.com"
       static let version = "v1"
   }
   ```

## 开发流程

### 第一步：创建基础模型
```swift
// Models/Paper.swift
struct Paper: Identifiable, Codable {
    let id: String
    let title: String
    let authors: [String]
    let abstract: String
    let categories: [String]
    let publishedDate: Date
    let pdfURL: URL?
}
```

### 第二步：实现网络服务
```swift
// Services/APIService.swift
class APIService {
    static let shared = APIService()
    
    func fetchPapers(for query: String) async throws -> [Paper] {
        // 实现API调用
    }
}
```

### 第三步：创建视图
```swift
// Views/Home/PaperListView.swift
struct PaperListView: View {
    @StateObject private var viewModel = PaperViewModel()
    
    var body: some View {
        List(viewModel.papers) { paper in
            PaperRow(paper: paper)
        }
        .task {
            await viewModel.loadPapers()
        }
    }
}
```

### 第四步：添加视图模型
```swift
// ViewModels/PaperViewModel.swift
@MainActor
class PaperViewModel: ObservableObject {
    @Published var papers: [Paper] = []
    
    func loadPapers() async {
        do {
            papers = try await APIService.shared.fetchPapers(for: "machine learning")
        } catch {
            print("Error loading papers: \(error)")
        }
    }
}
```

## 测试

### 单元测试
```swift
// Tests/ArxivReaderTests/PaperTests.swift
class PaperTests: XCTestCase {
    func testPaperDecoding() throws {
        // 测试JSON解码
    }
}
```

### UI测试
```swift
// Tests/ArxivReaderUITests/LoginUITests.swift
class LoginUITests: XCTestCase {
    func testLoginFlow() throws {
        // 测试登录流程
    }
}
```

## 构建和运行

1. 打开 `ArxivReader.xcodeproj`
2. 选择模拟器或连接真机
3. 点击 Run (⌘R)

## 下一步

1. 实现用户认证
2. 集成推送通知
3. 添加离线缓存
4. 优化性能

---

**开始开发时间**: 2026-03-09
import SwiftUI

struct ContentView: View {
    @EnvironmentObject var paperManager: PaperManager
    @EnvironmentObject var userSettings: UserSettings
    @State private var searchText = ""
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            // 搜索标签页
            NavigationView {
                SearchView(searchText: $searchText)
                    .navigationTitle("搜索论文")
                    .searchable(text: $searchText, prompt: "搜索论文标题、作者或关键词")
            }
            .tabItem {
                Label("搜索", systemImage: "magnifyingglass")
            }
            .tag(0)
            
            // 收藏标签页
            NavigationView {
                FavoritesView()
                    .navigationTitle("我的收藏")
            }
            .tabItem {
                Label("收藏", systemImage: "star.fill")
            }
            .tag(1)
            
            // 阅读列表标签页
            NavigationView {
                ReadingListView()
                    .navigationTitle("阅读列表")
            }
            .tabItem {
                Label("阅读列表", systemImage: "list.bullet")
            }
            .tag(2)
            
            // 设置标签页
            NavigationView {
                SettingsView()
                    .navigationTitle("设置")
            }
            .tabItem {
                Label("设置", systemImage: "gear")
            }
            .tag(3)
        }
        .accentColor(.blue)
    }
}

struct SearchView: View {
    @Binding var searchText: String
    @EnvironmentObject var paperManager: PaperManager
    @State private var searchResults: [Paper] = []
    @State private var isSearching = false
    
    var body: some View {
        List(searchResults) { paper in
            PaperRow(paper: paper)
                .swipeActions(edge: .trailing) {
                    Button {
                        paperManager.addToFavorites(paper)
                    } label: {
                        Label("收藏", systemImage: "star")
                    }
                    .tint(.yellow)
                    
                    Button {
                        paperManager.addToReadingList(paper)
                    } label: {
                        Label("稍后读", systemImage: "bookmark")
                    }
                    .tint(.blue)
                }
        }
        .overlay {
            if isSearching {
                ProgressView("搜索中...")
            } else if searchResults.isEmpty && !searchText.isEmpty {
                ContentUnavailableView.search(text: searchText)
            }
        }
        .onChange(of: searchText) { newValue in
            Task {
                await performSearch(query: newValue)
            }
        }
    }
    
    private func performSearch(query: String) async {
        guard !query.isEmpty else {
            searchResults = []
            return
        }
        
        isSearching = true
        defer { isSearching = false }
        
        do {
            searchResults = try await paperManager.searchPapers(query: query)
        } catch {
            print("搜索失败: \(error)")
        }
    }
}

struct FavoritesView: View {
    @EnvironmentObject var paperManager: PaperManager
    
    var body: some View {
        List(paperManager.favorites) { paper in
            PaperRow(paper: paper)
        }
        .overlay {
            if paperManager.favorites.isEmpty {
                ContentUnavailableView(
                    "暂无收藏",
                    systemImage: "star",
                    description: Text("将论文添加到收藏夹后，它们会显示在这里")
                )
            }
        }
    }
}

struct ReadingListView: View {
    @EnvironmentObject var paperManager: PaperManager
    
    var body: some View {
        List(paperManager.readingList) { paper in
            PaperRow(paper: paper)
        }
        .overlay {
            if paperManager.readingList.isEmpty {
                ContentUnavailableView(
                    "阅读列表为空",
                    systemImage: "book",
                    description: Text("将论文添加到阅读列表后，它们会显示在这里")
                )
            }
        }
    }
}

struct SettingsView: View {
    @EnvironmentObject var userSettings: UserSettings
    
    var body: some View {
        Form {
            Section("外观") {
                Toggle("深色模式", isOn: $userSettings.isDarkMode)
            }
            
            Section("通知") {
                Toggle("新论文提醒", isOn: $userSettings.notificationEnabled)
            }
            
            Section("关于") {
                HStack {
                    Text("版本")
                    Spacer()
                    Text("1.0.0")
                        .foregroundColor(.secondary)
                }
                
                Link("隐私政策", destination: URL(string: "https://paperflow.app/privacy")!)
                Link("使用条款", destination: URL(string: "https://paperflow.app/terms")!)
            }
        }
    }
}

struct PaperRow: View {
    let paper: Paper
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(paper.title)
                .font(.headline)
                .lineLimit(2)
            
            Text(paper.formattedAuthors)
                .font(.subheadline)
                .foregroundColor(.secondary)
                .lineLimit(1)
            
            Text(paper.abstract)
                .font(.caption)
                .foregroundColor(.secondary)
                .lineLimit(3)
            
            HStack {
                ForEach(paper.categories.prefix(3), id: \.self) { category in
                    Text(category)
                        .font(.caption2)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(Color.blue.opacity(0.1))
                        .cornerRadius(4)
                }
                
                Spacer()
                
                Text(paper.formattedDate)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
}

#Preview {
    ContentView()
        .environmentObject(PaperManager())
        .environmentObject(UserSettings())
}
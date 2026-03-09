//
//  ArxivPaperAssistantApp.swift
//  ArxivPaperAssistant
//
//  Created by Arxiv Paper Assistant Team on 2026/03/09.
//

import SwiftUI

@main
struct ArxivPaperAssistantApp: App {
    @StateObject private var authViewModel = AuthViewModel()
    @StateObject private var appState = AppState()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(authViewModel)
                .environmentObject(appState)
                .onAppear {
                    setupAppearance()
                }
        }
    }
    
    private func setupAppearance() {
        // 设置全局外观
        UITableView.appearance().backgroundColor = .clear
        UINavigationBar.appearance().largeTitleTextAttributes = [
            .foregroundColor: UIColor(Color.primary)
        ]
    }
}

// 应用状态管理
class AppState: ObservableObject {
    @Published var isLoggedIn: Bool = false
    @Published var isLoading: Bool = false
    @Published var selectedTab: Tab = .home
    
    enum Tab {
        case home
        case papers
        case teams
        case notifications
        case profile
    }
}

// 根视图
struct ContentView: View {
    @EnvironmentObject var authViewModel: AuthViewModel
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        Group {
            if appState.isLoading {
                LoadingView()
            } else if authViewModel.isAuthenticated {
                MainTabView()
            } else {
                LoginView()
            }
        }
        .transition(.opacity)
        .animation(.easeInOut(duration: 0.3), value: authViewModel.isAuthenticated)
    }
}

// 加载视图
struct LoadingView: View {
    var body: some View {
        VStack(spacing: 20) {
            ProgressView()
                .scaleEffect(1.5)
            
            Text("加载中...")
                .font(.headline)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Color(.systemBackground))
    }
}

// 主标签页视图
struct MainTabView: View {
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        TabView(selection: $appState.selectedTab) {
            HomeView()
                .tabItem {
                    Label("首页", systemImage: "house.fill")
                }
                .tag(AppState.Tab.home)
            
            PaperListView()
                .tabItem {
                    Label("论文", systemImage: "doc.text.fill")
                }
                .tag(AppState.Tab.papers)
            
            TeamListView()
                .tabItem {
                    Label("团队", systemImage: "person.3.fill")
                }
                .tag(AppState.Tab.teams)
            
            NotificationListView()
                .tabItem {
                    Label("通知", systemImage: "bell.fill")
                }
                .tag(AppState.Tab.notifications)
            
            ProfileView()
                .tabItem {
                    Label("我的", systemImage: "person.fill")
                }
                .tag(AppState.Tab.profile)
        }
        .accentColor(.blue)
    }
}

// 预览
#Preview {
    ContentView()
        .environmentObject(AuthViewModel())
        .environmentObject(AppState())
}
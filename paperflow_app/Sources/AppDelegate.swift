import SwiftUI

@main
struct PaperFlowApp: App {
    @StateObject private var paperManager = PaperManager()
    @StateObject private var userSettings = UserSettings()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(paperManager)
                .environmentObject(userSettings)
                .preferredColorScheme(userSettings.isDarkMode ? .dark : .light)
        }
    }
}

class PaperManager: ObservableObject {
    @Published var papers: [Paper] = []
    @Published var favorites: [Paper] = []
    @Published var readingList: [Paper] = []
    
    func searchPapers(query: String) async throws -> [Paper] {
        // 这里会调用后端 API 搜索论文
        return []
    }
    
    func addToFavorites(_ paper: Paper) {
        if !favorites.contains(where: { $0.id == paper.id }) {
            favorites.append(paper)
        }
    }
    
    func addToReadingList(_ paper: Paper) {
        if !readingList.contains(where: { $0.id == paper.id }) {
            readingList.append(paper)
        }
    }
}

class UserSettings: ObservableObject {
    @Published var isDarkMode: Bool = false
    @Published var preferredCategories: [String] = ["cs.AI", "cs.LG", "cs.CV"]
    @Published var notificationEnabled: Bool = true
}

struct Paper: Identifiable, Codable {
    let id: String
    let title: String
    let authors: [String]
    let abstract: String
    let categories: [String]
    let publishedDate: Date
    let pdfURL: URL?
    let arxivURL: URL
    
    var formattedAuthors: String {
        authors.joined(separator: ", ")
    }
    
    var formattedDate: String {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        formatter.timeStyle = .none
        return formatter.string(from: publishedDate)
    }
}
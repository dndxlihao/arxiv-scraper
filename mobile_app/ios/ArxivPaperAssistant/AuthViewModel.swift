//
//  AuthViewModel.swift
//  ArxivPaperAssistant
//
//  Created by Arxiv Paper Assistant Team on 2026/03/09.
//

import Foundation
import SwiftUI
import KeychainAccess

@MainActor
class AuthViewModel: ObservableObject {
    @Published var isAuthenticated: Bool = false
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?
    @Published var user: User?
    
    private let keychain = Keychain(service: "com.arxivpaperassistant.auth")
    private let authService = AuthService()
    
    init() {
        // 检查本地是否有保存的token
        checkLocalAuth()
    }
    
    private func checkLocalAuth() {
        if let token = keychain["auth_token"], !token.isEmpty {
            // 如果有token，验证是否有效
            validateToken(token)
        }
    }
    
    private func validateToken(_ token: String) {
        Task {
            do {
                let user = try await authService.validateToken(token)
                self.user = user
                self.isAuthenticated = true
                self.errorMessage = nil
            } catch {
                // Token无效，清除本地存储
                await logout()
            }
        }
    }
    
    func login(email: String, password: String) async {
        isLoading = true
        errorMessage = nil
        
        do {
            let result = try await authService.login(email: email, password: password)
            
            // 保存token到Keychain
            try keychain.set(result.token, key: "auth_token")
            try keychain.set(result.user.id, key: "user_id")
            
            // 更新状态
            self.user = result.user
            self.isAuthenticated = true
            self.errorMessage = nil
            
        } catch let error as AuthError {
            errorMessage = error.localizedDescription
        } catch {
            errorMessage = "登录失败，请检查网络连接"
        }
        
        isLoading = false
    }
    
    func register(email: String, password: String, name: String) async {
        isLoading = true
        errorMessage = nil
        
        do {
            let result = try await authService.register(
                email: email,
                password: password,
                name: name
            )
            
            // 保存token到Keychain
            try keychain.set(result.token, key: "auth_token")
            try keychain.set(result.user.id, key: "user_id")
            
            // 更新状态
            self.user = result.user
            self.isAuthenticated = true
            self.errorMessage = nil
            
        } catch let error as AuthError {
            errorMessage = error.localizedDescription
        } catch {
            errorMessage = "注册失败，请检查网络连接"
        }
        
        isLoading = false
    }
    
    func logout() async {
        do {
            if let token = keychain["auth_token"] {
                try await authService.logout(token: token)
            }
        } catch {
            print("登出API调用失败: \(error)")
        }
        
        // 清除本地存储
        try? keychain.remove("auth_token")
        try? keychain.remove("user_id")
        
        // 更新状态
        self.isAuthenticated = false
        self.user = nil
        self.errorMessage = nil
    }
    
    func resetPassword(email: String) async -> Bool {
        isLoading = true
        errorMessage = nil
        
        do {
            try await authService.resetPassword(email: email)
            isLoading = false
            return true
        } catch let error as AuthError {
            errorMessage = error.localizedDescription
            isLoading = false
            return false
        } catch {
            errorMessage = "请求失败，请检查网络连接"
            isLoading = false
            return false
        }
    }
}

// 用户模型
struct User: Codable, Identifiable {
    let id: String
    let email: String
    let name: String
    let interests: [String]
    let createdAt: Date
    let updatedAt: Date
    
    enum CodingKeys: String, CodingKey {
        case id
        case email
        case name
        case interests
        case createdAt = "created_at"
        case updatedAt = "updated_at"
    }
}

// 认证响应
struct AuthResponse: Codable {
    let user: User
    let token: String
}

// 认证错误
enum AuthError: Error, LocalizedError {
    case invalidCredentials
    case emailAlreadyExists
    case weakPassword
    case networkError
    case serverError
    
    var errorDescription: String? {
        switch self {
        case .invalidCredentials:
            return "邮箱或密码不正确"
        case .emailAlreadyExists:
            return "该邮箱已被注册"
        case .weakPassword:
            return "密码强度不足，请使用至少8位字符"
        case .networkError:
            return "网络连接失败，请检查网络设置"
        case .serverError:
            return "服务器错误，请稍后重试"
        }
    }
}
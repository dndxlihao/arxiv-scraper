//
//  AuthService.swift
//  ArxivPaperAssistant
//
//  Created by Arxiv Paper Assistant Team on 2026/03/09.
//

import Foundation
import Alamofire

class AuthService {
    private let baseURL = "http://localhost:8000/api"
    
    // MARK: - 登录
    func login(email: String, password: String) async throws -> AuthResponse {
        let parameters: [String: Any] = [
            "email": email,
            "password": password
        ]
        
        return try await performRequest(
            path: "/auth/login",
            method: .post,
            parameters: parameters
        )
    }
    
    // MARK: - 注册
    func register(email: String, password: String, name: String) async throws -> AuthResponse {
        let parameters: [String: Any] = [
            "email": email,
            "password": password,
            "name": name
        ]
        
        return try await performRequest(
            path: "/auth/register",
            method: .post,
            parameters: parameters
        )
    }
    
    // MARK: - 验证Token
    func validateToken(_ token: String) async throws -> User {
        return try await performRequest(
            path: "/auth/me",
            method: .get,
            token: token
        )
    }
    
    // MARK: - 登出
    func logout(token: String) async throws {
        _ = try await performRequest(
            path: "/auth/logout",
            method: .post,
            token: token
        ) as EmptyResponse
    }
    
    // MARK: - 重置密码
    func resetPassword(email: String) async throws {
        let parameters: [String: Any] = [
            "email": email
        ]
        
        _ = try await performRequest(
            path: "/auth/reset-password",
            method: .post,
            parameters: parameters
        ) as EmptyResponse
    }
    
    // MARK: - 通用请求方法
    private func performRequest<T: Decodable>(
        path: String,
        method: HTTPMethod,
        parameters: [String: Any]? = nil,
        token: String? = nil
    ) async throws -> T {
        let url = baseURL + path
        
        var headers: HTTPHeaders = [
            "Accept": "application/json",
            "Content-Type": "application/json"
        ]
        
        if let token = token {
            headers["Authorization"] = "Bearer \(token)"
        }
        
        return try await withCheckedThrowingContinuation { continuation in
            AF.request(
                url,
                method: method,
                parameters: parameters,
                encoding: JSONEncoding.default,
                headers: headers
            )
            .validate()
            .responseDecodable(of: APIResponse<T>.self) { response in
                switch response.result {
                case .success(let apiResponse):
                    if apiResponse.success, let data = apiResponse.data {
                        continuation.resume(returning: data)
                    } else {
                        let errorMessage = apiResponse.message ?? "未知错误"
                        let error = mapError(message: errorMessage)
                        continuation.resume(throwing: error)
                    }
                case .failure(let error):
                    if let data = response.data,
                       let apiResponse = try? JSONDecoder().decode(APIResponse<EmptyData>.self, from: data),
                       let message = apiResponse.message {
                        let mappedError = mapError(message: message)
                        continuation.resume(throwing: mappedError)
                    } else {
                        continuation.resume(throwing: mapAFError(error))
                    }
                }
            }
        }
    }
    
    // MARK: - 错误映射
    private func mapError(message: String) -> AuthError {
        switch message.lowercased() {
        case let msg where msg.contains("invalid credentials") || msg.contains("邮箱或密码"):
            return .invalidCredentials
        case let msg where msg.contains("already exists") || msg.contains("已被注册"):
            return .emailAlreadyExists
        case let msg where msg.contains("weak password") || msg.contains("密码强度"):
            return .weakPassword
        case let msg where msg.contains("network") || msg.contains("连接"):
            return .networkError
        default:
            return .serverError
        }
    }
    
    private func mapAFError(_ error: AFError) -> AuthError {
        if let underlyingError = error.underlyingError as? URLError {
            switch underlyingError.code {
            case .notConnectedToInternet, .networkConnectionLost:
                return .networkError
            default:
                return .serverError
            }
        }
        return .serverError
    }
}

// MARK: - API响应模型
struct APIResponse<T: Decodable>: Decodable {
    let success: Bool
    let data: T?
    let message: String?
}

struct EmptyData: Decodable {}

struct EmptyResponse: Decodable {}

// MARK: - 扩展用于测试
#if DEBUG
extension AuthService {
    static var mock: AuthService {
        let service = AuthService()
        return service
    }
}
#endif
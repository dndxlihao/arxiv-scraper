//
//  LoginView.swift
//  ArxivPaperAssistant
//
//  Created by Arxiv Paper Assistant Team on 2026/03/09.
//

import SwiftUI

struct LoginView: View {
    @EnvironmentObject var authViewModel: AuthViewModel
    @EnvironmentObject var appState: AppState
    @State private var email = ""
    @State private var password = ""
    @State private var showingRegister = false
    @State private var showingResetPassword = false
    @FocusState private var focusedField: Field?
    
    enum Field {
        case email, password
    }
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 30) {
                    // 头部
                    headerView
                    
                    // 表单
                    formView
                    
                    // 登录按钮
                    loginButton
                    
                    // 其他选项
                    otherOptionsView
                    
                    Spacer()
                }
                .padding(.horizontal, 24)
                .padding(.top, 40)
            }
            .background(Color(.systemGroupedBackground))
            .navigationBarHidden(true)
            .sheet(isPresented: $showingRegister) {
                RegisterView()
            }
            .sheet(isPresented: $showingResetPassword) {
                ResetPasswordView()
            }
            .alert("登录失败", isPresented: .constant(authViewModel.errorMessage != nil)) {
                Button("确定") {
                    authViewModel.errorMessage = nil
                }
            } message: {
                Text(authViewModel.errorMessage ?? "")
            }
        }
    }
    
    private var headerView: some View {
        VStack(spacing: 16) {
            Image(systemName: "doc.text.magnifyingglass")
                .font(.system(size: 80))
                .foregroundColor(.blue)
                .padding(.bottom, 8)
            
            Text("arXiv论文助手")
                .font(.largeTitle)
                .fontWeight(.bold)
                .foregroundColor(.primary)
            
            Text("发现最新研究，智能推送通知")
                .font(.subheadline)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
        }
    }
    
    private var formView: some View {
        VStack(spacing: 20) {
            // 邮箱输入
            VStack(alignment: .leading, spacing: 8) {
                Text("邮箱")
                    .font(.caption)
                    .foregroundColor(.secondary)
                
                TextField("请输入邮箱", text: $email)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .keyboardType(.emailAddress)
                    .autocapitalization(.none)
                    .disableAutocorrection(true)
                    .focused($focusedField, equals: .email)
                    .submitLabel(.next)
                    .onSubmit {
                        focusedField = .password
                    }
            }
            
            // 密码输入
            VStack(alignment: .leading, spacing: 8) {
                Text("密码")
                    .font(.caption)
                    .foregroundColor(.secondary)
                
                SecureField("请输入密码", text: $password)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .focused($focusedField, equals: .password)
                    .submitLabel(.go)
                    .onSubmit {
                        Task {
                            await performLogin()
                        }
                    }
            }
        }
    }
    
    private var loginButton: some View {
        Button(action: {
            Task {
                await performLogin()
            }
        }) {
            if authViewModel.isLoading {
                ProgressView()
                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                    .frame(maxWidth: .infinity)
                    .frame(height: 50)
            } else {
                Text("登录")
                    .font(.headline)
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .frame(height: 50)
            }
        }
        .background(Color.blue)
        .cornerRadius(12)
        .disabled(authViewModel.isLoading || email.isEmpty || password.isEmpty)
        .opacity((authViewModel.isLoading || email.isEmpty || password.isEmpty) ? 0.6 : 1)
    }
    
    private var otherOptionsView: some View {
        VStack(spacing: 16) {
            // 忘记密码
            Button("忘记密码？") {
                showingResetPassword = true
            }
            .font(.footnote)
            .foregroundColor(.blue)
            
            Divider()
                .padding(.horizontal, 20)
            
            // 注册
            HStack {
                Text("还没有账号？")
                    .font(.footnote)
                    .foregroundColor(.secondary)
                
                Button("立即注册") {
                    showingRegister = true
                }
                .font(.footnote)
                .fontWeight(.semibold)
                .foregroundColor(.blue)
            }
        }
    }
    
    private func performLogin() async {
        focusedField = nil
        await authViewModel.login(email: email, password: password)
    }
}

// 注册视图
struct RegisterView: View {
    @Environment(\.dismiss) var dismiss
    @EnvironmentObject var authViewModel: AuthViewModel
    @State private var email = ""
    @State private var password = ""
    @State private var confirmPassword = ""
    @State private var name = ""
    @FocusState private var focusedField: RegisterField?
    
    enum RegisterField {
        case name, email, password, confirmPassword
    }
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("基本信息")) {
                    TextField("姓名", text: $name)
                        .focused($focusedField, equals: .name)
                        .submitLabel(.next)
                    
                    TextField("邮箱", text: $email)
                        .keyboardType(.emailAddress)
                        .autocapitalization(.none)
                        .disableAutocorrection(true)
                        .focused($focusedField, equals: .email)
                        .submitLabel(.next)
                }
                
                Section(header: Text("密码")) {
                    SecureField("密码", text: $password)
                        .focused($focusedField, equals: .password)
                        .submitLabel(.next)
                    
                    SecureField("确认密码", text: $confirmPassword)
                        .focused($focusedField, equals: .confirmPassword)
                        .submitLabel(.done)
                }
                
                Section {
                    Button(action: {
                        Task {
                            await performRegister()
                        }
                    }) {
                        if authViewModel.isLoading {
                            HStack {
                                Spacer()
                                ProgressView()
                                Spacer()
                            }
                        } else {
                            Text("注册")
                                .frame(maxWidth: .infinity)
                        }
                    }
                    .disabled(!isFormValid || authViewModel.isLoading)
                }
            }
            .navigationTitle("注册")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("取消") {
                        dismiss()
                    }
                }
            }
            .alert("注册失败", isPresented: .constant(authViewModel.errorMessage != nil)) {
                Button("确定") {
                    authViewModel.errorMessage = nil
                }
            } message: {
                Text(authViewModel.errorMessage ?? "")
            }
        }
    }
    
    private var isFormValid: Bool {
        !email.isEmpty &&
        !password.isEmpty &&
        !confirmPassword.isEmpty &&
        !name.isEmpty &&
        password == confirmPassword &&
        password.count >= 8
    }
    
    private func performRegister() async {
        await authViewModel.register(email: email, password: password, name: name)
        if authViewModel.isAuthenticated {
            dismiss()
        }
    }
}

// 重置密码视图
struct ResetPasswordView: View {
    @Environment(\.dismiss) var dismiss
    @EnvironmentObject var authViewModel: AuthViewModel
    @State private var email = ""
    @State private var isSubmitted = false
    
    var body: some View {
        NavigationView {
            Form {
                Section(
                    header: Text("请输入注册邮箱"),
                    footer: Text("我们将发送重置密码链接到您的邮箱")
                ) {
                    TextField("邮箱", text: $email)
                        .keyboardType(.emailAddress)
                        .autocapitalization(.none)
                        .disableAutocorrection(true)
                }
                
                if isSubmitted {
                    Section {
                        Text("重置链接已发送，请检查您的邮箱")
                            .foregroundColor(.green)
                            .font(.footnote)
                    }
                }
                
                Section {
                    Button(action: {
                        Task {
                            let success = await authViewModel.resetPassword(email: email)
                            if success {
                                isSubmitted = true
                                DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                                    dismiss()
                                }
                            }
                        }
                    }) {
                        if authViewModel.isLoading {
                            HStack {
                                Spacer()
                                ProgressView()
                                Spacer()
                            }
                        } else {
                            Text("发送重置链接")
                                .frame(maxWidth: .infinity)
                        }
                    }
                    .disabled(email.isEmpty || authViewModel.isLoading)
                }
            }
            .navigationTitle("重置密码")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("取消") {
                        dismiss()
                    }
                }
            }
        }
    }
}

// 预览
#Preview {
    LoginView()
        .environmentObject(AuthViewModel())
        .environmentObject(AppState())
}
//
//  PilotVoiceAssistant.swift
//  PilotVoiceAssistant
//
//  Pilot — AI-assisted reflective memory system for strategic knowledge workers
//  MVP Core: Capture → Transcribe → Summarize → Retrieve
//

import SwiftUI

@main
struct PilotVoiceAssistantApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    @StateObject private var audioManager = AudioManager()
    @StateObject private var viewModel = AppViewModel()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(audioManager)
                .environment(viewModel)
        }
    }
}

// MARK: - App Delegate
class AppDelegate: NSObject, UIApplicationDelegate {
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]? = nil) -> Bool {
        UINavigationBar.appearance().largeTitleTextAttributes = [
            .foregroundColor: UIColor.label
        ]
        return true
    }
}

// MARK: - App ViewModel
class AppViewModel: ObservableObject {
    @Published var currentSession: Session?
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    func startNewSession() {
        currentSession = Session(id: .init(), timestamp: Date())
    }
}

struct Session: Identifiable, Codable {
    let id: UUID
    let timestamp: Date
}

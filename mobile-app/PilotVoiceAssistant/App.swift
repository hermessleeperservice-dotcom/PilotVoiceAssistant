//
//  App.swift
//  PilotVoiceAssistant
//
//  Pilot — AI-assisted reflective memory system
//  MVP Core: Capture → Transcribe → Summarize → Retrieve
//

import SwiftUI

@main
struct PilotVoiceAssistantApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    @StateObject privatevar audioManager = AudioManager()
    @StateObject private var viewModel = AppViewModel()
    
    init() {
        // Per PRD UX Principle 5: Calm interface
        UINavigationBar.appearance().largeTitleTextAttributes = [
            .foregroundColor: UIColor.label
        ]
        UINavigationBar.appearance().titleTextAttributes = [
            .foregroundColor: UIColor.label
        ]
        UITabBar.appearance().barTintColor = .systemBackground
    }
    
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
        // Initialize audio session for background recording
        let session = AVAudioSession.sharedInstance()
        try? session.setCategory(.playback, mode: .default)
        try? session.setActive(true)
        return true
    }
}

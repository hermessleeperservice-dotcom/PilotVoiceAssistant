//
//  ContentView.swift
//  PilotVoiceAssistant
//
//  Per PRD UX: Calm interface, instant capture, one-tap recording
//  MVP Core: Capture → Transcribe → Summarize → Retrieve
//

import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = SessionViewModel()
    @State private var showingSearch = false
    @State private var searchQuery = ""
    
    var body: some View {
        VStack(spacing: 0) {
            // Header
            HStack {
                Text("Pilot")
                    .font(.title2)
                    .fontWeight(.semibold)
                Spacer()
                Button(action: { showingSearch.toggle() }) {
                    Image(systemName: "magnifyingglass")
                        .font(.title3)
                }
            }
            .padding(.horizontal)
            .padding(.vertical, 8)
            
            // Recording button (centered, instant)
            VStack(spacing: 16) {
                RecordButton(
                    isRecording: viewModel.isRecording,
                    duration: viewModel.recordingDuration,
                    onStart: { viewModel.startRecording() },
                    onStop: { viewModel.stopRecording() }
                )
                
                Text(viewModel.statusText)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            .padding(.vertical, 40)
            
            // Waveform (when recording)
            if viewModel.isRecording {
                WaveformView(waveform: viewModel.waveform)
                    .frame(height: 40)
                    .padding(.horizontal, 20)
            }
            
            Spacer()
            
            // Timeline preview
            if !viewModel.reflections.isEmpty {
                VStack(alignment: .leading, spacing: 12) {
                    Text("Recent reflections")
                        .font(.headline)
                        .padding(.horizontal)
                    
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 12) {
                            ForEach(Array(viewModel.reflections.prefix(10)), id: \.id) { reflection in
                                ReflectionCard(reflection: reflection)
                            }
                        }
                        .padding(.horizontal, 16)
                    }
                }
                .padding(.bottom, 20)
            }
            
            // Empty state
            if viewModel.reflections.isEmpty {
                VStack(spacing: 8) {
                    Image(systemName: "waveform")
                        .font(.system(size: 48))
                        .foregroundColor(.gray.opacity(0.3))
                    Text("Your first reflection")
                        .font(.title3)
                        .foregroundColor(.gray)
                    Text("Tap the record button above and speak your thoughts")
                        .font(.caption)
                        .foregroundColor(.gray.opacity(0.6))
                        .multilineTextAlignment(.center)
                        .padding(.horizontal, 40)
                }
                .padding(.vertical, 40)
            }
        }
        .sheet(isPresented: $showingSearch) {
            SearchView()
        }
    }
}

// MARK: - Record Button
struct RecordButton: View {
    let isRecording: Bool
    let duration: TimeInterval
    let onStart: () -> Void
    let onStop: () -> Void
    
    var body: some View {
        VStack(spacing: 8) {
            ZStack {
                // Pulse ring when recording
                if isRecording {
                    Circle()
                        .stroke(Color.red.opacity(0.3), lineWidth: 3)
                        .frame(width: 110, height: 110)
                        .scaleEffect(isRecording ? 1.1 : 1.0)
                        .opacity(isRecording ? 0.6 : 0)
                        .animation(.easeInOut(duration: 1.0).repeatForever(autoreverses: true), value: isRecording)
                }
                
                // Main button
                Button(action: {
                    if isRecording {
                        onStop()
                    } else {
                        onStart()
                    }
                }) {
                    Circle()
                        .fill(isRecording ? Color.red : Color.blue)
                        .frame(width: 80, height: 80)
                        .shadow(color: Color.black.opacity(0.15), radius: 8, y: 4)
                }
            }
            
            if isRecording {
                Text(duration, formatter: recordingFormatter)
                    .font(.title2)
                    .fontWeight(.medium)
                    .monospacedDigit()
            }
        }
    }
}

private let recordingFormatter: DateIntervalFormatter = {
    let formatter = DateIntervalFormatter()
    formatter.dateFormat = "m:ss"
    return formatter
}()

// MARK: - Waveform View
struct WaveformView: View {
    let waveform: [Float]
    
    var body: some View {
        HStack(spacing: 2) {
            ForEach(Array(waveform.enumerated()), id: \.offset) { _, value in
                RoundedRectangle(cornerRadius: 1)
                    .fill(Color.blue.opacity(0.7))
                    .frame(width: 3, height: max(4, CGFloat(value) * 40 + 4))
            }
        }
        .frame(maxWidth: .infinity)
        .animation(.easeInOut(duration: 0.05), value: waveform)
    }
}

// MARK: - Reflection Card
struct ReflectionCard: View {
    let reflection: Reflection
    @State private var isExpanded = false
    
    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(reflection.date, style: .date)
                .font(.caption2)
                .foregroundColor(.secondary)
            
            Text(reflection.summary ?? "No summary yet")
                .font(.body)
                .lineLimit(isExpanded ? nil : 2)
                .onTapGesture { isExpanded.toggle() }
            
            if let duration = reflection.duration {
                Text("\(Int(duration))s")
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }
        }
        .padding()
        .frame(width: 200, height: 120)
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
}

// MARK: - Search View
struct SearchView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var query = ""
    @State private var results: [Reflection] = []
    
    var body: some View {
        NavigationView {
            VStack(spacing: 16) {
                TextField("What did you say about...?", text: $query)
                    .textFieldStyle(.roundedBorder)
                    .padding(.horizontal)
                    .onChange(of: query) { _ in
                        performSearch()
                    }
                
                if !results.isEmpty {
                    List(results) { result in
                        VStack(alignment: .leading, spacing: 4) {
                            Text(result.date, style: .date)
                                .font(.caption2)
                                .foregroundColor(.secondary)
                            Text(result.summary ?? "—")
                                .font(.body)
                                .lineLimit(3)
                        }
                        .padding(.vertical, 4)
                    }
                    .listStyle(.plain)
                    .frame(maxHeight: .infinity)
                }
                
                Spacer()
            }
            .navigationTitle("Search")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }
    
    private func performSearch() {
        // TODO: API call to /api/v1/retrieve
    }
}

// MARK: - ViewModel
@MainActor
class SessionViewModel: ObservableObject {
    @Published var isRecording = false
    @Published var recordingDuration: TimeInterval = 0
    @Published var waveform: [Float] = Array(repeating: 0, count: 30)
    @Published var statusText = "Tap to record"
    @Published var reflections: [Reflection] = []
    
    private var timer: Timer?
    
    func startRecording() {
        isRecording = true
        recordingDuration = 0
        statusText = "Recording..."
        
        timer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { [weak self] _ in
            self?.recordingDuration += 0.1
            // Simulate waveform (in production, feed from mic)
            self?.waveform = self?.waveform.map { _ in Float.random(in: 0.1...1.0) } ?? []
        }
    }
    
    func stopRecording() {
        isRecording = false
        timer?.invalidate()
        timer = nil
        recordingDuration = 0
        waveform = Array(repeating: 0, count: 30)
        statusText = "Processing..."
        
        // TODO: Upload to /api/v1/capture → transcribe → summarize
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
            statusText = "Reflection saved"
            reflections.append(Reflection(
                id: .init(),
                summary: "Simulated reflection",
                date: .now,
                duration: nil
            ))
        }
    }
}

struct Reflection: Identifiable {
    let id: UUID
    let summary: String?
    let date: Date
    let duration: TimeInterval?
}

#Preview {
    ContentView()
}

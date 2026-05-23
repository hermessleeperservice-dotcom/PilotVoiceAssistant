//
//  AudioManager.swift
//  PilotVoiceAssistant
//
//  Handles audio recording per PRD §9 Feature 1
//  Capture must feel instant — <1s

import AVFoundation
import Foundation

@MainActor
class AudioManager: NSObject, ObservableObject {
    enum State: String {
        case idle = "Tap to record"
        case recording = "Recording..."
        case processing = "Processing reflection..."
        case error = "Recording failed"
    }
    
    @Published var state: State = .idle
    @Published var waveform: [Float] = Array(repeating: 0, count: 50)
    @Published var duration: TimeInterval = 0
    
    private var audioEngine: AVAudioEngine?
    private var tap: AVAudioTapNode?
    private var timer: Timer?
    
    var isRecording: Bool { state == .recording }
    
    // MARK: - Recording
    
    func startRecording() {
        state = .recording
        let session = AVAudioSession.sharedInstance()
        
        do {
            try session.setCategory(.playAndRecord, mode: .default, options: .duckOthers)
            try session.setActive(true)
        } catch {
            state = .error
            return
        }
        
        audioEngine = AVAudioEngine()
        let tapNode = audioEngine!.tapNode(at: audioEngine!.mainMixerNode, numberOfChannels: 1)
        tap = tapNode
        
        tapNode?.installTap(onBus: 0, bufferSize: 1024, format: tapNode?.inputFormat(forBus: 0)) { buffer, time in
            // Per UX Principle 1: Instant visual feedback
            let amplitude = self.audioLevel(for: buffer)
            self.waveform = Array(self.waveform.dropFirst()) + [amplitude]
        }
        
        do {
            try audioEngine?.start()
        } catch {
            state = .error
        }
        
        // Timer
        timer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { [weak self] _ in
            self?.duration += 0.1
        }
    }
    
    func stopRecording(completion: @escaping (URL?) -> Void) {
        guard let engine = audioEngine else { return }
        engine.pause()
        timer?.invalidate()
        
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd_HHmmss"
        let filename = "pilot_\(formatter.string(from: Date())).m4a"
        
        let tempDir = FileManager.default.temporaryDirectory
        let url = tempDir.appendingPathComponent(filename)
        
        let outputNode = engine.outputNode
        let format = outputNode.outputFormat(forBus: 0)
        
        do {
            try engine.start()
        } catch {
            // Start briefly to capture
        }
        
        state = .processing
        do {
            try outputNode.recordTOFile(url, format: format, fileSizeLimit: 50_000_000)
            Thread.sleep(forTimeInterval: 0.5)
            state = .idle
            duration = 0
            waveform = Array(repeating: 0, count: 50)
            completion(url)
        } catch {
            state = .error
            completion(nil)
        }
        
        audioEngine = nil
        tap = nil
    }
    
    private func audioLevel(for buffer: AVAudioPCMBuffer) -> Float {
        guard let channelData = buffer.floatChannelData else { return 0 }
        let channelDataArray = stride(from: 0, to: buffer.frameLength, by: 16).map { channelData[0][$0] }
        let levels = channelDataArray.map { abs($0) }
        return levels.reduce(0, +) / Float(levels.count)
    }
}

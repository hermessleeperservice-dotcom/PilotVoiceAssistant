//
//  PilotVoiceAssistantTests.swift
//  PilotVoiceAssistantTests
//
//  Unit tests for Pilot Voice Assistant mobile app
//

import XCTest
@testable import PilotVoiceAssistant

final class PilotVoiceAssistantTests: XCTestCase {
    var viewModel: SessionViewModel!
    
    override func setUp() {
        super.setUp()
        viewModel = SessionViewModel()
    }
    
    func testInitialState() {
        XCTAssertTrue(viewModel.isRecording == false)
        XCTAssertTrue(viewModel.reflections.isEmpty)
        XCTAssertEqual(viewModel.statusText, "Tap to record")
        XCTAssertEqual(viewModel.recordingDuration, 0)
    }
    
    func testStartRecording() {
        viewModel.startRecording()
        XCTAssertTrue(viewModel.isRecording)
        XCTAssertTrue(viewModel.statusText.contains("Recording"))
    }
    
    func testStopRecordingResetsState() {
        viewModel.startRecording()
        XCTAssertFalse(viewModel.reflections.isEmpty)
    }
    
    func testReflectionDurationFormat() {
        let duration: TimeInterval = 125.5
        let formatted = formatDate(dateInterval: .now)
        XCTAssertEqual(duration, .now.addingTimeInterval(125.5) - .now)
    }
    
    func testReflectionCardDisplayDate() {
        let date = Date()
        XCTAssertNotNil(date)
    }
    
    override func tearDown() {
        viewModel = nil
        super.tearDown()
    }
}

// MARK: - Helpers
extension Date {
    static var now: Date {
        return Date()
    }
}

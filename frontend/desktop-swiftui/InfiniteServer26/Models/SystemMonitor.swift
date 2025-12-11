//
//  SystemMonitor.swift
//  System monitoring model
//

import Foundation
import Combine

class SystemMonitor: ObservableObject {
    @Published var cpuUsage: Int = 45
    @Published var memoryUsage: Int = 62
    @Published var threatsBlocked: Int = 0
    @Published var activeContainers: Int = 8
    @Published var recentActivity: [String] = [
        "All systems health check passed",
        "JessicAi: No threats detected",
        "NayDoeV1: Optimization cycle completed",
        "NiA_Vault: Blockchain sync successful"
    ]
    
    private var timer: Timer?
    
    init() {
        startMonitoring()
    }
    
    func startMonitoring() {
        timer = Timer.scheduledTimer(withTimeInterval: 3.0, repeats: true) { [weak self] _ in
            self?.updateMetrics()
        }
    }
    
    func updateMetrics() {
        cpuUsage = Int.random(in: 40...60)
        memoryUsage = Int.random(in: 55...75)
    }
    
    deinit {
        timer?.invalidate()
    }
}

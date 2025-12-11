//
//  DashboardView.swift
//  Main dashboard showing system overview
//

import SwiftUI
import Charts

struct DashboardView: View {
    @EnvironmentObject var systemMonitor: SystemMonitor
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Header
                HStack {
                    Text("System Overview")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                    
                    Spacer()
                    
                    HStack(spacing: 8) {
                        Image(systemName: "shield.fill")
                            .foregroundColor(.green)
                        Text("FORTRESS MODE ACTIVE")
                            .font(.headline)
                            .foregroundColor(.green)
                    }
                    .padding(.horizontal, 16)
                    .padding(.vertical, 8)
                    .background(Color.green.opacity(0.1))
                    .cornerRadius(8)
                }
                .padding()
                
                // Metrics Grid
                LazyVGrid(columns: [GridItem(.adaptive(minimum: 250))], spacing: 20) {
                    MetricCard(
                        icon: "bolt.fill",
                        title: "CPU Usage",
                        value: "\(systemMonitor.cpuUsage)%",
                        color: .yellow
                    )
                    
                    MetricCard(
                        icon: "memorychip",
                        title: "Memory Usage",
                        value: "\(systemMonitor.memoryUsage)%",
                        color: .blue
                    )
                    
                    MetricCard(
                        icon: "lock.shield",
                        title: "Threats Blocked",
                        value: "\(systemMonitor.threatsBlocked)",
                        color: .green
                    )
                    
                    MetricCard(
                        icon: "cube.box.fill",
                        title: "Active Containers",
                        value: "\(systemMonitor.activeContainers)",
                        color: .purple
                    )
                }
                .padding(.horizontal)
                
                // AI Systems Status
                VStack(alignment: .leading, spacing: 12) {
                    Text("AI Systems Status")
                        .font(.title2)
                        .fontWeight(.semibold)
                        .padding(.horizontal)
                    
                    AISystemStatusRow(name: "NayDoeV1 Orchestrator", status: "AUTONOMOUS", isOnline: true)
                    AISystemStatusRow(name: "JessicAi Huntress", status: "NO MERCY MODE", isOnline: true)
                    AISystemStatusRow(name: "Quantum TwinBrain", status: "ENHANCED", isOnline: true)
                    AISystemStatusRow(name: "NAi_gAil Shield", status: "IMPENETRABLE", isOnline: true)
                }
                .padding()
                .background(Color(.windowBackgroundColor))
                .cornerRadius(12)
                .padding(.horizontal)
                
                // Activity Feed
                VStack(alignment: .leading, spacing: 12) {
                    Text("Recent Activity")
                        .font(.title2)
                        .fontWeight(.semibold)
                        .padding(.horizontal)
                    
                    ForEach(systemMonitor.recentActivity, id: \.self) { activity in
                        ActivityRow(activity: activity)
                    }
                }
                .padding()
                .background(Color(.windowBackgroundColor))
                .cornerRadius(12)
                .padding(.horizontal)
            }
            .padding()
        }
    }
}

struct MetricCard: View {
    let icon: String
    let title: String
    let value: String
    let color: Color
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: icon)
                    .font(.title)
                    .foregroundColor(color)
                
                Spacer()
            }
            
            Text(title)
                .font(.subheadline)
                .foregroundColor(.secondary)
            
            Text(value)
                .font(.title)
                .fontWeight(.bold)
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color(.windowBackgroundColor))
        .cornerRadius(12)
        .shadow(radius: 2)
    }
}

struct AISystemStatusRow: View {
    let name: String
    let status: String
    let isOnline: Bool
    
    var body: some View {
        HStack {
            Circle()
                .fill(isOnline ? Color.green : Color.red)
                .frame(width: 8, height: 8)
            
            Text(name)
                .font(.body)
            
            Spacer()
            
            Text(status)
                .font(.caption)
                .fontWeight(.semibold)
                .foregroundColor(.green)
                .padding(.horizontal, 12)
                .padding(.vertical, 4)
                .background(Color.green.opacity(0.1))
                .cornerRadius(12)
        }
        .padding(.horizontal)
        .padding(.vertical, 8)
    }
}

struct ActivityRow: View {
    let activity: String
    
    var body: some View {
        HStack {
            Text("• ")
                .foregroundColor(.green)
            Text(activity)
                .font(.body)
                .foregroundColor(.secondary)
        }
        .padding(.horizontal)
        .padding(.vertical, 4)
    }
}

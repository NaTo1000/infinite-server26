//
//  AISystemsView.swift
//  AI Systems control interface
//

import SwiftUI

struct AISystemsView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text("AI Systems Control Center")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                    .padding()
                
                LazyVGrid(columns: [GridItem(.adaptive(minimum: 350))], spacing: 20) {
                    AISystemCard(
                        name: "NayDoeV1 Orchestrator",
                        icon: "brain",
                        status: "ONLINE",
                        mode: "AUTONOMOUS",
                        uptime: "156 hours",
                        tasks: "12,847"
                    )
                    
                    AISystemCard(
                        name: "JessicAi Huntress",
                        icon: "shield.checkered",
                        status: "HUNTING",
                        mode: "NO MERCY",
                        uptime: "156 hours",
                        tasks: "0 Threats"
                    )
                    
                    AISystemCard(
                        name: "Quantum TwinBrain",
                        icon: "cpu",
                        status: "ENHANCED",
                        mode: "ACTIVE",
                        uptime: "156 hours",
                        tasks: "1,234 Decisions"
                    )
                }
                .padding(.horizontal)
            }
            .padding()
        }
    }
}

struct AISystemCard: View {
    let name: String
    let icon: String
    let status: String
    let mode: String
    let uptime: String
    let tasks: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack {
                Image(systemName: icon)
                    .font(.title)
                    .foregroundColor(.green)
                
                Text(name)
                    .font(.headline)
                
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
            
            Divider()
            
            VStack(alignment: .leading, spacing: 8) {
                InfoRow(label: "Mode:", value: mode)
                InfoRow(label: "Uptime:", value: uptime)
                InfoRow(label: "Tasks:", value: tasks)
            }
            
            HStack(spacing: 12) {
                Button("View Logs") {}
                    .buttonStyle(.borderedProminent)
                
                Button("Configure") {}
                    .buttonStyle(.bordered)
            }
        }
        .padding()
        .background(Color(.windowBackgroundColor))
        .cornerRadius(12)
        .shadow(radius: 2)
    }
}

struct InfoRow: View {
    let label: String
    let value: String
    
    var body: some View {
        HStack {
            Text(label)
                .foregroundColor(.secondary)
                .font(.subheadline)
            
            Text(value)
                .fontWeight(.semibold)
                .font(.subheadline)
        }
    }
}

struct SecurityView: View {
    var body: some View {
        Text("Security Control Center")
            .font(.largeTitle)
            .padding()
    }
}

struct BlockchainView: View {
    var body: some View {
        Text("NiA_Vault Blockchain")
            .font(.largeTitle)
            .padding()
    }
}

struct ContainersView: View {
    var body: some View {
        Text("Container Management")
            .font(.largeTitle)
            .padding()
    }
}

struct SettingsView: View {
    var body: some View {
        Text("System Settings")
            .font(.largeTitle)
            .padding()
    }
}

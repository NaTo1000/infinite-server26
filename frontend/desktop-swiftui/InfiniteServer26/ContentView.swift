//
//  ContentView.swift
//  Infinite Server26 Desktop
//
//  Main dashboard view for the Fortress control center
//

import SwiftUI

struct ContentView: View {
    @EnvironmentObject var systemMonitor: SystemMonitor
    @State private var selectedTab: Tab = .dashboard
    
    enum Tab {
        case dashboard
        case aiSystems
        case security
        case blockchain
        case containers
        case settings
    }
    
    var body: some View {
        NavigationView {
            // Sidebar
            List {
                NavigationLink(destination: DashboardView(), tag: Tab.dashboard, selection: $selectedTab) {
                    Label("Dashboard", systemImage: "square.grid.2x2")
                }
                
                NavigationLink(destination: AISystemsView(), tag: Tab.aiSystems, selection: $selectedTab) {
                    Label("AI Systems", systemImage: "brain")
                }
                
                NavigationLink(destination: SecurityView(), tag: Tab.security, selection: $selectedTab) {
                    Label("Security", systemImage: "shield.fill")
                }
                
                NavigationLink(destination: BlockchainView(), tag: Tab.blockchain, selection: $selectedTab) {
                    Label("Blockchain", systemImage: "link")
                }
                
                NavigationLink(destination: ContainersView(), tag: Tab.containers, selection: $selectedTab) {
                    Label("Containers", systemImage: "cube.box.fill")
                }
                
                NavigationLink(destination: SettingsView(), tag: Tab.settings, selection: $selectedTab) {
                    Label("Settings", systemImage: "gearshape.fill")
                }
            }
            .listStyle(SidebarListStyle())
            .frame(minWidth: 200)
            
            // Main content
            DashboardView()
        }
        .navigationTitle("∞ Infinite Server26")
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .environmentObject(SystemMonitor())
    }
}

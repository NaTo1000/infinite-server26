//
//  InfiniteServer26App.swift
//  Infinite Server26 Desktop
//
//  Created by NaTo1000
//  Version: 26.1 - FORTRESS
//

import SwiftUI

@main
struct InfiniteServer26App: App {
    @StateObject private var systemMonitor = SystemMonitor()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(systemMonitor)
                .frame(minWidth: 1200, minHeight: 800)
        }
        .windowStyle(.hiddenTitleBar)
        .commands {
            CommandGroup(replacing: .appInfo) {
                Button("About Infinite Server26") {
                    NSApplication.shared.orderFrontStandardAboutPanel(
                        options: [
                            NSApplication.AboutPanelOptionKey.credits: NSAttributedString(
                                string: "Autonomous AI-Powered Security Fortress\nVersion 26.1 - FORTRESS\nBuilt by NaTo1000",
                                attributes: [NSAttributedString.Key.font: NSFont.systemFont(ofSize: 11)]
                            ),
                            NSApplication.AboutPanelOptionKey(rawValue: "Copyright"): "© 2025 NaTo1000"
                        ]
                    )
                }
            }
        }
    }
}

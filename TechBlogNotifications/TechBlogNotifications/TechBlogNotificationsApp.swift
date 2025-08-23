//
//  TeckBlogNotificationsApp.swift
//  TeckBlogNotifications
//
//  Created by 이상현 on 5/29/24.
//

import SwiftUI
import FirebaseCore
import FirebaseFirestore

@main
struct TeckBlogNotificationsApp: App {
    @State var postManager: PostManager
    
    init() {
        FirebaseApp.configure()
        
        let settings = FirestoreSettings()
        settings.isPersistenceEnabled = true
        settings.cacheSizeBytes = FirestoreCacheSizeUnlimited
        Firestore.firestore().settings = settings
        
        self._postManager = State(initialValue: PostManager())
    }
    
    var body: some Scene {
        WindowGroup {
            MainView()
                .environment(postManager)
        }
    }
}

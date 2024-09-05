//
//  TeckBlogNotificationsApp.swift
//  TeckBlogNotifications
//
//  Created by 이상현 on 5/29/24.
//

import SwiftUI

@main
struct TeckBlogNotificationsApp: App {
    @State var postManager: PostManager = PostManager()
    
    var body: some Scene {
        WindowGroup {
            MainView()
                .environment(postManager)
        }
    }
}

//
//  PostRowView.swift
//  TechBlogNotifications
//
//  Created by 이상현 on 6/8/24.
//

import SwiftUI
import SafariServices

struct PostRowView: View {
    @Environment(PostManager.self) private var postManager
    
    var post: Post
    
    var body: some View {
        NavigationLink(destination: PostDetailView(post: post)) {
            VStack(alignment: .leading, spacing: 12) {
                Text(post.title)
                    .font(.headline)
                    .fontWeight(.bold)
                HStack {
                    Image("\(post.blogName)_favicon")
                    Text("\(post.blogName)")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
            }
            .padding(.vertical, 4)
            .padding(.trailing, 12)
        }
    }
}

struct PostDetailView: View {
    @Environment(PostManager.self) private var postManager
    @State private var isShareSheetPresented = false
    var post: Post
    
    var body: some View {
        WebView(url: URL(string: post.link)!)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {
                        postManager.toggleBookmark(for: post) // 북마크 상태 토글
                    }) {
                        Image(systemName: post.isBookmarked ? "bookmark.fill" : "bookmark")
                    }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    ShareLink(item: URL(string: post.link)!)
                }
            }
    }
}

#Preview {
    MainView()
        .environment(PostManager())
}

//
//  PostRowView.swift
//  TeckBlogNotifications
//
//  Created by 이상현 on 6/8/24.
//

import SwiftUI

// MARK: PostRowView
struct PostRowView: View {
    var post: Post
    
    var body: some View {
        NavigationLink {
            WebView(url: URL(string: post.link)!)
        } label: {
            VStack(alignment: .leading, spacing: 10) {
                HStack {
                    Text("\(post.blogName)")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                    Spacer()
                    Text(post.timestamp, format: Date.FormatStyle(date: .numeric, time: .omitted))
                        .font(.caption)
                        .foregroundColor(.gray)
                }
                Text(post.title)
                    .font(.headline)
                    .fontWeight(.bold)
            }
        }
        
    }
}

#Preview {
    MainView()
        .environment(PostManager())
}

//
//  BookmarkView.swift
//  TeckBlogNotifications
//
//  Created by 이상현 on 6/8/24.
//

import SwiftUI

struct BookmarkView: View {
    @Environment(PostManager.self) private var postManager
    
    var body: some View {
        NavigationStack {
            List {
//                let bookmarkedPosts = postManager.getBookmarkedPosts()
//                if bookmarkedPosts.isEmpty {
//                    Text("북마크된 게시글이 없습니다.")
//                        .font(.headline)
//                        .padding()
//                } else {
//                    ForEach(bookmarkedPosts) { post in
//                        PostRowView(post: post)
//                    }
//                }
            }
            .navigationTitle("북마크")
        }
    }
}

#Preview {
    BookmarkView()
        .environment(PostManager())
}

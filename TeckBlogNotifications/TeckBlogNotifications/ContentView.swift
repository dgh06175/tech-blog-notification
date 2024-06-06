//
//  ContentView.swift
//  TeckBlogNotifications
//
//  Created by 이상현 on 5/29/24.
//

import SwiftUI
import SwiftData

struct ContentView: View {
    @Environment(\.modelContext) private var modelContext
    @Query private var items: [Post]
    var postService: PostService
    var groupedPosts : [String: [Post]] {
        postService.groupPostsByDate(posts: SamplePosts.contents)
    }

    var body: some View {
        NavigationSplitView {
            List {
                ForEach(groupedPosts.keys.sorted().reversed(), id: \.self) { key in
                    Section {
                        ForEach(groupedPosts[key]!) { post in
                            PostRowView(post: post)
                        }
                        .onDelete(perform: deleteItems)
                    } header: {
                        Text(key)
                    }
                }
            }
            .navigationTitle("기술 블로그 게시글")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    EditButton()
                }
            }
        } detail: {
            Text("Select an item")
        }
    }

    private func deleteItems(offsets: IndexSet) {
        withAnimation {
            for index in offsets {
                modelContext.delete(items[index])
            }
        }
    }
}

struct PostRowView: View {
    var post: Post
    
    var body: some View {
        NavigationLink {
            WebView(url: URL(string: post.link)!)
        } label: {
            HStack {
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
                VStack {
                    Image(systemName: "bookmark")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 16)
                    Spacer()
                }
                .padding(.vertical, 10)
            }
        }
    }
}

#Preview {
    ContentView(postService: PostService())
        .modelContainer(previewContainer)
        //.modelContainer(for: Post.self, inMemory: true)
}

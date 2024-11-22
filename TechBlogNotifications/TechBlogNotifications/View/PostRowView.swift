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
                    CachedAsyncImage(url: URL(string: FavIcon(post.baseUrl)[.s]))
                        .frame(width: 16, height: 16)
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

struct CachedAsyncImage: View {
    let url: URL?
    @State private var uiImage: UIImage? = nil
    @State private var isLoading = false
    
    var body: some View {
        Group {
            if let uiImage = uiImage {
                Image(uiImage: uiImage)
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } else if isLoading {
                ProgressView()
            } else {
                Image(systemName: "photo")
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .foregroundColor(.gray)
            }
        }
        .onAppear {
            loadImage()
        }
    }
    
    private func loadImage() {
        guard let url = url else { return }
        
        // URLCache를 통한 캐싱된 데이터 확인
        if let cachedResponse = URLCache.shared.cachedResponse(for: URLRequest(url: url)),
           let cachedImage = UIImage(data: cachedResponse.data) {
            DispatchQueue.main.async {
                self.uiImage = cachedImage
            }
            return
        }
        
        // 네트워크 요청 시작
        isLoading = true
        URLSession.shared.dataTask(with: url) { data, response, error in
            defer {
                DispatchQueue.main.async {
                    self.isLoading = false
                }
            }
                        
            guard let data = data, let response = response, error == nil,
                  let image = UIImage(data: data) else {
                return
            }
            
            // 캐시 저장
            if let response = response as? HTTPURLResponse,
               (200...299).contains(response.statusCode) {
                let cachedData = CachedURLResponse(response: response, data: data)
                URLCache.shared.storeCachedResponse(cachedData, for: URLRequest(url: url))
            }
            
            // UI 업데이트
            DispatchQueue.main.async {
                self.uiImage = image
            }
        }.resume()
    }
}

#Preview {
    MainView()
        .environment(PostManager())
}

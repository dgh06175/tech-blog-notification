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
                    CachedAsyncImage(urls: FavIcon(post.baseUrl).candidates(blogName: post.blogName, size: .l))
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
    let urls: [URL]
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
            loadImage(candidateIndex: 0)
        }
    }

    // 후보 URL을 순서대로 시도한다. Google favicon 서비스는 못 찾은 도메인에도 (404 상태이지만)
    // 유효한 기본 이미지를 돌려주므로, 디코딩 성공 여부만으로는 실패를 감지할 수 없다. 그래서
    // HTTP 상태 코드까지 확인해 진짜 실패일 때만 다음 후보로 넘어간다.
    private func loadImage(candidateIndex: Int) {
        guard candidateIndex < urls.count else { return }
        let url = urls[candidateIndex]

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

            guard let data = data, error == nil,
                  let httpResponse = response as? HTTPURLResponse,
                  (200...299).contains(httpResponse.statusCode),
                  let image = UIImage(data: data) else {
                DispatchQueue.main.async {
                    self.loadImage(candidateIndex: candidateIndex + 1)
                }
                return
            }

            // 캐시 저장
            let cachedData = CachedURLResponse(response: httpResponse, data: data)
            URLCache.shared.storeCachedResponse(cachedData, for: URLRequest(url: url))

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

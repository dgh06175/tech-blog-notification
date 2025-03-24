//
//  ContentView.swift
//  TechBlogNotifications
//
//  Created by 이상현 on 5/29/24.
//

import SwiftUI

struct MainView: View {
    @Environment(PostManager.self) private var postManager
    //    @State var selectedHour: Int = 9
    //    @State private var isPickerPresented = false
    
    var groupedPosts: [String: [Post]] {
        groupPostsByDate(posts: postManager.posts)
    }
    
    var body: some View {
        NavigationStack {
            List {
                ForEach(groupedPosts.keys.sorted().reversed(), id: \.self) { key in
                    Section {
                        if let posts = groupedPosts[key] {
                            ForEach(Array(posts.enumerated()), id: \.offset) { index, post in
                                PostRowView(post: post)
                            }
                        } else {
                            Text("게시글 없음")
                        }
                    } header: {
                        Text(key)
                    }
                }
                if !groupedPosts.isEmpty {
                    LastListLoadingView()
                        .onAppear {
                            Task {
                                await postManager.loadNextPage()
                            }
                        }
                }
            }
            .disabled(postManager.isLoading)
            .redacted(reason: postManager.isLoading ? .placeholder : [])
            .navigationTitle(Constants.Messages.HOME_TITLE)
            // TODO: 알림 툴바
            //            .toolbar {
            //                ToolbarItem(placement: .topBarTrailing) {
            //                    Button(action: { isPickerPresented.toggle() }, label: {
            //                        HStack {
            //                            Image(systemName: "bell")
            //                            if selectedHour <= 12 {
            //                                Text("\(selectedHour) AM")
            //                            } else {
            //                                Text("\(selectedHour - 12) PM")
            //                            }
            //                        }
            //                    })
            //                }
            //            }
            //            .sheet(isPresented: $isPickerPresented) {
            //                VStack {
            //                    Text("알림 시간을 선택하세요")
            //                        .font(.headline)
            //                    Picker("알림 시간", selection: $selectedHour) {
            //                        ForEach(0..<24) { hour in
            //                            Text("\(hour)시").tag(hour)
            //                        }
            //                    }
            //                    .pickerStyle(WheelPickerStyle())
            //                    .labelsHidden()
            //                    .frame(height: 150)
            //                    .clipped()
            //                    Button("확인") {
            //                        isPickerPresented = false
            //                    }
            //                }
            //                .padding()
            //                .presentationDetents([.height(240)])
            //            }
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    NavigationLink(destination: BookmarkView()) {
                        Image(systemName: "book")
                    }
                }
            }
        }
    }
}

extension MainView {
    private static let RECENT_POST_DAY = 1
    
    private func groupPostsByDate(posts: [Post]) -> [String: [Post]] {
        var groupedPosts: [String: [Post]] = [:]
        
        let calendar = Calendar.current
        let now = Date()
        
        for post in posts {
            if (post.blogName == "Aws") {
                continue
            }
            let dateComponentsToNow = calendar.dateComponents([.year, .month, .day], from: post.pubDate, to: now)
            
            let groupKey: String
            if dateComponentsToNow.year == 0 && dateComponentsToNow.month == 0 && dateComponentsToNow.day ?? 0 <= MainView.RECENT_POST_DAY {
                groupKey = Constants.Messages.RECENT
            } else {
                groupKey = post.pubDate.formatDateToYearMonth()
            }
            
            if groupedPosts[groupKey] != nil {
                groupedPosts[groupKey]!.append(post)
            } else {
                groupedPosts[groupKey] = [post]
            }
        }
        return groupedPosts
    }
}

struct LastListLoadingView: View {
    var body: some View {
        Text(Constants.Messages.LOADING)
    }
}

#Preview {
    MainView()
        .environment(PostManager())
}

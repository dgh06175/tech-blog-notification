//
//  PostService.swift
//  TeckBlogNotifications
//
//  Created by 이상현 on 5/30/24.
//

import Foundation

class PostService {
    
    /**
     날짜 별로 게시글들을 딕셔너리로 그룹화 하는 함수
     */
    func groupPostsByDate(posts: [Post]) -> [String: [Post]] {
        var groupedPosts: [String: [Post]] = [:]
        
        let calendar = Calendar.current
        let now = Date()
        
        for post in posts {
            let components = calendar.dateComponents([.year, .month, .day], from: post.timestamp, to: now)
            
            let groupKey: String
            if components.year == 0 && components.month == 0 && components.day ?? 0 <= 1 {
                groupKey = "최신"
            } else {
                let dateFormatter = DateFormatter()
                dateFormatter.dateFormat = "yyyy년 MM월"
                groupKey = dateFormatter.string(from: post.timestamp)
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

//
//  PostService.swift
//  TeckBlogNotifications
//
//  Created by 이상현 on 5/30/24.
//

import Foundation

class PostService {
    private static let RECENT_POST_DAY = 1
    
    /**
     날짜 별로 게시글들을 딕셔너리로 그룹화 하는 함수
     */
    func groupPostsByDate(posts: [Post]) -> [String: [Post]] {
        var groupedPosts: [String: [Post]] = [:]
        
        let calendar = Calendar.current
        let now = Date()
        
        for post in posts {
            let dateComponentsToNow = calendar.dateComponents([.year, .month, .day], from: post.timestamp, to: now)
            
            let groupKey: String
            if dateComponentsToNow.year == 0 && dateComponentsToNow.month == 0 && dateComponentsToNow.day ?? 0 <= PostService.RECENT_POST_DAY {
                groupKey = Constants.Messages.RECENT
            } else {
                groupKey = post.timestamp.formatDateToYearMonth()
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

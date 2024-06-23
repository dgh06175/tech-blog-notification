//
//  Item.swift
//  TeckBlogNotifications
//
//  Created by 이상현 on 5/29/24.
//

import Foundation

@Observable
class Post: Identifiable {
    var id: Int64
    var link: String
    var blogName: String
    var title: String
    var timestamp: Date
    
    init(id: Int64, blogName: String, link: String, title: String, timestamp: Date) {
        self.id = id
        self.blogName = blogName
        self.link = link
        self.title = title
        self.timestamp = timestamp
    }
}

//var isBookMark: Bool
//var bookMarkCount: Int
//var isSeen: Bool
//var tags: [String]

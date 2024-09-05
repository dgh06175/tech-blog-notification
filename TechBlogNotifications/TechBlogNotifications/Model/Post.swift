//
//  Item.swift
//  TechBlogNotifications
//
//  Created by 이상현 on 5/29/24.
//

import Foundation

struct Post: Identifiable, Decodable {
    var id: Int64
    var link: String
    var blogName: String
    var title: String
    var pubDate: Date
    var scrapedDate: Date
    
    enum CodingKeys: String, CodingKey {
        case id
        case link
        case blogName
        case title
        case pubDate
        case scrapedDate
    }
}

//var isBookMark: Bool
//var bookMarkCount: Int
//var isSeen: Bool
//var tags: [String]
